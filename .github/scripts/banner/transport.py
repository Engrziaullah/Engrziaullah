"""Stage 4: optimal-transport (Hungarian assignment) matching between successive logos,
so each traveler dot takes the shortest possible path python->pytorch->opencv."""
import os
import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import cdist

HERE = os.path.dirname(os.path.abspath(__file__))


def optimal_match(a, b, seed=0):
    cost = cdist(a, b, metric="sqeuclidean")
    row_ind, col_ind = linear_sum_assignment(cost)
    matched_b = b[col_ind]
    dist = np.sqrt(((a - matched_b) ** 2).sum(axis=1))

    rng = np.random.default_rng(seed)
    rand_perm = rng.permutation(len(b))
    rand_dist = np.sqrt(((a - b[rand_perm]) ** 2).sum(axis=1))

    return matched_b, dist, rand_dist


def main():
    py = np.load(os.path.join(HERE, "logo_dots_python.npy"))
    pt = np.load(os.path.join(HERE, "logo_dots_pytorch.npy"))
    cv = np.load(os.path.join(HERE, "logo_dots_opencv.npy"))

    pt_matched, d1, rd1 = optimal_match(py, pt, seed=1)
    cv_matched, d2, rd2 = optimal_match(pt_matched, cv, seed=2)

    print(f"python->pytorch: mean travel {d1.mean():.2f}px (optimal) vs {rd1.mean():.2f}px (random assignment), "
          f"{rd1.mean()/d1.mean():.2f}x shorter")
    print(f"pytorch->opencv: mean travel {d2.mean():.2f}px (optimal) vs {rd2.mean():.2f}px (random assignment), "
          f"{rd2.mean()/d2.mean():.2f}x shorter")

    # save the three POSITION SETS each traveler dot visits, in matched order:
    # index i -> py[i] -> pt_matched[i] -> cv_matched[i]
    np.save(os.path.join(HERE, "traveler_python.npy"), py)
    np.save(os.path.join(HERE, "traveler_pytorch.npy"), pt_matched)
    np.save(os.path.join(HERE, "traveler_opencv.npy"), cv_matched)


if __name__ == "__main__":
    main()
