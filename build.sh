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

# Install packages one by one to better handle dependencies
pip install --no-cache-dir numpy==1.23.5
pip install --no-cache-dir pandas==1.5.3
pip install --no-cache-dir Flask==2.0.1
pip install --no-cache-dir yfinance==0.1.70
pip install --no-cache-dir prophet==1.1.1
pip install --no-cache-dir plotly==5.3.1
pip install --no-cache-dir gunicorn==20.1.0 