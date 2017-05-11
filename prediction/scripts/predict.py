import argparse
parser = argparse.ArgumentParser(prog='predict.py', description='''
    Given x in standard format and model, output prediction
''')
parser.add_argument('--x')
parser.add_argument('--model')
parser.add_argument('--out')
args = parser.parse_args()


import sys
if 'scripts/' not in sys.path:
    sys.path.insert(0, 'scripts/')
import os
os.environ['THEANO_FLAGS'] = "device=gpu"
os.environ['floatX'] = 'float32'
import keras
from keras.models import load_model
import my_python


x = my_python.read_data(args.x)
model = load_model(args.model)
pred = model.predict(x, verbose=1)
my_python.save_data(pred, args.out)
