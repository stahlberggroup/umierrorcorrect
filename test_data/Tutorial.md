## Tutorial
This tutorial shows an example on how to use umierrorcorrect

### Step 1 - Download the example files

Download the files from [here](https://guse.sharefile.eu/d-s878525e0e6234cd69de7b4e4cfa4c113)

Create a folder named `tutorial` and move the files there. 

### Step 2 - Reference genome

The `run_umierrorcorrect` script is running `bwa mem` for aligning the reads to the reference genome. In this tutorial the data contains reads from chr3 of the Human genome.

If you don't have a version of the Human reference genome, you can download the sequence in fasta format for chromosome3 (or for the full data set) from the hgdownload page (UCSC genome browser) [http://hgdownload.cse.ucsc.edu/downloads.html#human](http://hgdownload.cse.ucsc.edu/downloads.html#human).

After downloading the reference fasta file, unzip the file and index the file using `bwa`. For example:

```bash
gunzip chr3.fa.gz
bwa index chr3.fa
```

### Step 3 - Run UMI error correct

The data in the file `test_1.fastq.gz` is single end data generated with the SimSenSeq protocol described in Ståhlberg et al. (2017; [https://doi.org/10.1038/nprot.2017.006](https://doi.org/10.1038/nprot.2017.006)).

According to the protocol, the parameters umi length (`ul`) should be set to 12 and spacer length (`sl`) is set to 16.

Run the `umierrorcorrect` pipeline with the following command:

```python
run_umierrorcorrect.py -o tutorial_output -r1 test_1.fastq.gz \
-r chr3.fa -bed target_regions_hg38.bed -ul 12 -sl 16 -t 1
```

The `-o` specifies the path to the output directory. If it doesn't exist it will be created.

The `-r1` specifies the path to the fastq file with sequencing data.

The `-r` specifies the path to the reference genome fasta file.

The `-bed` specifies the path to the bedfile that will be used for annotation. If you used hg38 reference genome, this should be the path to the target_regions_hg38.bed file. If you used hg19 reference genome, this should be the path to the target_regions_hg19.bed file. 

The `-ul` parameter specifies the UMI sequence length. It should be 12 in this case.

The `-sl` parameter specifies the length of the spacer. It should be 16 in this case.

The `-t` parameter specifies the number of cpu threads the program will be run on.

All the other parameters will be set to default values.

### Step 4 - Filter the cons file

The pipeline should have created 8 files in the folder `tutorial_out`

