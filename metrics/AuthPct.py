# This file contains functions for the data-copying test in addition to
# each of the baselines demonstrated in the paper

import torch
import numpy as np
from sklearn.neighbors import NearestNeighbors as NN
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from fls.metrics.Metric import Metric


class AuthPct(Metric):
    def __init__(self):
        super().__init__()
        self.name = "AuthPct"

    def compute_metric(
        self,
        train_feat,
        baseline_feat,
        test_feat,
        gen_feat,
        plot=False,
    ):
        real_dists = torch.cdist(train_feat, train_feat)

        # Hacky way to get it to ignore distance to self in nearest neighbor calculation
        real_dists.fill_diagonal_(float("inf"))
        gen_dists = torch.cdist(train_feat, gen_feat)

        real_min_dists = real_dists.min(axis=0)
        gen_min_dists = gen_dists.min(dim=0)

        authen = real_min_dists.values[gen_min_dists.indices] < gen_min_dists.values
        return 100 * torch.sum(authen) / len(authen)
