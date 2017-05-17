import sys

def read_standard(filename, name):
    f = h5py.File(filename, 'r')
    x = f[name][()]
    f.close()
    return x
def save_standard(data, filename):
    f = h5py.File(filename, 'w')
    f.create_dataset('trainxdata', data=data)
    f.close()
def check_and_shrink(x, y):
    xn = x.shape[0]
    yn = y.shape[0]
    if xn != yn:
        print('The size of x and y are different. Exiting', file=sys.stderr)
        sys.exit()
    x = x[:int(xn/2)]
    y = y[:int(xn/2)]
    return (x, y)
def binary_to_fasta(x, filename, window_size):
    lx = x.shape[1]
    if window_size > lx or window_size < 200:
        print('Window size is too big. Exiting', file=sys.stderr)
        sys.exit()
    half = int(window_size / 2)
    if window_size % 2 == 0:
        subx = x[:, 400 - half : 800 + half, :]
    else:
        subx = x[:, 400 - half - 1 : 800 + half, :]
    o = open(filename, 'w')
    for i in range(x.shape[0]):
        seq = _binary_to_seq(x[i])
        o.write('>{i}\n'.format(i=i))
        o.write(seq + '\n')
    o.close()
def _binary_to_seq(bianry):
    pick_list = np.array([0,1,2,3])
    alphabet_dic = { 0:'A': 1:'G', 2:'C', 3:'T' }
    seq = ''
    for j in range(binary.shape[0]):
        bin_char = binary[j, :]
        picked = pick_list[bin_char == 1]
        if picked.size == 0:
            char = 'N'
        else:
            char = alphabet_dic[picked[0]]
        seq = seq + char
    return seq
