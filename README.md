######################################################################################
# ENCODE-DREAM in vivo transcription factor binding site (TFBS) Prediction Challenge
# Team: HINT
# Authors: Eduardo G. Gusmao, Zhijian Li and Ivan G. Costa
# Email: (eduardo.gusmao, zhijian.li, ivan.costa)@rwth-aachen.de
######################################################################################

######################################################################################
# 1. Prerequisites
######################################################################################

To run our solution to the challenge, please make sure you have the following tools and python packages:

	1.1. numpy (http://www.numpy.org/) [tested in version 1.10.4]
	1.2. bedtools (http://bedtools.readthedocs.io/en/latest/) [tested in version 2.25.0]
	1.3. BioPython (http://biopython.org/) [tested in version 1.66]
	1.4. pysam (https://github.com/pysam-developers/pysam) [tested in version 0.8.3]
	1.5. MOODS (http://www.regulatory-genomics.org/wp-content/uploads/2016/04/MOODS_1.0.1.tar.gz)
	1.6. LightGBM (https://github.com/Microsoft/LightGBM) [tested in version 0.1]

The MOODS version needs to be the 1.0.1 as in the link provided above. To install, unzip the file and simply type the following commands:

cd <MOODS_DIRECTORY>/src
make
cd <MOODS_DIRECTORY>/python
sudo python setup.py install

######################################################################################
# 2. Execution Instructions:
######################################################################################

## Step 1: Generating Features
	
please open the file "features.py" in any text editor. Modify the lines marked with the comment "change this line" at the end.

2.1.1. The variable "genomeFileName" should point to the fasta file containing the genome sequence

2.1.2. The variable "bedLoc" should point to the location containing the bed file of the non-merged challenge region annotations.
([download here](https://www.synapse.org/#!Synapse:syn6184307))

2.1.3. The variable "dnaseBamLoc" should point to the bed file containing the DNase-seq data
([download here](https://www.synapse.org/#!Synapse:syn6176232))

After changing these lines just execute the following command:

python features.py

The features of the specified cell type (variable "cell" in the code) and transcription factor (variable "factor" in the code) 
and chromsome (variable "chrom" in the code) for challenge (train, leader, final ) will be in the correspond folder "./output/". 

## Step 2: Training Model and Prediction
	
please open the file "data.py" in any text editor. Modify the lines marked with the comment "change this line" at the end.

2.2.1. The variable "LABELS_DIR" should point the folder containing the labels file of factors.
([download here](https://www.synapse.org/#!Synapse:syn7413983))

After changing these lines just execute the following command:

python call_classifier.py

The predciton file for the specified cell type (variable "cell" in the code) and transcription factor (variable "factor" in the code) 
will be gzipped in the correct format in the folder "./output/prediction/"


