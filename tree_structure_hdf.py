#HDF file tree structure of all the available datasets and you can use it to find the correct path to the dataset you need
import h5py
import numpy as np

with h5py.File("Amite_20200114.g01.hdf", "r") as f:
    f.visit(print)
