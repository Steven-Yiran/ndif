FROM ubuntu:22.04

# Install base utilities
RUN apt-get update \
    && apt-get install -y build-essential \
    && apt-get install -y wget \
    && apt-get install -y python3-distutils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# CONDA ##################################################################

# Copy over environment file
COPY environment.yml .

# Install miniconda
ENV CONDA_DIR /opt/conda

# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH

# Install Miniforge for ARM64
RUN wget --quiet https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh -O ~/miniforge.sh \
    && /bin/bash ~/miniforge.sh -b -p /opt/conda \
    && rm ~/miniforge.sh \
    && conda env create --name service -f environment.yml 
###########################################################################