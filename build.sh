#!/usr/bin/env bash

# Install system dependencies
apt-get update
apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    python3-venv \
    gcc \
    g++ \
    gfortran \
    libopenblas-dev

# Upgrade pip
python -m pip install --upgrade pip

# Install Python packages
pip install --no-cache-dir -r requirements.txt 