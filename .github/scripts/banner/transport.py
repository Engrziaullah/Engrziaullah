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
    a = np.load(os.path.join(HERE, "logo_dots_langchain.npy"))
    b = np.load(os.path.join(HERE, "logo_dots_langgraph.npy"))
    c = np.load(os.path.join(HERE, "logo_dots_langsmith.npy"))

    b_matched, d1, rd1 = optimal_match(a, b, seed=1)
    c_matched, d2, rd2 = optimal_match(b_matched, c, seed=2)

    print(f"langchain->langgraph: mean travel {d1.mean():.2f}px (optimal) vs {rd1.mean():.2f}px (random assignment), "
          f"{rd1.mean()/d1.mean():.2f}x shorter")
    print(f"langgraph->langsmith: mean travel {d2.mean():.2f}px (optimal) vs {rd2.mean():.2f}px (random assignment), "
          f"{rd2.mean()/d2.mean():.2f}x shorter")

    # save the three POSITION SETS each traveler dot visits, in matched order:
    # index i -> a[i] -> b_matched[i] -> c_matched[i]
    np.save(os.path.join(HERE, "traveler_langchain.npy"), a)
    np.save(os.path.join(HERE, "traveler_langgraph.npy"), b_matched)
    np.save(os.path.join(HERE, "traveler_langsmith.npy"), c_matched)


if __name__ == "__main__":
    main()
