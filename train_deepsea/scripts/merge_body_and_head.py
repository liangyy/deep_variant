import argparse
parser = argparse.ArgumentParser(prog='merge_body_and_head.py', description='''
    Given the Keras model that extracts motif feature from primary sequences (body)
    and the Keras model that takes features and predicts labels based on logistic
    regression, output a merged model by combining the two parts
''')
parser.add_argument('--body')
parser.add_argument('--head')
parser.add_argument('--out')
args = parser.parse_args()

import sys
if 'scripts/' not in sys.path:
    sys.path.insert(0, 'scripts/')
import my_python
from keras.models import load_model
from keras.models import Model

body = load_model(args.body)
try:
    head = load_model(args.head)
except UnboundLocalError:
    head = load_model(args.head, custom_objects = {'binary_accuracy_svm': my_python.binary_accuracy_svm, 'hinge_svm': my_python.hinge_svm}) 
noutput = head.layers[-1].output_shape[-1]
from keras.layers import Dense, Activation

x = body.layers[-1].output
x = Dense(noutput, name='head_dense')(x)
x = Activation('sigmoid', name='head_activation')(x)
model = Model(inputs=body.layers[0].input, outputs=x)
model.layers[-2].set_weights(head.layers[-2].get_weights())
model.compile(optimizer='sgd', loss='binary_crossentropy')
model.save(args.out)
