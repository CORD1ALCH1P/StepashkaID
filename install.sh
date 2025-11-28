#!/bin/bash

set -e

echo "=================================================="
echo "   StepashkaID — auto installation"
echo "=================================================="

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}packets updating + installing depends${NC}"
sudo apt update -y
sudo apt install -y \
    build-essential \
    cmake \
    git \
    libatlas-base-dev \
    libopenblas-dev \
    liblapack-dev \
    libjpeg-dev \
    zlib1g-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    ffmpeg \
    libglib2.0-0

echo -e "${GREEN}creating venv${NC}"
python3 -m venv .venv
source .venv/bin/activate

echo -e "${GREEN}Upgrading pip...${NC}"
pip install --upgrade pip setuptools wheel

echo -e "${GREEN}building dlib ...${NC}"
pip install --verbose dlib

echo -e "${GREEN}dep installing${NC}"
pip install -r requirements.txt

echo -e "${GREEN}creating known persons dir${NC}"
mkdir -p known_persons

echo ""
echo -e "${YELLOW}All set!${NC}"

chmod +x install.sh 2>/dev/null || true