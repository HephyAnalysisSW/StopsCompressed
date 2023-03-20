import copy, os, sys
from RootTools.core.Sample import Sample 
import ROOT

# Logging
import logging
logger = logging.getLogger(__name__)

# Data directory
try:
    data_directory_ = sys.modules['__main__'].data_directory
except:
    from StopsCompressed.samples.default_locations import default_locations
    data_directory_ = default_locations.data_2016_data_directory 

# Take post processing directory if defined in main module
try:
  import sys
  postProcessing_directory_ = sys.modules['__main__'].postProcessing_directory
except:
  from StopsCompressed.samples.default_locations import default_locations
  postProcessing_directory_ = default_locations.data_2016_postProcessing_directory 


logger.info("Loading data samples from directory %s", os.path.join(data_directory_, postProcessing_directory_))

dirs = {}
for (run, version) in [('F',''),('G',''),('H','')]: 
    runTag = 'Run2016' + run + '_UL' + version
    dirs["MET_Run2016"       	 	+ run + version ] = ["MET_"	          + runTag ]

def merge(pd, totalRunName, listOfRuns):
    dirs[pd + '_' + totalRunName] = []
    for run in listOfRuns: dirs[pd + '_' + totalRunName].extend(dirs[pd + '_' + run])

for pd in ['MET']:
    merge(pd, 'Run2016FG', [ 'Run2016F', 'Run2016G'])
    merge(pd, 'Run2016',   ['Run2016FG', 'Run2016H'])

for key in dirs:
    dirs[key] = [ os.path.join( data_directory_, postProcessing_directory_, dir) for dir in dirs[key]]


def getSample(pd, runName, lumi):
    sample      = Sample.fromDirectory(name=(pd + '_' + runName), treeName="Events", texName=(pd + ' (' + runName + ')'), directory=dirs[pd + '_' + runName])
    sample.lumi = lumi
    return sample

#l_tot = (5.883+2.646+4.353+4.050+3.124+7.554+8.494+0.217) # old normtag

allSamples_Data25ns = []

MET_Run2016                	  = getSample('MET',       	  'Run2016',           (16.5)*1000)

allSamples_Data25ns += [MET_Run2016]

Run2016postVFP = Sample.combine("Run2016postVFP", [MET_Run2016], texName = "Run2016postVFP")
Run2016postVFP.lumi = (16.81)*1000
allSamples_Data25ns.append(Run2016postVFP)


for s in allSamples_Data25ns:
  s.color   = ROOT.kBlack
  s.isData  = True


