import os
import sys

LABELS_DIR = "/hpcwork/izkf/projects/dream_tfbs/local/ChIPseq/labels/"  # change this line

TRAINING_LABELS_DIR = "./data/training/labels/"
TRAINING_FEATURES_DIR = "./data/training/features/"
TRAINING_DIR = "./data/training/"


chrom_list = list()


def get_labels_data(factor, cell_list):
    labels_fname = os.path.join(LABELS_DIR, "{}.train.labels.tsv.gz".format(factor))
    ziped_labels_fname = os.path.join(TRAINING_LABELS_DIR, "{}.train.labels.tsv.gz".format(factor))
    unziped_labels_fname = os.path.join(TRAINING_LABELS_DIR, "{}.train.labels.tsv".format(factor))

    remove_list = list()
    remove_list.append(unziped_labels_fname)

    os.system("cp " + labels_fname + " " + TRAINING_LABELS_DIR)
    os.system("gzip -d " + ziped_labels_fname)

    header = list()
    with open(unziped_labels_fname, "r") as file:
        header = file.readline().strip().split("\t")

    for cell in cell_list:
        factor_cell_labels_fname = os.path.join(TRAINING_LABELS_DIR, "{}.{}.train.labels".format(factor, cell))
        index = header.index(cell) + 1
        os.system("cut -f1-3," + str(index) + " " + unziped_labels_fname + " > " + factor_cell_labels_fname)
        remove_list.append(factor_cell_labels_fname)
        for chrom in chrom_list:
            factor_cell_chr_labels_fname = os.path.join(
                TRAINING_LABELS_DIR, "{}.{}.{}.train.labels".format(factor, cell, chrom))
            os.system("grep -w " + str(chrom) + " " + factor_cell_labels_fname + " > " + factor_cell_chr_labels_fname)

    for e in remove_list:
        os.system("rm " + e)


def get_training_data(factor, cell_list):
    chrom_list = ["chr2", "chr22", "chr9"]
    for cell in cell_list:
        remove_list = []
        training_fname = os.path.join(TRAINING_DIR, "{}.{}".format(factor, cell))
        remove_list.append(training_fname)
        for chrom in chrom_list:
            features_fname = os.path.join(TRAINING_FEATURES_DIR, "T.{}.{}.{}.tab".format(factor, cell, chrom))

            # Fetch the features
            cut_features_fname = os.path.join(TRAINING_DIR, "T.{}.{}.{}.tab.cut".format(factor, cell, chrom))
            os.system("cut -f4- " + features_fname + " > " + cut_features_fname)

            # Fetch the labels
            training_labels_fname = os.path.join(
                TRAINING_LABELS_DIR, "{}.{}.{}.train.labels".format(factor, cell, chrom))
            cut_labels_fname = os.path.join(TRAINING_DIR, "{}.{}.{}.train.labels.cut".format(factor, cell, chrom))
            os.system("cut -f4 " + training_labels_fname + " > " + cut_labels_fname)

            # Merge them
            merge_data_fname = os.path.join(TRAINING_DIR, "{}.{}.{}.merge".format(factor, cell, chrom))
            os.system("paste " + cut_labels_fname + " " + cut_features_fname + " > " + merge_data_fname)

            os.system("cat " + merge_data_fname + " >> " + training_fname)
            remove_list.append(cut_features_fname)
            remove_list.append(cut_labels_fname)
            remove_list.append(merge_data_fname)

        # Remove the label A (representing ambiguous)
        remove_a_fname = os.path.join(TRAINING_DIR, "{}.{}.rma".format(factor, cell))
        os.system("sed '/A/d' " + training_fname + " > " + remove_a_fname)
        remove_list.append(remove_a_fname)

        # remove the repeated data
        uniq_fname = os.path.join(TRAINING_DIR, "{}.{}.uniq".format(factor, cell))
        os.system("uniq " + remove_a_fname + " > " + uniq_fname)
        remove_list.append(uniq_fname)

        # Replace the label B (representing bound) with 1 and U (representing unbound) with 0
        repleace_b_fname = os.path.join(TRAINING_DIR, "{}.{}.rpb".format(factor, cell))
        repleace_u_fname = os.path.join(TRAINING_DIR, "{}.{}.rpu".format(factor, cell))
        os.system("tr 'B' '1' < " + uniq_fname + " > " + repleace_b_fname)
        os.system("tr 'U' '0' < " + repleace_b_fname + " > " + repleace_u_fname)
        remove_list.append(repleace_b_fname)

        # Rename the final data file
        final_fname = os.path.join(TRAINING_DIR, "{}.{}.tab".format(factor, cell))
        os.system("mv " + repleace_u_fname + " " + final_fname)

        for e in remove_list:
            os.remove(e)


if __name__ == '__main__':
    factor = sys.argv[1]
    cell_list = sys.argv[2].split(",")
    get_labels_data(factor, cell_list)
    get_training_data(factor, cell_list)
