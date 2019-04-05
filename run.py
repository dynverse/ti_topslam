#!/usr/local/bin/python

import dynclipy
task = dynclipy.main()

# force matplotlib backend, to avoid tkinter problems (through GPy)
import matplotlib
matplotlib.use('PS')

# add topslam to syspath
import sys
sys.path.insert(0, "/topslam")

# import topslam and others
import os
import json
import pandas as pd
import numpy as np
import topslam
from topslam.optimization import run_methods, create_model, optimize_model
from topslam import ManifoldCorrectionTree

import time
checkpoints = {}

#   ____________________________________________________________________________
#   Load data                                                               ####

expression = task["expression"]
p = task["parameters"]
start_id = task["priors"]["start_id"]
if isinstance(start_id, list):
  start_id = np.random.choice(start_id)

checkpoints["method_afterpreproc"] = time.time()

#   ____________________________________________________________________________
#   Infer trajectory                                                        ####
# run topslam
from sklearn.manifold import TSNE, LocallyLinearEmbedding, SpectralEmbedding, Isomap
from sklearn.decomposition import FastICA, PCA

n_components = p["n_components"]

methods = {
  't-SNE':TSNE(n_components=n_components),
  'PCA':PCA(n_components=n_components),
  'Spectral': SpectralEmbedding(n_components=n_components, n_neighbors=p["n_neighbors"]),
  'Isomap': Isomap(n_components=n_components, n_neighbors=p["n_neighbors"]),
  'ICA': FastICA(n_components=n_components)
}
method_names = sorted(methods.keys())
method_names_selected = [method_names[i] for i, selected in enumerate(p["dimreds"]) if selected]
methods = {method_name:method for method_name, method in methods.items() if method_name in method_names_selected}

# dimensionality reduction
X_init, dims = run_methods(expression, methods)

# model expression
m = create_model(expression, X_init, linear_dims=p["linear_dims"])
m.optimize(messages=1, max_iters=p["max_iters"])

# manifold correction
m_topslam = ManifoldCorrectionTree(m)
start_cell_ix = expression.index.tolist().index(start_id)
pt_topslam = m_topslam.get_pseudo_time(start=start_cell_ix, estimate_direction=True)

# calculate landscape
landscape = topslam.landscape.waddington_landscape(m, resolution=100, xmargin=(0.5, 0.5), ymargin=(0.5, 0.5))

checkpoints["method_aftermethod"] = time.time()

#   ____________________________________________________________________________
#   Process & save output                                                   ####

dataset = dynclipy.wrap_data(cell_ids = expression.index)

pseudotime = pd.DataFrame({
  "cell_id": expression.index,
  "pseudotime": pt_topslam
})

dataset.add_linear_trajectory(pseudotime = pseudotime)

# pd.DataFrame(landscape[0], columns=["x", "y"]).to_csv("/ti/output/wad_grid.csv", index=False)
# pd.DataFrame(landscape[1], columns=["energy"]).to_csv("/ti/output/wad_energy.csv", index=False)

dimred = pd.DataFrame(landscape[2], columns=["comp_" + str(i+1) for i in range(landscape[2].shape[1])])
dimred["cell_id"] = expression.index

dataset.add_dimred(dimred)

# timings
dataset.add_timings(checkpoints)

# save
dataset.write_output(task["output"])
