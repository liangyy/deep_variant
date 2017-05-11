import h5py
def read_data(filename):
    f = h5py.File(filename, 'r')
    x = f['trainxdata'][()]
    f.close()
    return x
def save_data(data, filename):
    f = h5py.File(filename, 'w')
    f.create_dataset('y_pred', data=data)
    f.close()
