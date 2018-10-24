#!/bin/sh

export LSSS_URL="http://localhost:8000"
export CRUISE_DATA_ROOT="/ces/cruise_data"
export NMD_QUALITY_ROOT="/data/workspace/quality"

export LSSSDB_CSV="LSSSdb.csv"
export CES_LSSS_CSV="CES-LSSS.csv"

export MAIN_SCRATCH_DIR="`pwd`/main"

export OVERWRITE_OUTPUT=1
export PROCESS_RAW=1

mkdir -p $MAIN_SCRATCH_DIR

findAcousticsLSSSdb.sh > $LSSSDB_CSV

python EchoConvFindLSSSRaw.py

python EchoConvRun.py -i $CES_LSSS_CSV
