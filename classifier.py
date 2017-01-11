import os
import sys
import numpy as np

import lightgbm as lgb


TRAINING_DIR = "./output/train/"
FINAL_FEATURES_DIR = "./output/final/features/"

MODEL_DIR = "./output/model/"
PREDICTION_DIR = "./output/prediction/"


def get_data(tf, cell):
    training_data_fname = os.path.join(
        TRAINING_DIR, "{}.{}.tab".format(factor, cell))
    features = list()
    labels = list()
    with open(training_data_fname, "r") as file:
        lines = file.readlines()
        for line in lines:
            ll = line.strip().split("\t")
            if int(ll[1]) >= 0:
                labels.append(ll[:1])
                features.append(ll[1:])
    return labels, features


def train(labels, features):
    X = np.asarray(features).astype(np.float)
    y = np.asarray(labels).astype(np.int)
    y = np.ravel(y)

    train_size = int(0.9 * len(y))
    X_train = X[:train_size]
    X_test = X[train_size:]
    y_train = y[:train_size]
    y_test = y[train_size:]

    lgb_train = lgb.Dataset(X_train, y_train)
    lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train)

    params = {
        'task': 'train',
        'boosting_type': 'gbdt',
        'objective': 'binary',
        'metric': {'binary_logloss'},
        'max_bin': 255,
        'num_tree': 100,
        'learning_rate': 0.1,
        'num_leaves': 63,
        'feature_fraction': 0.8,
        'bagging_freq': 5,
        'bagging_fraction': 0.8,
        'verbose': 0,
        'num_iterations': 600
    }

    # train
    gbm = lgb.train(params,
                    lgb_train,
                    valid_sets=lgb_eval,
                    num_boost_round=20,
                    early_stopping_rounds=5)
    return gbm


def output_model(factor, cell, gbm):
    model_fname = os.path.join(MODEL_DIR, "{}.{}.model".format(factor, cell))
    gbm.save_model(model_fname)


def final(factor, cell_list, gbm_dict):
    chrom_list = ["chr1", "chr10", "chr11", "chr12", "chr13", "chr14", "chr15", "chr16", "chr17", "chr18", "chr19",
                  "chr2", "chr20", "chr21", "chr22", "chr3", "chr4", "chr5", "chr6", "chr7",
                  "chr8", "chr9", "chrX"]
    for test_cell in cell_list:
        test_fname = os.path.join(PREDICTION_DIR, "F.{}.{}.tab".format(factor, test_cell))
        with open(test_fname, "a") as test_file:
            for chrom in chrom_list:
                features_fname = os.path.join(
                    FINAL_FEATURES_DIR, "F.{}.{}.{}.tab".format(factor, test_cell, chrom))
                with open(features_fname, "r") as file:
                    #  skip the header
                    file.readline()
                    lines = file.readlines()
                    for line in lines:
                        data = line.strip().split("\t")
                        header = data[:3]
                        feature = data[3:]
                        X = np.asarray(feature).astype(np.float)
                        proba_list = list()
                        for cell, gbm in gbm_dict.iteritems():
                            X_reshape = X.reshape(1, -1)
                            proba = gbm_dict[cell].predict(X_reshape,
                                                           num_iteration=gbm_dict[cell].best_iteration)[0]
                            proba_list.append(proba)
                        predict = sum(proba_list) / float(len(proba_list))
                        test_file.write("\t".join(header) + "\t" + str("%.3e" % predict) + "\n")
        os.system("gzip " + test_fname)


if __name__ == '__main__':
    factor = sys.argv[1]
    train_cell_list = sys.argv[2].split(",")
    final_cell_list = sys.argv[3].split(",")

    gbm_dict = dict()
    for cell in train_cell_list:
        labels, features = get_data(factor, cell)
        gbm_dict[cell] = train(labels, features)
        output_model(factor, cell, gbm_dict[cell])
    final(factor, final_cell_list, gbm_dict)
