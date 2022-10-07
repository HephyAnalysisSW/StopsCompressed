#!/bin/sh

##Test command:
python analysisPlots.py --era Run2016postVFP --reweightPU Central     --targetDir v_UL01 --small

## For submission over all eras
python analysisPlots.py --era Run2016preVFP --reweightPU Central --targetDir UL_v02  
python analysisPlots.py --era Run2016postVFP --reweightPU Central     --targetDir UL_v02 
python analysisPlots.py --era Run2017 --reweightPU Central     --targetDir UL_v02 
python analysisPlots.py --era Run2018 --reweightPU Central     --targetDir UL_v02 

## no preSelection cuts
#python analysisPlots.py --era Run2016 --reweightPU Central --targetDir lowPtEl_v01 --selection '(1)' --small 
## for submission of various eras
#submit --title "pl16APV" 'python analysisPlots.py --era Run2016preVFP --reweightPU Central --targetDir v_UL06'
#submit --title "pl16APV" 'python analysisPlots.py --era Run2016postVFP --reweightPU Central --targetDir v_UL06'
#submit --title "preSel16" 'python analysisPlots.py --era Run2016 --reweightPU Central --targetDir v_UL06'
#submit --title "preSel17" 'python analysisPlots.py --era Run2017 --reweightPU Central --targetDir v_UL12'
