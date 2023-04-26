#!/bin/sh -x
#SBATCH --time 06:00:00

export X509_USER_PROXY=$HOME/private/proxy
voms-proxy-info

./sync-files-to-scratch


