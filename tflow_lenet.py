import numpy as np
import tensorflow as tf
strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy()

import tflow_lib
from tflow_models import LeNet5

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-nodes', type = int, required = True)
parser.add_argument('-batch', type = int, required = True)
parser.add_argument('-epochs', type = int, required = True)
args = parser.parse_args()
        
Model = LeNet5()
if args.nodes > 1:
    model = tflow_lib.distribute(strategy, Model, args.nodes)
else:
    model = Model.create()

# dataset = tflow_lib.give2d(ds_size=1024, numf=32, channels=3, out_size=10)
(x,y),_ = tf.keras.datasets.mnist.load_data(
    path='mnist.npz'
)

x = x.astype(np.float32)
x = x/255
x = x.reshape(x.shape[0], 28, 28, 1)

# y = y.astype(np.float32)
y = tf.keras.utils.to_categorical(y, 10)

dataset = tf.data.Dataset.from_tensor_slices((x, y))

the_time = tflow_lib.profile(model, dataset, args.batch, args.epochs)

import socket
host = socket.gethostname()

if(the_time != None):
    print()
    print('Host: ', host,', Time : ', the_time/1000/1000, ' s')
    print()
