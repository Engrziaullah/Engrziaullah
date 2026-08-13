"""Stage 2: rasterize the official brand SVGs into filled dot clouds (~900 pts each),
sized to overlay the same VISUAL.MAP frame as the portrait."""
import os
import re
import numpy as np
from matplotlib.path import Path as MplPath
from PIL import Image
from svgpath import parse_path_d

HERE = os.path.dirname(os.path.abspath(__file__))
LOGOS_DIR = os.path.join(HERE, "logos")
TARGET_N = 900
RASTER_RES = 260  # supersample grid for fill test, then subsample to TARGET_N points

LOGOS = ["langchain", "langgraph", "langsmith"]
EXCLUDE_FILL = {"langsmith": "#030710"}  # LangSmith ships a background chip we don't want


def rasterize_logo(svg_path, out_res=RASTER_RES, exclude_fill=None):
    with open(svg_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Strip <defs>...</defs> (clipPath rects etc.) and <mask ...>...</mask> DEFINITION
    # blocks (not <g mask="url(#...)"> usages, which we want to keep) - some official
    # marks (e.g. LangSmith's) ship a background chip + luminance mask alongside the
    # actual glyph paths; we only want the visible glyph.
    content = re.sub(r"<defs\b.*?</defs>", "", content, flags=re.DOTALL)
    content = re.sub(r"<mask\b[^>]*>.*?</mask>", "", content, flags=re.DOTALL)
    path_tags = re.findall(r"<path\b[^>]*/?>", content)
    d_strings = []
    for tag in path_tags:
        if exclude_fill and f'fill="{exclude_fill}"' in tag:
            continue
        m = re.search(r'\sd="([^"]+)"', tag)
        if m:
            d_strings.append(m.group(1))
    all_polys = []
    for d in d_strings:
        all_polys.extend([p for p in parse_path_d(d) if len(p) >= 3])

    all_pts = np.concatenate(all_polys, axis=0)
    minx, miny = all_pts.min(axis=0)
    maxx, maxy = all_pts.max(axis=0)
    w, h = maxx - minx, maxy - miny
    scale = (out_res * 0.92) / max(w, h)
    off_x = (out_res - w * scale) / 2 - minx * scale
    off_y = (out_res - h * scale) / 2 - miny * scale

    def to_px(poly):
        return poly * scale + np.array([off_x, off_y])

    px_polys = [to_px(p) for p in all_polys]

    yy, xx = np.mgrid[0:out_res, 0:out_res]
    sample_pts = np.column_stack([xx.ravel() + 0.5, yy.ravel() + 0.5])

    # Even-odd fill across ALL subpaths combined (handles inner holes like the 'o' counters correctly)
    codes = None
    vertices = []
    all_codes = []
    for poly in px_polys:
        vertices.append(poly)
        c = [MplPath.MOVETO] + [MplPath.LINETO] * (len(poly) - 1)
        all_codes.extend(c)
    vertices = np.concatenate(vertices, axis=0)
    combined = MplPath(vertices, all_codes)
    inside = combined.contains_points(sample_pts)
    mask = inside.reshape(out_res, out_res)
    return mask


def sample_dots(mask, n_target, rng):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        raise RuntimeError("empty mask")
    if len(xs) >= n_target:
        idx = rng.choice(len(xs), size=n_target, replace=False)
    else:
        idx = rng.choice(len(xs), size=n_target, replace=True)
    pts = np.column_stack([xs[idx], ys[idx]]).astype(float)
    pts += rng.uniform(-0.4, 0.4, size=pts.shape)
    return pts


def main():
    rng = np.random.default_rng(20260813)
    results = {}
    for name in LOGOS:
        svg_path = os.path.join(LOGOS_DIR, f"{name}.svg")
        mask = rasterize_logo(svg_path, exclude_fill=EXCLUDE_FILL.get(name))
        fill_frac = mask.mean()
        print(f"{name}: raster fill {fill_frac*100:.1f}% of {RASTER_RES}x{RASTER_RES} box, "
              f"{mask.sum()} candidate px")
        Image.fromarray((mask * 255).astype(np.uint8)).save(os.path.join(HERE, f"diag_logo_{name}.png"))
        pts = sample_dots(mask, TARGET_N, rng)
        results[name] = pts
        np.save(os.path.join(HERE, f"logo_dots_{name}.npy"), pts)
        print(f"  -> sampled {len(pts)} dots, bbox x[{pts[:,0].min():.1f},{pts[:,0].max():.1f}] "
              f"y[{pts[:,1].min():.1f},{pts[:,1].max():.1f}]")

    return results


if __name__ == "__main__":
    main()
