#!/bin/sh

#python nanoPostProcessing.py  --skim singleLep --triggerSelection --year 2018 --processingEra stops_2018_nano_v1  --overwrite --sample DoubleMuon_Run2018A_17Sep2018 #SPLIT30
#python nanoPostProcessing.py  --skim singleLep --triggerSelection --year 2018 --processingEra stops_2018_nano_v1  --overwrite --sample DoubleMuon_Run2018B_17Sep2018 #SPLIT30
#python nanoPostProcessing.py  --skim singleLep --triggerSelection --year 2018 --processingEra stops_2018_nano_v1  --overwrite --sample DoubleMuon_Run2018C_17Sep2018 #SPLIT30
#python nanoPostProcessing.py  --skim singleLep --triggerSelection --year 2018 --processingEra stops_2018_nano_v1  --overwrite --sample DoubleMuon_Run2018D_17Sep2018 #SPLIT30

#python nanoPostProcessing.py  --skim singleLep --triggerSelection --year 2018 --processingEra stops_2018_nano_v1  --overwrite --sample MuonEG_Run2018A_17Sep2018 #SPLIT30
#python nanoPostProcessing.py  --skim singleLep --triggerSelection --year 2018 --processingEra stops_2018_nano_v1  --overwrite --sample MuonEG_Run2018B_17Sep2018 #SPLIT30
#python nanoPostProcessing.py  --skim singleLep --triggerSelection --year 2018 --processingEra stops_2018_nano_v1  --overwrite --sample MuonEG_Run2018C_17Sep2018 #SPLIT30
#python nanoPostProcessing.py  --skim singleLep --triggerSelection --year 2018 --processingEra stops_2018_nano_v1  --overwrite --sample MuonEG_Run2018D_17Sep2018 #SPLIT30

#python nanoPostProcessing.py  --skim singleLep --triggerSelection --year 2018 --processingEra stops_2018_nano_v1  --overwrite --sample EGamma_Run2018A_17Sep2018 #SPLIT30
#python nanoPostProcessing.py  --skim singleLep --triggerSelection --year 2018 --processingEra stops_2018_nano_v1  --overwrite --sample EGamma_Run2018B_17Sep2018 #SPLIT30
#python nanoPostProcessing.py  --skim singleLep --triggerSelection --year 2018 --processingEra stops_2018_nano_v1  --overwrite --sample EGamma_Run2018C_17Sep2018 #SPLIT30
#python nanoPostProcessing.py  --skim singleLep --triggerSelection --year 2018 --processingEra stops_2018_nano_v1  --overwrite --sample EGamma_Run2018D_22Jan2019 #SPLIT30

#python nanoPostProcessing.py  --skim singleLep --triggerSelection --year 2018 --processingEra stops_2018_nano_v1  --overwrite --sample SingleMuon_Run2018A_17Sep2018 #SPLIT30
#python nanoPostProcessing.py  --skim singleLep --triggerSelection --year 2018 --processingEra stops_2018_nano_v1  --overwrite --sample SingleMuon_Run2018B_17Sep2018 #SPLIT30
#python nanoPostProcessing.py  --skim singleLep --triggerSelection --year 2018 --processingEra stops_2018_nano_v1  --overwrite --sample SingleMuon_Run2018C_17Sep2018 #SPLIT30
#python nanoPostProcessing.py  --skim singleLep --triggerSelection --year 2018 --processingEra stops_2018_nano_v1  --overwrite --sample SingleMuon_Run2018D_22Jan2019 #SPLIT30

#python nanoPostProcessing.py  --skim singleLep --year 2018 --processingEra compstops_2018_nano_v1  --sample TTSingleLep_pow #SPLIT30
python nanoPostProcessing.py  --skim singleLep --year 2018 --processingEra compstops_2018_nano_v1  --sample DisplacedStops_mStop_250_ctau_0p01 --overwrite #SPLIT10
#python nanoPostProcessing.py  --skim singleLep --year 2018 --processingEra compstops_2018_nano_v1  --sample DisplacedStops_mStop_250_ctau_0p01 --small --keepAllJets
