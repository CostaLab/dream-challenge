#!/usr/bin/env zsh

export PATH=$PATH:/hpcwork/izkf/bin/:/home/rs619065/local/bin
export PYTHONPATH=$PYTHONPATH:/hpcwork/izkf/lib/python2.7/site-packages
export PYTHONPATH=$PYTHONPATH:/home/rs619065/local/lib64/python2.7/site-packages
export PYTHONPATH=$PYTHONPATH:/home/rs619065/local/lib/python2.7/site-packages
export R_LIBS_USER=$R_LIBS_USER:/home/rs619065/local/lib64/R/library

factor=$1
train_cell_list=$2
final_cell_list=$3

python data.py $factor $train_cell_list &&
## python classifier.py $factor $train_cell_list $final_cell_list
