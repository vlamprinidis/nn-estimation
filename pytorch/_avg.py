import torch 
import torch.nn as nn
import argparse

from tor_data import give
import funs_torch
import funs

parser = argparse.ArgumentParser()
parser.add_argument('-numf', type = int, required = True,
                           choices = funs.numf_ls )
parser.add_argument('-batch', type = int, required = True, 
                           choices = funs.batch_ls )
parser.add_argument('-nodes', type = int, required = True,
                           choices = funs.nodes_ls )
parser.add_argument('-epochs', type = int, required = True)
parser.add_argument('-channels', type = int, required = True)
parser.add_argument('-pool', type = int, required = True)
parser.add_argument('-stride', type = int, required = True)
parser.add_argument('-dim', type = int, required = True)
args = parser.parse_args()

DIM = args.dim
RESULT = '__avg{}d.torch'.format(DIM)
avg_pool = nn.AvgPool1d if DIM==1 else nn.AvgPool2d    

layer = avg_pool(kernel_size = args.pool, stride = args.stride)

model = nn.Sequential(
    layer,
    nn.Flatten(),
    nn.Linear(
        in_features = args.channels * funs_torch.avg_size_out(args.numf, args.pool, args.stride) ** DIM,
        out_features = 10
    )
)

train_dataset = give(DIM, args.numf, args.channels)

if args.nodes > 1:
    model, train_loader = funs_torch.distribute(model, train_dataset, args.nodes, batch)
else:
    train_loader = torch.utils.data.DataLoader(
        dataset = train_dataset,
        batch_size = args.batch,
        shuffle = True
    )

prof = funs_torch.profile(model, train_loader, args.epochs)

if prof != None:
    key = funs.my_key({
        'numf':args.numf,
        'batch':args.batch,
        'nodes':args.nodes,
        'channels':args.channels,
        'pool':args.pool,
        'stride':args.stride
    })
    value = funs_torch.get_ops(prof)
    
    funs.update(key, value, RESULT)