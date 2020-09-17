from lib import clean_go

opt = {
    'all': '-numf {numf} -batch {b} -nodes {nodes} -epochs {e} -channels {ch} -dim {dim}'.format,
    'conv': '-kern {kernel} -filters {filters} -stride {stride}'.format,
    'pool': '-pool {pool} -stride {stride}'.format,
    'dense': '-numf {numf} -batch {b} -nodes {nodes} -epochs {e} -units {units}'.format,
    'drop': '-drop {drop}'.format
}

pt_files = ['_flatten.py', '_avg.py', '_conv.py', '_dense.py', '_drop.py', '_max.py', '_norm.py', '_relu.py', '_tanh.py']

# PyTorch
FRAME = '/home/ubuntu/.env/bin/python3 /home/ubuntu/profile/ptorch/{file} {p1} {p2}'.format
epochs = 5

dim = 2

for nodes in [3,2,1]:
    for numf in [16, 32, 64]:
        for batch in [32, 64, 256, 512]:
            for channels in [1,3]:
                opt_all = opt['all'](numf=numf, b=batch, nodes=nodes, e=epochs, ch=channels, dim=dim)

                # Conv 2d
                for kernel in [2,4,8]:
                    for filters in [1,2,4,8,16]:
                        for stride in [1,2,4]:
                            cmd = FRAME(file = '_conv.py', 
                                 p1 = opt_all,
                                 p2 = opt['conv'](kernel=kernel, filters=filters, stride=stride))
                            clean_go(cmd, nodes)


for nodes in [3,2,1]:
    for numf in [16, 32, 64]:
        for batch in [32, 64, 256, 512]:
            for channels in [1,3]:
                opt_all = opt['all'](numf=numf, b=batch, nodes=nodes, e=epochs, ch=channels, dim=dim)

                # Pool 2d
                for file in ['_avg.py', '_max.py']:
                    for pool in [2,4,8]:
                        for stride in [1,2,4]:
                            cmd = FRAME(file = file, 
                                 p1 = opt_all,
                                 p2 = opt['pool'](pool=pool, stride=stride))
                            clean_go(cmd, nodes)


for nodes in [3,2,1]:
    for numf in [16, 32, 64]:
        for batch in [32, 64, 256, 512]:
            for channels in [1,3]:
                opt_all = opt['all'](numf=numf, b=batch, nodes=nodes, e=epochs, ch=channels, dim=dim)

                # Dropout 2d
                for drop in [0.2, 0.4, 0.8]:
                    cmd = FRAME(file = '_drop.py',
                                p1 = opt_all,
                                p2 = opt['drop'](drop = drop))
                    clean_go(cmd, nodes)


for nodes in [3,2,1]:
    for numf in [16, 32, 64]:
        for batch in [32, 64, 256, 512]:
            for channels in [1,3]:
                opt_all = opt['all'](numf=numf, b=batch, nodes=nodes, e=epochs, ch=channels, dim=dim)

                # Batch Normalization, Relu, Tanh, Alone 2d
                for file in ['_norm.py', '_relu.py', '_tanh.py', '_flatten.py']:
                    cmd = FRAME(file = file,
                                p1 = opt_all,
                                p2 = '')
                    clean_go(cmd, nodes)


for nodes in [3,2,1]:
    for numf in [16,32,64,128,256,512,1024,2048,4096]:
        for batch in [32, 64, 256, 512]:
            # Dense
            for units in [16, 32, 64, 128]:
                cmd = FRAME(file = '_dense.py',
                            p1 = opt['dense'](numf=numf, b=batch, nodes=nodes, e=epochs, units = units),
                            p2 = '')
                clean_go(cmd, nodes)


# dim = 1

# for nodes in [3,2,1]:
#     for numf in [16, 32, 64]:
#         for batch in [32, 64, 256, 512]:
#             for channels in [1,3]:
#                 opt_all = opt['all'](numf=numf, b=batch, nodes=nodes, e=epochs, ch=channels, dim=dim)

#                 # Conv 1d
#                 for kernel in [2,4,8]:
#                     for filters in [1,2,4,8,16]:
#                         for stride in [1,2,4]:
#                             cmd = FRAME(file = '_conv.py', 
#                                  p1 = opt_all,
#                                  p2 = opt['conv'](kernel=kernel, filters=filters, stride=stride))
#                             clean_go(cmd, nodes)


# for nodes in [3,2,1]:
#     for numf in [16, 32, 64]:
#         for batch in [32, 64, 256, 512]:
#             for channels in [1,3]:
#                 opt_all = opt['all'](numf=numf, b=batch, nodes=nodes, e=epochs, ch=channels, dim=dim)

#                 # Pool 1d
#                 for file in ['_avg.py', '_max.py']:
#                     for pool in [2,4,8]:
#                         for stride in [1,2,4]:
#                             cmd = FRAME(file = file, 
#                                  p1 = opt_all,
#                                  p2 = opt['pool'](pool=pool, stride=stride))
#                             clean_go(cmd, nodes)


# for nodes in [3,2,1]:
#     for numf in [16, 32, 64]:
#         for batch in [32, 64, 256, 512]:
#             for channels in [1,3]:
#                 opt_all = opt['all'](numf=numf, b=batch, nodes=nodes, e=epochs, ch=channels, dim=dim)

#                 # Dropout 1d
#                 for drop in [0.2, 0.4, 0.8]:
#                     cmd = FRAME(file = '_drop.py',
#                                 p1 = opt_all,
#                                 p2 = opt['drop'](drop = drop))
#                     clean_go(cmd, nodes)


# for nodes in [3,2,1]:
#     for numf in [16, 32, 64]:
#         for batch in [32, 64, 256, 512]:
#             for channels in [1,3]:
#                 opt_all = opt['all'](numf=numf, b=batch, nodes=nodes, e=epochs, ch=channels, dim=dim)

#                 # Batch Normalization, Relu, Tanh, Alone 1d
#                 for file in ['_norm.py', '_relu.py', '_tanh.py', '_flatten.py']:
#                     cmd = FRAME(file = file,
#                                 p1 = opt_all,
#                                 p2 = '')
#                     clean_go(cmd, nodes)