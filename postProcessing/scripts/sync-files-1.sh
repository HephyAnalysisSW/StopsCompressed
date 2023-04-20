#!/bin/bash -x

if [ -n $SLURM_JOB_ID ];  then
    SCRIPT_PATH=$(scontrol show job $SLURM_JOBID | awk -F= '/Command=/{print $2}')
else
    # otherwise: started with bash. Get the real location.
    SCRIPT_PATH=$(realpath $0)
fi
SCRIPT_DIR=$(dirname $SCRIPT_PATH)

export X509_USER_PROXY=$HOME/private/proxy
 
voms-proxy-info

$SCRIPT_DIR/sync-files-1
