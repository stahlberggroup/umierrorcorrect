#!/bin/bash
#make sure to install umierrorcorrect first, for example python setup.py install

#download example reference genome, in this case only human chromosome 3, for testing purposes.
wget http://hgdownload.soe.ucsc.edu/goldenPath/hg38/chromosomes/chr3.fa.gz 
gunzip chr3.fa.gz

#run the pipeline
run_umierrorcorrect.py -r1 test_data/test_R1.fastq.gz -r chr3.fa -ul 12 -sl 16 -o testout 
