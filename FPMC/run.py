import sys, os, pickle, argparse
from random import shuffle
import pandas as pd
from utils import *
#try:
#    from FPMC_numba import FPMC
#except ImportError:
#    from FPMC import FPMC
from FPMC import FPMC
# numba版本的应该更快，但是暂时还没调好，先用普通版本的

cwd = os.path.dirname(os.path.realpath(__file__))


allowed_trans = {}

n_road = 38026

df = pd.read_csv(cwd + '/../database/data/rel.csv')

for index, row in df.iterrows():
    origin_id = int(row['origin_id'])
    destination_id = int(row['destination_id'])

    if origin_id not in allowed_trans:
        allowed_trans[origin_id] = [origin_id]
    if destination_id != origin_id and destination_id not in allowed_trans[origin_id]:
        allowed_trans[origin_id].append(destination_id)
    
# 这是为了防止之后出现一些空数组
for i in range(n_road + 1):
    if i not in allowed_trans:
        allowed_trans[i] = [i]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir', help='The directory of input', type=str)
    parser.add_argument('-e', '--n_epoch', help='# of epoch', type=int, default=20)
    parser.add_argument('--n_neg', help='# of neg samples', type=int, default=15)
    parser.add_argument('-n', '--n_factor', help='dimension of factorization', type=int, default=32)
    parser.add_argument('-l', '--learn_rate', help='learning rate', type=float, default=0.02)
    parser.add_argument('-r', '--regular', help='regularization', type=float, default=0.001)
    args = parser.parse_args()
    
    f_dir = args.input_dir

    data_list, user_set, item_set = load_data_from_dir(f_dir)
    shuffle(data_list)

    train_ratio = 0.8
    split_idx = int(len(data_list) * train_ratio)
    tr_data = data_list[:split_idx]
    # print(tr_data)
    te_data = data_list[split_idx:]

    fpmc = FPMC(n_user=max(user_set)+1, n_item=max(item_set)+1, 
                n_factor=args.n_factor, learn_rate=args.learn_rate, regular=args.regular, allowed_trans=allowed_trans)
    fpmc.user_set = user_set
    fpmc.item_set = item_set
    fpmc.init_model()

    acc, mrr = fpmc.learnSBPR_FPMC(tr_data, te_data, n_epoch=args.n_epoch, 
                                   neg_batch_size=args.n_neg, eval_per_epoch=False)

    print ("Accuracy:%.2f MRR:%.2f" % (acc, mrr))
    
    fpmc.dump(fpmcObj=fpmc,fname=cwd+'/model.pkl')






