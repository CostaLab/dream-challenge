#!/usr/bin/env bash

# Input
inLoc=$1
oLoc=$2
factor=$3
genomeFastaFile=$4
motifdb=$5

# Creating MEME fasta input
outLoc=$oLoc$factor"_TEMP/"
mkdir -p $outLoc
gunzip -c $inLoc"ChIPseq."$factor".conservative.train.narrowPeak.gz" > $outLoc"a.bed"
python ./narrowPeakToCenter.py "50" $outLoc"a.bed" $outLoc"b.bed"
sort -k1,1 -k2,2n $outLoc"b.bed" > $outLoc"c.bed"
fastaFromBed -fi $genomeFastaFile -bed $outLoc"c.bed" -fo $outLoc"a.fa"

# Applying MEME-chip
memeLoc=$oLoc$factor"/"
mkdir -p $memeLoc
meme-chip -oc $memeLoc -db $motifdb -nmeme "600" -meme-mod "zoops" -meme-minw "5" -meme-maxw "15" -meme-nmotifs "5" -meme-p "4" $outLoc"a.fa"
rm -rf $outLoc


