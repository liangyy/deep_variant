import h5py
import numpy as np

def read_standard_data_x(filename):
    f = h5py.File(filename, 'r')
    x = f['trainxdata'][()]
    f.close()
    return x
def binary_to_char(binary):
    dic = { 1: 'A', 2: 'G', 3: 'C', 4: 'T', 0: 'N' }
    code = np.array([1, 2, 3, 4])
    codes = np.dot(binary, code)
    seq = ''
    for i in codes:
        seq = seq + dic[i]
    return seq

def save_layer(activation, spatial_x, dataname, filename):
    f = h5py.File(filename, 'w+')
    grp = f.create_group(dataname)
    grp.create_dataset('activation', activation)
    grp.create_dataset('spatial_x', spatial_x)
    f.close()
