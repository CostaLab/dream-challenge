
# Import
import os


genomeFileName = "/hpcwork/izkf/projects/TfbsPrediction/Data/HG19/hg19.fa"  # change this line
bedLoc = "/hpcwork/izkf/projects/dream_tfbs/local/annotations/"  # change this line
dnaseBamLoc = "/hpcwork/izkf/projects/dream_tfbs/exp/dnase/"  # change this line

# Iterating on the challenge level
challengeList = ["train"]
for challenge in challengeList:

    # Challenge Parameters
    if(challenge == "ladder"):
        challengeLabel = "L"
        challengeCol = 2
    elif(challenge == "train"):
        challengeLabel = "T"
        challengeCol = 1
    else:
        challengeLabel = "F"
        challengeCol = 3

    # Iterating on TF-CELL table
    tfCellTableFileName = "./tf_cell_table.txt"
    tfCellTableFile = open(tfCellTableFileName, "r")
    tfCellTableFile.readline()
    for line in tfCellTableFile:

        # Line parsing
        ll = line.strip().split("\t")
        if(ll[challengeCol] == "."):
            continue
        factor = ll[0]
        trainCellList = ll[1].split(",")
        testCellList = ll[challengeCol].split(",")

        # Creating PFM list based on training cells
        pfmLoc = "./data/motifs/pfm_hocomoco_meme/"
        pfmInfoFileName = pfmLoc + "info.txt"
        pfmInfoFile = open(pfmInfoFileName, "r")
        pfmList = []
        for line2 in pfmInfoFile:
            ll2 = line2.strip().split("\t")
            if(ll2[0] == factor):
                pfmList = [pfmLoc + e + ".pwm" for e in ll2[1].split(",")]
                break
        pfmInfoFile.close()

        # Iterating on test cells
        for cell in testCellList:

            # Iterating on chromosomes
            if(challenge == "train"):
                chromList = ["chr2"]
            if(challenge == "final"):
                chromList = ["chr1", "chr10", "chr11", "chr12", "chr13", "chr14", "chr15",
                             "chr16", "chr17", "chr18", "chr19", "chr2", "chr20", "chr21",
                             "chr22", "chr3", "chr4", "chr5", "chr6", "chr7", "chr8", "chr9", "chrX"]
            if(challenge == "ladder"):
                chromList = ["chr1", "chr21", "chr8"]

            for chrom in chromList:

                # Parameters
                bedFileName = bedLoc + challenge + "_" + chrom + ".bed"
                pfmFileNameList = ",".join(pfmList)

                footprintBamFileName = "./data/footprints/results/" + cell + ".bam"
                dnaseBamFileName = dnaseBamLoc + cell + "/" + cell + "_DNase.bam"
                ol = "./output/" + challenge + "/features/"
                os.system("mkdir -p " + ol)
                outputFileName = ol + challengeLabel + "." + factor + "." + cell + "." + chrom + ".tab"

                # Execution on the cluster
                myL = "_".join([challenge, factor, cell, chrom])
                clusterCommand = "bsub -J " + myL + " -o " + myL + "_out.txt -e " + myL + "_err.txt "
                clusterCommand += "-W 120:00 -M 24000 -S 100 -R \"select[hpcwork]\" ./pipeline_features.zsh "
                clusterCommand += bedFileName + " " + pfmFileNameList + " " + genomeFileName + \
                    " " + footprintBamFileName + " "
                clusterCommand += dnaseBamFileName + " " + outputFileName
                os.system(clusterCommand)

                # Execution on your computer
                # myL = "_".join([challenge, factor, cell, chrom])
                # clusterCommand += "./pipeline_features.zsh "
                # clusterCommand += bedFileName + " " + pfmFileNameList + " " + genomeFileName + \
                #     " " + footprintBamFileName + " "
                # clusterCommand += dnaseBamFileName + " " + outputFileName
                # os.system(clusterCommand)

    tfCellTableFile.close()
