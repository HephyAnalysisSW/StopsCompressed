#!/bin/sh
#SBATCH --job-name a-plots
#SBATCH --time 06:00:00
#SBATCH --output analysis_plots-%j.log

##Test command:
#python analysisPlots.py --era Run2016postVFP --reweightPU Central     --targetDir v_UL01 --small

## For submission over all eras
eval $(scramv1 runtime -sh)
python analysisPlots.py --era Run2016preVFP  --reweightPU Central --targetDir UL_v01  
python analysisPlots.py --era Run2016postVFP --reweightPU Central     --targetDir UL_v01 
python analysisPlots.py --era Run2017        --reweightPU Central     --targetDir UL_v01 
python analysisPlots.py --era Run2018        --reweightPU Central     --targetDir UL_v01 

## no preSelection cuts
#python analysisPlots.py --era Run2016 --reweightPU Central --targetDir lowPtEl_v01 --selection '(1)' --small 
## for submission of various eras
#submit --title "pl16APV" 'python analysisPlots.py --era Run2016preVFP --reweightPU Central --targetDir v_UL06'
#submit --title "pl16APV" 'python analysisPlots.py --era Run2016postVFP --reweightPU Central --targetDir v_UL06'
#submit --title "preSel16" 'python analysisPlots.py --era Run2016 --reweightPU Central --targetDir v_UL06'
#submit --title "preSel17" 'python analysisPlots.py --era Run2017 --reweightPU Central --targetDir v_UL12'
