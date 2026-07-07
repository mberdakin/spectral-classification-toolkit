#!/usr/bin/env bash

conda init bash

conda remove --yes --name ML-LIBS --all

conda create --yes --name ML-LIBS python=3.9

# Then: 
# conda activate ML-LIBS 
# pip install -r requirements.txt
