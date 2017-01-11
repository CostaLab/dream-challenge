import os

tf_cell_table_fname = "./tf_cell_table.txt"
train_tf_cell_dict = dict()
final_tf_cell_dict = dict()
with open(tf_cell_table_fname, "r") as file:
    file.readline()
    for line in file:
        ll = line.strip().split("\t")
        train_tf_cell_dict[ll[0]] = ll[1].split(",")
        final_tf_cell_dict[ll[0]] = ll[3].split(",")


for factor, train_cell_list in train_tf_cell_dict.iteritems():
    final_tf_cell_dict = final_tf_cell_dict[factor]
    job_name = "score_" + factor
    command = "bsub -J " + job_name + " -o " + "./cluster_out/" + \
        job_name + "_out.txt -e " + "./cluster_out/" + job_name + "_err.txt "
    command += "-W 120:00 -M 51200 -S 100 -R \"select[hpcwork]\"  ./pipeline_classifier.zsh"
    os.system(command + " " + str(factor) + " " + ",".join(train_cell_list) + " " + ",".join(final_tf_cell_dict))
