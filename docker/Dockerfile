################## BASE IMAGE ######################
FROM ubuntu:18.04

################## METADATA ######################
LABEL base.image="ubuntu:18.04"
LABEL version="1"
LABEL software="umierrorcorrect"
LABEL software.version="0.26"
LABEL about.summary="Umi error correct pipeline"
LABEL about.home="https://github.com/stahlberggroup/umierrorcorrect"
LABEL about.tags="Genomics"


# Update Ubuntu Software repository and install dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    make \
    curl \
    libbz2-dev \
    liblzma-dev \
    libz-dev \
    libxml2-dev \
    libcurl4-openssl-dev \
    libjpeg-dev \
    bzip2 \
    xz-utils \
    gcc \
    g++ \
    python3-dev \
    python3-pip \
    python3-setuptools \
    pigz \
    bwa && \
    pip3 install wheel && \
    pip3 install Cython && \
    pip3 install pysam && \
    pip3 install scipy && \
    pip3 install matplotlib && \
    pip3 install cutadapt && \
    pip3 install umierrorcorrect 


################## create folders ##################
#USER root
#RUN mkdir -p /srv/code && \
#    mkdir -p /srv/example && \
#    mkdir -p /srv/references
#
################## Install uec ##################

#RUN pip3 install /srv/code/v0.13.tar.gz
