import copy, os, sys
from RootTools.core.Sample import Sample
import ROOT

# Logging
import logging
logger = logging.getLogger(__name__)

from StopsCompressed.samples.color import color

from StopsCompressed.samples.default_locations import default_locations
data_directory_ = default_locations.mc_2016_data_directory
#postProcessing_directory_ = default_locations.mc_2016_postProcessing_directory
postProcessing_directory_ = default_locations.signal_2016_postProcessing_directory

logger.info("Loading MC samples from directory %s", os.path.join(data_directory_, postProcessing_directory_))



dirs = {}
dirs['T2tt_mStop_500_mLSP_420']  = ['SMS_T2tt_mStop_500_mLSP_420']
dirs['T2tt_mStop_500_mLSP_450']  = ['SMS_T2tt_mStop_500_mLSP_450']
dirs['T2tt_mStop_500_mLSP_470']  = ['SMS_T2tt_mStop_500_mLSP_470']
dirs['T2tt_LL_mStop_300_mLSP_290']  = ['SMS_T2tt_LL_mStop_300_mLSP_290']
dirs['T2tt_LL_mStop_400_mLSP_380']  = ['SMS_T2tt_LL_mStop_400_mLSP_380']
dirs['T2tt_LL_mStop_350_mLSP_335']  = ['SMS_T2tt_LL_mStop_350_mLSP_335']

dirs['allDispSignal']   = dirs['T2tt_LL_mStop_300_mLSP_290'] + dirs['T2tt_LL_mStop_400_mLSP_380'] + dirs['T2tt_LL_mStop_350_mLSP_335']
dirs['allPromptSignal'] = dirs['T2tt_mStop_500_mLSP_420'] + dirs['T2tt_mStop_500_mLSP_450'] + dirs['T2tt_mStop_500_mLSP_470']
directories = { key : [ os.path.join( data_directory_, postProcessing_directory_, dir) for dir in dirs[key]] for key in dirs.keys()}

#

# FullSim signals
T2tt_500_420   	  = Sample.fromDirectory(name="T2tt_500_420",    treeName="Events", isData=False, color=color.DY,     texName="T2tt(500,420)",     directory=directories['T2tt_mStop_500_mLSP_420'])
T2tt_500_450   	  = Sample.fromDirectory(name="T2tt_500_450",    treeName="Events", isData=False, color=color.DY,     texName="T2tt(500,450)",     directory=directories['T2tt_mStop_500_mLSP_450'])
T2tt_500_470   	  = Sample.fromDirectory(name="T2tt_500_470",    treeName="Events", isData=False, color=color.DY,     texName="T2tt(500,470)",     directory=directories['T2tt_mStop_500_mLSP_470'])
T2tt_LL_300_290   = Sample.fromDirectory(name="T2tt_LL_300_290",    treeName="Events", isData=False, color=color.DY,     texName="T2tt_LL(300,290)",     directory=directories['T2tt_LL_mStop_300_mLSP_290'])
T2tt_LL_350_335   = Sample.fromDirectory(name="T2tt_LL_350_335",    treeName="Events", isData=False, color=color.DY,     texName="T2tt_LL(350,335)",     directory=directories['T2tt_LL_mStop_350_mLSP_335'])
T2tt_LL_400_380   = Sample.fromDirectory(name="T2tt_LL_400_380",    treeName="Events", isData=False, color=color.DY,     texName="T2tt_LL(400,380)",     directory=directories['T2tt_LL_mStop_400_mLSP_380'])
T2tt_allDispSignal 	  =  Sample.fromDirectory(name=" T2tt_Disp_Signal", treeName="Events", isData=False, color=color.allDispSignal,     texName= "FullSim_T2tt_Disp Signals"	,	directory=directories['allDispSignal'])
T2tt_allPromptSignal 	  =  Sample.fromDirectory(name=" T2tt_Prompt_Signal", treeName="Events", isData=False, color=color.allSignal,     texName= "FullSim_T2tt Prompt_Signals"	,	directory=directories['allPromptSignal'])


signals_T2tt = [
    T2tt_500_420,
    T2tt_500_450,
    T2tt_500_470,
    T2tt_LL_300_290,
    T2tt_LL_400_380,
    T2tt_LL_350_335,
]

for s in signals_T2tt:
    if s.name.startswith('T2tt_LL_'):
	    mStop, mNeu = s.name.replace('T2tt_LL_','').split('_')
    else:
	    mStop, mNeu = s.name.replace('T2tt_','').split('_')
    s.mStop = int(mStop)
    s.mNeu = int(mNeu)
    s.isFastSim = False

