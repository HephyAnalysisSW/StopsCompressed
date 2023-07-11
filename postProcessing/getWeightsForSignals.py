'''
Get all the needed weights and norms for SUSY signals. Usage like
python getWeightsForSignals.py --year 2017 --sample SMS_T2tt_mStop_250to350 --ppSamplePath /afs/hephy.at/data/cms01/nanoTuples/stops_2017_nano_v0p12/dilep/

/afs/hephy.at/data/dspitzbart03/nanoTuples/stops_2017_nano_v0p7/inclusive/SMS_T2tt_mStop_400to1200/
'''

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import sys
import os
import copy
import random
import subprocess
import datetime
import shutil
import uuid

from array import array
from operator import mul
from math import sqrt, atan2, sin, cos

# RootTools
from RootTools.core.standard import *

# User specific
import StopsCompressed.Tools.user as user
# top pt reweighting
#from StopsDilepton.tools.topPtReweighting import getUnscaledTopPairPtReweightungFunction, getTopPtDrawString, getTopPtsForReweighting

# use a cacheDir that's read/writable for all of us
cacheDir = "/groups/hephy/cms/priya.hussain/StopsCompressed/signals/caches/UL/"
#cacheDir = "/mnt/hephy/cms/priya.hussain/StopsCompressed/signals/caches/modified"
#cacheDir = "/afs/hephy.at/data/cms08/StopsCompressed/signals/caches/"

def get_parser():
    ''' Argument parser for post-processing module.
    '''
    import argparse
    argParser = argparse.ArgumentParser(description = "Argument parser for cmgPostProcessing")

    argParser.add_argument('--logLevel',        action='store',         nargs='?',  choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'],   default='INFO', help="Log level for logging" )
    argParser.add_argument('--samples',         action='store',         nargs='*',  type=str, default=['TTZToLLNuNu_ext'],                  help="List of samples to be post-processed, given as CMG component name" )
    argParser.add_argument('--ppSamplePath',    action='store',         nargs='*',  type=str, default=None,                  help="List of samples to be post-processed, given as CMG component name" )
    argParser.add_argument('--year',            action='store',                     type=str,                                               help="Which year?" )
    argParser.add_argument('--overwrite',       action='store_true',                help="Overwrite ISR norm cache?" )

    return argParser

options = get_parser().parse_args()

# Logging
import StopsCompressed.Tools.logger as _logger
logFile = None
logger  = _logger.get_logger(options.logLevel, logFile = logFile)


import RootTools.core.logger as _logger_rt
logger_rt = _logger_rt.get_logger(options.logLevel, logFile = None )
cacheDir += "%s/"%options.year
## First, get the normalization per masspoint (done on nanoAOD tuples)

if options.year == 'UL2016':
    #from Samples.nanoAOD.Summer16_private_legacy_v1 import allSamples as bkgSamples
    #from Samples.nanoAOD.Summer16_private_legacy_v1 import compSUSY as signalSamples
    #from Samples.nanoAOD.Run2016_17Jul2018_private  import allSamples as dataSamples
    #allSamples = bkgSamples + dataSamples + signalSamples
    from Samples.nanoAOD.UL16v9_private import compSUSY as signalSamples
 
    allSamples = signalSamples
 
elif options.year == "UL2016_preVFP":
    from Samples.nanoAOD.UL16APVv9_private               import compSUSY as signalSamples
    allSamples = signalSamples

elif options.year == "UL2017":
    from Samples.nanoAOD.UL17v9_private                  import compSUSY as signalSamples
    allSamples = signalSamples

elif options.year == "UL2018":
    from Samples.nanoAOD.UL18v9_private                  import compSUSY as signalSamples
    allSamples = signalSamples
else:
    raise NotImplementedError


samples = []
for selectedSamples in options.samples:
    for sample in allSamples:
        if selectedSamples == sample.name:
            samples.append(sample)

if len(samples)==0:
    logger.info( "No samples found. Was looking for %s. Exiting" % options.samples )
    sys.exit(-1)

targetLumi = 1000 #pb-1 Which lumi to normalize to

from StopsCompressed.samples.helpers import getT2ttSignalWeight

logger.info("Getting the signal weights for sample %s", options.samples[0])

signalWeight = getT2ttSignalWeight( samples[0], lumi = targetLumi, cacheDir = cacheDir)
masspoints = signalWeight.keys()

## now, if we already have a post-processed version of the samples, also get the ISR norm for each masspoint

if options.ppSamplePath:
    import glob
    files = '%s/%s/*.root'%(options.ppSamplePath[0], options.samples[0])
    fileList = [ f for f in  glob.glob(files) if not f.count('signalCounts') ]
    
    sample = Sample.fromFiles(samples[0].name, fileList)

    logger.info("Now extracting the ISR normalization factors.")

    from StopsCompressed.samples.helpers import getT2ttISRNorm

    norm = getT2ttISRNorm(sample, masspoints[0][0], masspoints[0][1], masspoints, options.year, signal=sample.name, cacheDir=cacheDir, fillCache=True, overwrite=options.overwrite)
    logger.info("Got the following norms for the masspoints (mStop, mLSP)")
    for masspoint in sorted(masspoints):
        norm = getT2ttISRNorm(sample, masspoint[0], masspoint[1], masspoints, options.year, signal=sample.name, cacheDir=cacheDir)
        logger.info("%s, %s: %s", masspoint[0], masspoint[1], norm)
    logger.info("Done.")


