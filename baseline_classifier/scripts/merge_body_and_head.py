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

from keras.models import load_model
body = load_model(args.body)
head = load_model(args.head)
noutput = head.layers[-1].output_shape[-1]
from keras.layers import Dense, Activation
body.add(Dense(noutput, name='head_dense'))
body.layers[-1].set_weights(head.layers[-2].get_weights())
body.add(Activation('sigmoid', name='head_activation'))
body.compile(optimizer='sgd', loss='binary_crossentropy')
body.save(args.out)
