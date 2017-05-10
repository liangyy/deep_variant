import argparse
parser = argparse.ArgumentParser(prog='train_logistic_on_cluster.py', description='''
    Given the input training data and validation data, train a logistic regression
	head with user specified l1 and l2 penalty on weights (bias is excluded) using
	Keras
''')
parser.add_argument('--train', help='''
    Sequence and label for training
''')
parser.add_argument('--valid', help='''
    Sequence and label for validation
''')
parser.add_argument('--outdir', help='''
    Output directory
''')
parser.add_argument('--batch_size', help='''
    The size of minibatch used for optimization
''')
parser.add_argument('--epoch', help='''
    Number of epochs (iterations)
''')
parser.add_argument('--l1', type=float, help='''
    L1 penalty
''')
parser.add_argument('--l2', type=float, help='''
    L2 penalty
''')
args = parser.parse_args()

import sys
if 'scripts/' not in sys.path:
    sys.path.insert(0, 'scripts/')
import my_python
import os
os.environ['THEANO_FLAGS'] = "device=gpu"
os.environ['floatX'] = 'float32'
import keras
from keras.optimizers import SGD
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.models import load_model
import glob

epochs = int(args.epoch)
batch_size = int(args.batch_size)

if args.outdir[-1] == os.sep:
	logfile = ''.join(args.outdir[:-1]) + '.log'
else:
	logfile = args.outdir + '.log'

breaker = '=' * 50

print('1 - Loading data')
X_train, y_train = my_python.load_data(args.train)
X_valid, y_valid = my_python.load_data(args.valid)
print(breaker)

print('2 - Building model')
files = glob.glob(args.outdir + os.sep + '*')
resume_flag = 0

if epochs <= len(files):
	print('The number of epochs has reached the goal! Exiting')
	sys.exit()
if len(files) == 0:
	print('No previous models detected, build a new one from scratch!')
	magic_1 = np.random.random_integers(10000)
	np.random.seed(magic_1)
	model = my_python.logistic_head(X_valid.shape[-1], y_valid.shape[-1], args.l1, args.l2)
	print('Write log to ' + logfile)
	loghandle = open(logfile, 'w')
	loghandle.write('Date\tMagicNum_Init\tMagicNum_Fit\tEpochNum_BeforeStart\n')
	loghandle.close()
else:
	print('Detected previous models, start resuming!')
	modelfile = ''
	# epochs -= len(files)
	for i in files:
		temp = ntpath.basename(i)
		temp = temp.split('-')
		if int(temp[0]) >= resume_flag:
			modelfile = i
			resume_flag = int(temp[0])
	resume_flag += 1
	magic_1 = np.random.random_integers(10000)
	np.random.seed(magic_1)
	model = load_model(modelfile)




# write into log file
magic_2 = np.random.random_integers(10000)
loghandle = open(logfile, 'a')
loghandle.write('\t'.join([time.asctime( time.localtime(time.time()) ), str(magic_1), str(magic_2), str(len(files))]) + '\n')
loghandle.close()

model.summary()
print(breaker)

print('3 - Training')
np.random.seed(magic_2)
checkpointer = ModelCheckpoint(filepath=sys.argv[3]+os.sep+"{epoch:02d}-{val_loss:.4f}-{loss:.4f}.hdf5", monitor='val_loss', verbose=1, save_best_only=False, period=1)
# earlystopper = EarlyStopping(monitor='val_loss', patience=5, verbose=1)
model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, shuffle=True,
          verbose=1, validation_data=(X_valid, y_valid), callbacks=[checkpointer], initial_epoch=resume_flag)
print(breaker)
