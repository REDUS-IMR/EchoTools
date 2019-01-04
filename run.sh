#!/bin/sh

# Define LSSS API url
export LSSS_URL="http://localhost:8000"

# Define the location of the CES cruise data
export CRUISE_DATA_ROOT="/ces/cruise_data"

# Define the location of the NMD echosounder output structures
export NMD_QUALITY_ROOT="/data/tmp"

# Set output CSV files (containing the location of the LSSS related files) 
export CES_LSSS_CSV="CES-LSSS.csv"

# Scratch directory for the LSSS
export MAIN_SCRATCH_DIR="`pwd`/main"

# Set overwrite outputs
export OVERWRITE_OUTPUT=1

# Set to process raw as addition to processing from database (WARNING: Super slow!)
export PROCESS_RAW=1

## DO NOT MODIFY BELOW ##

# Create scratch if not exists
mkdir -p $MAIN_SCRATCH_DIR

# Traverse the required LSSS files (needs couple of hours to finish)
python EchoConvFindLSSSAll.py

# Do conversion
python EchoConvRun.py -i $CES_LSSS_CSV
