"""Stage 3: intro groups (interleaved, evenness-verified) and drift bands
(noise-jittered nearest-seed clustering, straight-boundary-verified)."""
import os
import numpy as np
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
GRID_W, GRID_H = 300, 340
N_INTRO_GROUPS = 60
N_BANDS = 94
SUBCELL = 2  # coarse quadrant split for evenness metric (finer grids are dominated by
             # Poisson sampling noise, not actual patchiness, at ~650 dots/group)


def evenness_metric(dot_rc, group_ids, n_groups, grid_w=GRID_W, grid_h=GRID_H, subcell=SUBCELL):
    """Mean coefficient-of-variation of each group's per-subcell counts, normalized
    against the OVERALL dot density in that subcell (not a uniform assumption) -
    the portrait's own content is non-uniform (dense hair/suit, sparse skin/background),
    so 'even' has to mean 'tracks the whole-image density profile', not 'uniform in space'.
    Low = every group is a fair miniature of the full portrait (good, scattered).
    High = some groups over/under-represent regions relative to the whole (patchy)."""
    cell_w = grid_w / subcell
    cell_h = grid_h / subcell
    cx = np.clip((dot_rc[:, 1] / cell_w).astype(int), 0, subcell - 1)
    cy = np.clip((dot_rc[:, 0] / cell_h).astype(int), 0, subcell - 1)
    cell_idx = cy * subcell + cx
    n_cells = subcell * subcell

    overall_counts = np.bincount(cell_idx, minlength=n_cells).astype(float)
    overall_frac = overall_counts / overall_counts.sum()

    cvs = []
    for g in range(n_groups):
        m = group_ids == g
        gn = m.sum()
        if gn < 2:
            continue
        counts = np.bincount(cell_idx[m], minlength=n_cells).astype(float)
        expected = gn * overall_frac
        valid = expected > 1e-9
        ratio = counts[valid] / expected[valid]
        cvs.append(ratio.std() / ratio.mean())
    return float(np.mean(cvs))


def make_intro_groups(dots_bool, n_groups=N_INTRO_GROUPS, seed=7):
    """Interleaved random assignment (NOT spatial) so every group is scattered
    across the whole portrait from the first frame."""
    rows, cols = np.nonzero(dots_bool)
    dot_rc = np.column_stack([rows, cols])
    n = len(dot_rc)
    rng = np.random.default_rng(seed)
    order = rng.permutation(n)
    group_ids = np.empty(n, dtype=int)
    group_ids[order] = np.arange(n) % n_groups
    ev = evenness_metric(dot_rc, group_ids, n_groups)

    # bad baseline for sanity check: spatial quadrant-ish grouping (blocks of columns)
    block = max(1, GRID_W // n_groups)
    bad_ids = np.clip(dot_rc[:, 1] // block, 0, n_groups - 1)
    ev_bad = evenness_metric(dot_rc, bad_ids, n_groups)

    return dot_rc, group_ids, ev, ev_bad


def straight_boundary_metric(band_grid):
    """Fraction of band-boundary edges that belong to a long (>=10) contiguous
    straight run along a single grid line. Low = organic. High = literal grid."""
    h, w = band_grid.shape
    # vertical boundaries (between column c and c+1), for each such boundary column,
    # find rows where a change occurs, then longest-run length among consecutive rows.
    total_edges = 0
    straight_edges = 0

    horiz_diff = band_grid[:, :-1] != band_grid[:, 1:]  # h x (w-1)
    for c in range(w - 1):
        rows_changed = np.nonzero(horiz_diff[:, c])[0]
        total_edges += len(rows_changed)
        if len(rows_changed) == 0:
            continue
        run = 1
        best = 1
        for k in range(1, len(rows_changed)):
            if rows_changed[k] == rows_changed[k - 1] + 1:
                run += 1
                best = max(best, run)
            else:
                run = 1
        if best >= 10:
            # count how many of this column's changed-edges are part of runs >=10
            run = 1
            start = 0
            for k in range(1, len(rows_changed) + 1):
                cont = k < len(rows_changed) and rows_changed[k] == rows_changed[k - 1] + 1
                if cont:
                    run += 1
                else:
                    if run >= 10:
                        straight_edges += run
                    run = 1

    vert_diff = band_grid[:-1, :] != band_grid[1:, :]  # (h-1) x w
    for r in range(h - 1):
        cols_changed = np.nonzero(vert_diff[r, :])[0]
        total_edges += len(cols_changed)
        if len(cols_changed) == 0:
            continue
        run = 1
        for k in range(1, len(cols_changed) + 1):
            cont = k < len(cols_changed) and cols_changed[k] == cols_changed[k - 1] + 1
            if cont:
                run += 1
            else:
                if run >= 10:
                    straight_edges += run
                run = 1

    if total_edges == 0:
        return 0.0
    return straight_edges / total_edges


def make_drift_bands(n_bands=N_BANDS, grid_w=GRID_W, grid_h=GRID_H, noise_sigma=4.0, seed=11):
    """Assign every grid cell to one of n_bands organic regions: noise-jittered
    nearest-seed (Voronoi-like), NOT axis-aligned blocks."""
    rng = np.random.default_rng(seed)
    seeds = rng.uniform([0, 0], [grid_h, grid_w], size=(n_bands, 2))

    rows, cols = np.mgrid[0:grid_h, 0:grid_w]
    coords = np.column_stack([rows.ravel(), cols.ravel()]).astype(float)
    noisy = coords + rng.normal(0, noise_sigma, size=coords.shape)

    tree = cKDTree(seeds)
    _, band_idx = tree.query(noisy)
    band_grid = band_idx.reshape(grid_h, grid_w)

    sb = straight_boundary_metric(band_grid)

    # bad baseline: literal grid blocks (no noise, axis-aligned)
    import math
    n_cols_blocks = int(math.ceil(math.sqrt(n_bands * grid_w / grid_h)))
    n_rows_blocks = int(math.ceil(n_bands / n_cols_blocks))
    block_w = grid_w / n_cols_blocks
    block_h = grid_h / n_rows_blocks
    bad_grid = (rows // block_h).astype(int) * n_cols_blocks + (cols // block_w).astype(int)
    sb_bad = straight_boundary_metric(bad_grid)

    band_centroids = np.array([coords[band_idx == b].mean(axis=0) if np.any(band_idx == b) else [grid_h / 2, grid_w / 2]
                                for b in range(n_bands)])

    return band_grid, band_centroids, sb, sb_bad


def main():
    dots_dark = np.load(os.path.join(HERE, "dots_dark.npy"))
    dots_light = np.load(os.path.join(HERE, "dots_light.npy"))

    for name, dots in (("dark", dots_dark), ("light", dots_light)):
        rc, gids, ev, ev_bad = make_intro_groups(dots)
        print(f"[{name}] intro groups: {len(rc)} dots -> {N_INTRO_GROUPS} groups, "
              f"evenness={ev:.4f} (bad-baseline comparison={ev_bad:.4f})")
        np.save(os.path.join(HERE, f"intro_rc_{name}.npy"), rc)
        np.save(os.path.join(HERE, f"intro_gid_{name}.npy"), gids)

    band_grid, band_centroids, sb, sb_bad = make_drift_bands()
    print(f"drift bands: straight-boundary={sb:.4f} (bad grid-baseline={sb_bad:.4f})")
    np.save(os.path.join(HERE, "band_grid.npy"), band_grid)
    np.save(os.path.join(HERE, "band_centroids.npy"), band_centroids)


if __name__ == "__main__":
    main()
