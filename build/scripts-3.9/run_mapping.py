#!python
import argparse
import subprocess
import sys
import os
import pysam
import logging
from umierrorcorrect.version import __version__

def parseArgs():
    parser = argparse.ArgumentParser(description="UmiErrorCorrect v. {}. \
                                                  Pipeline for analyzing barcoded amplicon sequencing \
                                                  data with Unique molecular identifiers (UMI)".format(__version__))
    parser.add_argument('-o', '--output_path', dest='output_path', 
                        help='Path to the output directory, required', required=True)
    parser.add_argument('-r1', '--read1', dest='read1', 
                        help='Path to first FASTQ file, R1, required', required=True)
    parser.add_argument('-r2', '--read2', dest='read2', 
                        help='Path to second FASTQ file, R2 if applicable')
    parser.add_argument('-r', '--reference', dest='reference_file', 
                        help='Path to the reference sequence in Fasta format (indexed), Required', required=True)
    parser.add_argument('-s', '--sample_name', dest='sample_name', 
                        help='Sample name that will be used as base name for the output files. \
                              If excluded the sample name will be extracted from the fastq files.')
    parser.add_argument('-remove', '--remove_large_files',  dest='remove_large_files', action='store_true',\
                            help='Include this flag to emove the original Fastq and BAM files (reads without error correction).')
    
    parser.add_argument('-t', '--num_threads', dest='num_threads', 
                        help='Number of threads to run the program on. Default=%(default)s', default='1')
    args = parser.parse_args(sys.argv[1:])
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
    logging.info('Starting UMI Error Correct')
    return(args)


def check_output_directory(outdir):
    '''Check if outdir exists, otherwise create it'''
    if os.path.isdir(outdir):
        return(outdir)
    else:
        os.mkdir(outdir)
        return(outdir)


def get_sample_name(read1, mode):
    '''Get the sample name as the basename of the input files.'''
    if mode == 'single':
        if '_umis_in_header' in read1:
            read1 = read1.replace('_umis_in_header', '')
        samplename = read1.split('/')[-1].rstrip('fastq').rstrip('fastq.gz')
    elif mode == 'paired':
        if '_umis_in_header' in read1:
            read1 = read1.replace('_umis_in_header', '')
        samplename = read1.split('/')[-1].rstrip('fastq').rstrip('fastq.gz').rstrip('_R012')
    return(samplename)

def check_bwa_index(reference_file):
    '''Check if BWA index files exists, otherwise create'''
    if not os.path.isfile(reference_file):
        print('Reference genome file {} does not exist, exiting'.format(reference_file))
        sys.exit(1)
    else:
        if not os.path.isfile(reference_file+'.bwt'): #check if index exists
            print('BWA index for reference genome file {} does not exist'.format(reference_file))
            answer=input("Do you want to create a BWA index now? (y/n) ".lower().strip())
            while not (answer == "y" or answer == "yes" or answer == "n" or answer == "no"):
                print("Answer yes or no ")
                answer=input("Do you want to create a BWA index now? (y/n) ".lower().strip())
            if answer[0]=="y":
                create_index=True
            else:
                create_index=False
                sys.exit(1)
            if create_index:
                a=subprocess.Popen(['bwa', 'index', reference_file])
                a.communicate()


def run_mapping(num_threads, reference_file, fastq_files, output_path, sample_name, remove_large_files):
    '''Run mapping with bwa to create a SAM file, then convert it to BAM, sort and index the file'''
    logging.info("Starting mapping with BWA")
    check_bwa_index(reference_file)
    output_file = output_path + '/' + sample_name
    logging.info("Creating output file: {}.sorted.bam".format(output_file))
    if len(fastq_files) == 1:
        bwacommand = ['bwa', 'mem', '-t', num_threads, reference_file, fastq_files[0]]
    if len(fastq_files) == 2:
        bwacommand = ['bwa', 'mem', '-t', num_threads, reference_file, fastq_files[0], fastq_files[1]]
    
    with open(output_file + '.sam', 'w') as g:
        p1 = subprocess.Popen(bwacommand, stdout=g)
    p1.communicate()
    p1.wait()
    pysam.view('-Sb', '-@', num_threads,  output_file + '.sam', '-o', output_file + '.bam', catch_stdout=False)
    
    pysam.sort('-@',  num_threads, output_file + '.bam', '-o', output_file + '.sorted.bam', catch_stdout=False)
    pysam.index(output_file + '.sorted.bam', catch_stdout=False)
    os.remove(output_file + '.sam')
    os.remove(output_file + '.bam')
    if remove_large_files:
        os.remove(fastq_files[0])
        if len(fastq_files)==2:
            os.remove(fastq_files[1])
    logging.info("Finished mapping")
    return(output_file + '.sorted.bam')


if __name__ == '__main__':
    args = parseArgs()
    args.output_path = check_output_directory(args.output_path)
    if args.read2 is None:
        fastq_files = [args.read1]
        mode = 'single'
    else:
        fastq_files = [args.read1, args.read2]
        mode = 'paired'

    if not args.sample_name:
        args.sample_name = get_sample_name(args.read1, mode)

    bamfile=run_mapping(args.num_threads, args.reference_file, fastq_files, args.output_path, args.sample_name, args.remove_large_files)
