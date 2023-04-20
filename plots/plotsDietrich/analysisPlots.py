'''
Analysis script for standard plots
'''
#
# Standard imports and batch mode

import ROOT, os
ROOT.gROOT.SetBatch(True)
import itertools
import copy
import array
import operator

from math   import pi, sqrt, sin, cos, atan2, log, isnan
from RootTools.core.standard import *
from StopsCompressed.Tools.user             import plot_directory
from Analysis.Tools.metFilters              import getFilterCut
from StopsCompressed.Tools.cutInterpreter   import cutInterpreter
#from Analysis.Tools.puProfileCache import *
from StopsCompressed.Tools.helpers           import deltaR, deltaPhi,ptRatio
from StopsCompressed.Tools.objectSelection   import muonSelector, eleSelector,  getGoodMuons, getGoodElectrons, getGoodTaus, getAllJets
#read gen filter efficicency
from StopsCompressed.Tools.genFilter import genFilter
#
# Arguments
#
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',           		action='store',      default='INFO',          nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--era',                		action='store',      default="Run2018",  	type=str )
argParser.add_argument('--eos',                		action='store_true', 			help='change sample directory to location eos directory' )
argParser.add_argument('--small',              		action='store_true', 			help='Run only on a small subset of the data?')#, default = True)
argParser.add_argument('--targetDir',          		action='store',      default='v_UL01')
#argParser.add_argument('--selection',          		action='store',      default='nISRJets1p-ntau0-lepSel-dphimetjet0to0p5-jet3Veto-met200-ht300')
#argParser.add_argument('--selection',          		action='store',      default='nISRJets1p-ntau0-lepSel-deltaPhiMetJetsInv-jet3Veto-met200-ht300')
#argParser.add_argument('--selection',          		action='store',      default='nISRJets1p-ntau0-lepSel-dphimetjet0p5-jet3Veto-met200-ht300')
#argParser.add_argument('--selection',          		action='store',      default='nISRJets1p-ntau0-lepSel-deltaPhiJets-jet3Veto-met200-ht300-isPrompt')
argParser.add_argument('--selection',          		action='store',      default='nISRJets1p-ntau0-lepSel-deltaPhiJets-jet3Veto-met200-ht300-isFake')
#argParser.add_argument('--selection',          		action='store',      default='nISRJets1p-ntau0-lepSel-deltaPhiJets-jet3Veto-met200-ht300-isGenMatched')
#argParser.add_argument('--selection',          		action='store',      default='nISRJets1p-ntau0-lepSel-deltaPhiJets-jet3Veto-met200-ht300')
argParser.add_argument('--reweightPU',         		action='store',      default=None, 		  choices=['VDown', 'Down', 'Central', 'Up', 'VUp', 'VVUp'])
argParser.add_argument('--badMuonFilters',     		action='store',      default="Summer2016",  	  help="Which bad muon filters" )
argParser.add_argument('--noBadPFMuonFilter',           action='store_true', default=False)
argParser.add_argument('--noBadChargedCandidateFilter', action='store_true', default=True)
argParser.add_argument('--preHEM',             action='store_true', default=False)
argParser.add_argument('--postHEM',            action='store_true', default=False)

args = argParser.parse_args()

#
# Logger
#
import RootTools.core.logger as _logger_rt
logger = _logger_rt.get_logger(args.logLevel, logFile = None)

if args.small:                        args.targetDir += "_small"
if args.reweightPU:                   args.targetDir += "_%s"%args.reweightPU
if args.preHEM:                       args.targetDir += "_preHEM"
if args.postHEM:                       args.targetDir += "_postHEM"

#
# Make samples, will be searched for in the postProcessing directory
#
from Analysis.Tools.puReweighting import getReweightingFunction

if  "2016" in args.era:
    year = 2016
elif "2017" in args.era:
    year = 2017
elif "2018" in args.era:
    year = 2018
logger.info( "Working in year %i", year )
if args.eos and "2016" in args.era:
    data_directory = "/eos/cms/store/group/phys_susy/hephy/"
    postProcessing_directory = "stopsCompressed/nanoTuples/"
    from StopsCompressed.samples.nanoTuples_Summer16_postProcessed import *
    samples = [TTLep_pow_16 , TTSingleLep_pow_16]
    
    
elif args.era == "Run2016preVFP" and not args.eos:
    from StopsCompressed.samples.nanoTuples_UL16APV_postProcessed import *
    samples = [WJetsToLNu_HT_16APV, Top_pow_16APV, singleTop_16APV, ZInv_16APV, DY_HT_LO_16APV, QCD_HT_16APV, VV_16APV, TTX_16APV]
    from StopsCompressed.samples.nanoTuples_RunUL16APV_postProcessed import *
    data_sample = Run2016preVFP
    from StopsCompressed.samples.nanoTuples_UL16APV_FullSimSignal_postProcessed import *
    #from StopsCompressed.samples.nanoTuples_FastSim_Summer16_postProcessed import *
    #signals = [T2tt_375_365,T2tt_500_470]
    #signals = [T2tt_375_365,T2tt_500_470, T2tt_500_420 ]
    signals = [T2tt_500_420, T2tt_500_470]
elif args.era == "Run2016postVFP" and not args.eos:
    from StopsCompressed.samples.nanoTuples_UL16_postProcessed import *
    #samples = [WJetsToLNu_HT_16, TTJets_1l_16, singleTop_16, ZInv_16, DY_HT_LO_16, QCD_HT_16, VV_16, TTX_16]
    #samples = [WJetsToLNu_HT_16, Top_pow_16, singleTop_16, ZInv_16, DY_HT_LO_16, QCD_HT_16, VV_16, TTX_16]
    #samples = [WJetsToLNu_HT_16]
    samples = [WJetsToLNu_HT_16, Top_pow_16, singleTop_16, ZInv_16, DY_HT_LO_16,QCD_HT_16, VV_16, TTX_16]
    from StopsCompressed.samples.nanoTuples_RunUL16_postProcessed import *
    data_sample = Run2016postVFP
    from StopsCompressed.samples.nanoTuples_UL16_FullSimSignal_postProcessed import *
    signals = [T2tt_500_420, T2tt_500_470, T2tt_LL_300_290, T2tt_LL_400_380, T2tt_LL_350_335]
    #from StopsCompressed.samples.nanoTuples_FastSim_Summer16_postProcessed import *
    #signals = [T2tt_500_420, T2tt_500_470]

    #if args.reweightPU:
    #	    nTrueInt_puRW = getReweightingFunction(data="PU_2016_35920_XSec%s"%args.reweightPU, mc="Summer16")
elif  args.era == "Run2016" and not args.eos:
    from StopsCompressed.samples.nanoTuples_UL16_36fb_postProcessed_v2 import *
    from StopsCompressed.samples.nanoTuples_UL16_36fb_FullSimSignal_postProcessed import *
    #samples = [WJetsToLNu_HT_16, Top_pow_16, singleTop_16, ZInv_16, DY_HT_M50_LO_16, QCD_HT_16, VV_16, WWToLNuQQ_16, TTX_16]
    samples = [WJetsToLNu_HT_16, Top_pow_16, singleTop_16, ZInv_16, DY_HT_LO_16, QCD_HT_16, VV_16, TTX_16]
    #samples = [QCD_HT_16]
    #samples = [WJetsToLNu_HT_16, Top_pow_16, singleTop_16, ZInv_16, DY_HT_M50_LO_16, QCD_HT_16, TTX_16]
    data_sample = RunUL16_36fb
    signals = [T2tt_500_470, T2tt_500_420]
    #signals = [T2tt_500_420, T2tt_500_490]
elif "2017" in args.era and not args.eos:
    from StopsCompressed.samples.nanoTuples_UL17_postProcessed import *
    #samples = [WJetsToLNu_HT_17, Top_pow_17, singleTop_17, ZInv_17, DY_HT_LO_17,QCD_Ele_17,QCD_Mu_17, VV_17, TTX_17]
    #samples = [WJetsToLNu_HT_17, Top_pow_17, singleTop_17, ZInv_17, DY_HT_LO_17, VV_17, TTX_17]
    samples = [WJetsToLNu_HT_17, Top_pow_17, singleTop_17, ZInv_17, DY_HT_LO_17, QCD_HT_17, VV_17, TTX_17]
    #from StopsCompressed.samples.nanoTuples_Run2017_14Dec2018_postProcessed import *
    from StopsCompressed.samples.nanoTuples_RunUL17_postProcessed import *
    data_sample = Run2017
    from StopsCompressed.samples.nanoTuples_UL17_FullSimSignal_postProcessed import *
    signals = [T2tt_500_420, T2tt_500_470]
    #if args.reweightPU:
	    # need sample based weights
    #	    pass
elif "2018" in args.era and not args.eos:
    from StopsCompressed.samples.nanoTuples_UL18_postProcessed import *
    #samples =[WJetsToLNu_HT_18, Top_pow_18, singleTop_18, ZInv_18, DY_HT_LO_18, QCD_Ele_18, QCD_Mu_18, VV_18, TTX_18]
    #samples =[WJetsToLNu_HT_18, Top_pow_18, singleTop_18, ZInv_18, DY_HT_LO_18, VV_18, TTX_18]
    samples =[WJetsToLNu_HT_18, Top_pow_18, singleTop_18, ZInv_18, DY_HT_LO_18, QCD_HT_18, VV_18, TTX_18]
    from StopsCompressed.samples.nanoTuples_RunUL18_postProcessed import *
    data_sample = Run2018
    from StopsCompressed.samples.nanoTuples_UL18_FullSimSignal_postProcessed import *
    signals = [T2tt_500_420, T2tt_500_470]
    #if args.reweightPU:
	#    nTrueInt_puRW = getReweightingFunction(data="PU_2018_58830_XSec%s"%args.reweightPU, mc="Autumn18")
if args.era != "Run2016" and not args.eos:
	try:
	    data_sample = eval(args.era)
	except Exception as e:
	    logger.error( "Didn't find %s", args.era )
	    raise e


# Text on the plots
#
tex = ROOT.TLatex()
tex.SetNDC()
tex.SetTextSize(0.04)
tex.SetTextAlign(11) # align right
lumi_scale = 35.9

def drawObjects( plotData, dataMCScale):
    lines = [
      (0.15, 0.95, 'CMS Preliminary' if plotData else 'CMS Simulation'), 
      (0.45, 0.95, ' L=%3.1f fb{}^{-1}(13 TeV) Scale %3.2f'% ( lumi_scale , dataMCScale) )
      #(0.45, 0.95, ' (13 TeV) Scale %3.2f'% ( dataMCScale) )
      #(0.15, 0.95, ' L=%3.1f fb{}^{-1}(13 TeV) Scale %3.2f Integral %3.2f'% ( lumi_scale , dataMCScale, mcIntegral) )
      #(0.15, 0.95, 'Scale %3.2f MCIntegral %3.2f DataIntegral %3.2f'% ( dataMCScale, mcIntegral, mcIntegral) )
    ]
    return [tex.DrawLatex(*l) for l in lines] 

def drawPlots(plots,mode, dataMCScale):
  for log in [False, True]:
    
    #plot_directory_ = os.path.join(plot_directory, 'analysisPlots','looseDxy' ,args.targetDir, args.era ,mode +("log" if log else ""), args.selection)
    plot_directory_ = os.path.join(plot_directory, 'analysisPlots','HInoDxyDz' ,args.targetDir, args.era ,mode +("log" if log else ""), args.selection)
    for plot in plots:
      #print "data?? : ", plot.histos[1], "mc:?? ", plot.histos[0]
      #if not max(l[0].GetMaximum() for l in plot.histos): continue # Empty plot
#      for l in plot.histos:
#	if len(l)>1: print "samples list in plot histo", [ l[x].GetName() for x in range(len(l))]
#	
#	if len(l)>1: 
#		mc_integral=  sum([ l[x].Integral() for x in range(len(l))]) 
#		print "integral: ", mc_integral
#      print l[0].GetName()
#      print "integral: ", l[0].Integral()

      
      _drawObjects = []
      plotting.draw(plot,
        plot_directory = plot_directory_,
	#ratio = {'yRange':(0.1,1.9)},
        ratio = None,
        logX = False, logY = log, sorting = False,
        yRange = (0.03, "auto") if log else (0.001, "auto"),
        scaling = {},
        legend = ( (0.18,0.88-0.03*sum(map(len, plot.histos)),0.9,0.88), 2),
        drawObjects = drawObjects( True, dataMCScale) + _drawObjects,
        copyIndexPHP = True, extensions = ["png","pdf", "root"],
      )

# Read variables and sequences
read_variables = [
            "weight/F", "l1_pt/F", "l1_eta/F" , "l1_phi/F", "l1_pdgId/I", "l1_muIndex/I", "reweightHEM/F","l1_miniRelIso/F", "l1_relIso03/F", "nlep/I",
	    "lep[pt/F, eta/F, phi/F]",
            "JetGood[pt/F, eta/F, phi/F, genPt/F]", 
            "Jet[pt/F, eta/F, phi/F, jetId/I]", 
            "met_pt/F", "met_phi/F","CT1/F", "HT/F","mt/F", 'l1_dxy/F', 'l1_dz/F', 'l1_dzErr/F', 'l1_dxyErr/F', 'dphij0j1/F','ISRJets_pt/F', 'nISRJets/I','nSoftBJets/I','nHardBJets/I', "nBTag/I", "nJetGood/I", "PV_npvsGood/I","event/I","run/I", "Flag_BadPFMuonDzFilter/O"]
read_variables += [
            "nMuon/I","nElectron/I","nJet/I", "dPhiMetJet/F", "metJet/I",
            "Muon[dxy/F,dxyErr/F,dz/F,dzErr/F,eta/F,ip3d/F,jetRelIso/F,mass/F,miniPFRelIso_all/F,miniPFRelIso_chg/F,pfRelIso03_all/F,pfRelIso03_chg/F,pfRelIso04_all/F,phi/F,pt/F,ptErr/F,segmentComp/F,sip3d/F,mvaTTH/F,charge/I,jetIdx/I,nStations/I,nTrackerLayers/I,pdgId/I,tightCharge/I,highPtId/b,inTimeMuon/O,isGlobal/O,isPFcand/O,isTracker/O,mediumId/O,mediumPromptId/O,miniIsoId/b,multiIsoId/b,mvaId/b,pfIsoId/b,softId/O,softMvaId/O,tightId/O,tkIsoId/b,triggerIdLoose/O]",
	    "LowPtElectron[pt/F]",
            ]
#for s in samples:
#    s.read_variables = ["genWeight/F",'reweightPU/F', 'Pileup_nTrueInt/F','reweightBTag_SF/F', 'GenMET_pt/F', 'GenMET_phi/F', 'Muon[genPartIdx/I,genPartFlav/b]', "GenPart[pt/F,eta/F,phi/F]", "nGenPart/I"]

#genfilter efficiency
genFilter = genFilter(year=year)


sequence = []
def lepLooseDxy(event, sample): 
	event.l1_abs_dxy = abs(event.l1_dxy)
	event.l1_abs_dz  = abs(event.l1_dz)
	event.l1_dxySig  = event.l1_abs_dxy / event.l1_dxyErr
	event.l1_dzSig  = event.l1_abs_dz / event.l1_dzErr
sequence.append (lepLooseDxy)


def mtwithdphi(event, sample):
	event.mtmod = float('nan')
	if deltaPhi(event.l1_phi ,event.met_phi) < 1.7: 
		event.mtmod            = sqrt (2 * event.l1_pt * event.met_pt * (1 - cos(event.l1_phi - event.met_phi) ) )

def muonSelecion (event, sample):
	#event.l1_nTrackerLayers = -1
	#event.l1_nStations 	= -1 
	#event.l1_segmentComp	= float('nan')
	#event.l1_isGlobal	= False
	#if sample.isData:
	#	event.l1_muIndex = -1
	#	for i in range(event.nMuon):
	#		if event.l1_pt==event.Muon_pt[i]:
	#			event.l1_muIndex = i
	#print "GenPart length: ", event.nGenPart
	#if abs(event.l1_pdgId)==13 and event.l1_muIndex>=0 and sample.isData != True:
	if abs(event.l1_pdgId)==13 and event.l1_muIndex>=0:
		event.l1_nTrackerLayers = event.Muon_nTrackerLayers[event.l1_muIndex]
		event.l1_nStations 	= event.Muon_nStations[event.l1_muIndex]
		event.l1_segmentComp 	= event.Muon_segmentComp[event.l1_muIndex]
		#print "muIndex: ", event.l1_muIndex
		event.l1_isGlobal 	= event.Muon_isGlobal[event.l1_muIndex]
		event.l1_isPF 	  	= event.Muon_isPFcand[event.l1_muIndex]
		event.l1_isTrackr 	= event.Muon_isTracker[event.l1_muIndex]
		#print "event.Muon_isGlobal: ", event.Muon_isGlobal[event.l1_muIndex]
	else:
		event.l1_nTrackerLayers = -1
		event.l1_nStations 	= -1
		event.l1_segmentComp	= -999
		event.l1_isGlobal	= -1 
		event.l1_isPF		= -1 
		event.l1_isTrackr	= -1
sequence.append(muonSelecion)

def dphiMetJet( event, sample):
	#event.dPhi = -1
	#if event.nJetGood < 2:
	#	event.dPhi = -1
	#	#print "here for < 2 jets"
	#else:
	event.dPhiMetJets = []
	for ij in range(event.nJetGood):
		#print "length of jets: ", event.nJetGood, ij
		event.dPhiMetJets.append(deltaPhi(event.met_phi, event.JetGood_phi[ij])) 
	#print "deltaphis of met with all jets > 2: ", event.dPhiMetJet
	#print "minimum angle selected for a jet:", min(event.dPhiMetJet)
	event.dPhi = min(event.dPhiMetJets)
	#print event.dPhi, "stored dPhi value"
#sequence.append(dphiMetJet)

def lowPTEl(event,sample):
#	print "low pt electron: ", event.LowPtElectron_pt[0], type(event.LowPtElectron_pt)

	if isnan(event.LowPtElectron_pt[0]) :
		event.el_pt = -999
	else:
		event.el_pt = event.LowPtElectron_pt[0]
sequence.append(lowPTEl)

def delR(event,sample):
	event.dR = float("nan")
	event.dR = sqrt(((deltaPhi(event.l1_phi,event.JetGood_phi[0])**2) + ((event.l1_eta - event.JetGood_eta[0])**2)))
#sequence.append(delR)


def jetToLeptonRatio (event, sample):
	event.cleanJets_pt  = float ('nan')
	event.cleanJets_eta = float ('nan')
	event.cleanJets_phi  = float ('nan')
	Electrons =  getGoodElectrons(event, ele_selector = eleSelector("hybridIso", year=year))	
	Muons =  getGoodMuons(event, mu_selector = muonSelector("hybridIso", year=year))	
	leptons = Electrons + Muons
	leptons.sort(key = lambda p:-p['pt'])
	jets = getAllJets(event, leptons, ptCut=30, absEtaCut=2.4,jetVars= ['pt','eta','phi', 'jetId'] , jetCollections=["Jet"], idVar='jetId')
	event.nJetsClean = len(jets)
	if event.nJetsClean >0:
		event.cleanJets_pt  = jets[0]['pt']
		event.cleanJets_eta = jets[0]['eta']
		event.cleanJets_phi = jets[0]['phi']
#	for i,jet in enumerate(jets):
#		event.cleanJets_pt  = jet['pt']
#		event.cleanJets_eta = jet['eta']
#		event.cleanJets_phi = jet['phi']

#def make_weight (event, sample):
#	print event.weight, event.reweightHEM
#sequence.append (make_weight)


def getLeptonSelection( mode ):
	if   mode == 'mu': return "abs(l1_pdgId)==13"
	elif mode == 'e' : return "abs(l1_pdgId)==11"


yields   = {}
allPlots = {}
allModes = ['mu','e']
for index, mode in enumerate(allModes):
	yields[mode] = {}
	if args.era == "Run2016":
		data_sample.setSelectionString([getFilterCut(isData=True, year=year, skipBadPFMuon=args.noBadPFMuonFilter, skipBadChargedCandidate=args.noBadChargedCandidateFilter, skipVertexFilter = True), getLeptonSelection(mode)])
		lumi_scale                 = data_sample.lumi/1000
		#print "lumi for each set: ", lumi_scale
		data_sample.scale          = 1.
		data_sample.style          = styles.errorStyle(ROOT.kBlack)
		data_sample.name 	   = "data"
	else:
		#print "data: ", data_sample.name
		data_sample.setSelectionString([getFilterCut(isData=True, year=year, skipBadPFMuon=args.noBadPFMuonFilter, skipBadChargedCandidate=args.noBadChargedCandidateFilter, skipVertexFilter = True), getLeptonSelection(mode)])
		if args.preHEM:
			data_sample.addSelectionString("run<319077")
		if args.postHEM:
			data_sample.addSelectionString("run>=319077")
		lumi_scale                 = data_sample.lumi/1000
		#print "lumi: ", lumi_scale
		if args.preHEM:   lumi_scale *= 0.37
		if args.postHEM:  lumi_scale *= 0.63
		data_sample.scale          = 1.
		data_sample.style          = styles.errorStyle(ROOT.kBlack)
		data_sample.name 	   = "data"
	if signals:
	    T2tt_500_470.color = ROOT.kPink+6
	    T2tt_500_420.color = ROOT.kCyan+2
	    # T2tt_LL_300_290.color = ROOT.kYellow
	    # T2tt_LL_400_380.color = ROOT.kRed
	    # T2tt_LL_350_335.color = ROOT.kBlue
	    #T2tt_375_365.color = ROOT.kAzure+1
	
	weight_ = lambda event, sample: event.weight*event.reweightHEM

	for sample in samples + signals:

		sample.read_variables = ['reweightPU/F', 'Pileup_nTrueInt/F','reweightLeptonSF/F', 'reweightBTag_SF/F','reweightL1Prefire/F','reweightnISR/F', 'reweightwPt/F',]
		sample.read_variables += ['reweightPU%s/F'%args.reweightPU if args.reweightPU != "Central" else "reweightPU/F"]
		#pu_getter = operator.attrgetter('reweightPU' if args.reweightPU=='Central' else "reweightPU%s"%args.reweightPU)
		if args.era == "Run2016":
			if "T2tt" in sample.name:
				mStop= int(sample.name.split('_')[1])
				mNeu= int(sample.name.split('_')[2])
				#print sample.name.split('_')[1], sample.name.split('_')[2]
				genEff = genFilter.getEff(mStop,mNeu)
				#print "signal name: ",sample.name, "mStop: ", mStop, "mNeu: ", mNeu,"genEff: " ,genEff
				#sample.read_variables += [ 'reweight_nISR/F']
				sample.read_variables += [ 'year/I', 'stop1_Lxy/F', 'stop1_dt/F']
				sample.weight         = lambda event, sample: event.reweightPU * event.reweightBTag_SF * event.reweightL1Prefire * event.reweightwPt * event.reweightLeptonSF * genEff * lumi_year[event.year]/1000
				#sample.weight         = lambda event, sample: event.reweightPU * event.reweightBTag_SF * event.reweightL1Prefire  * event.reweightLeptonSF 
				sample.style = styles.errorStyle( color=sample.color, markerSize = 0.6)
				sample.setSelectionString([getFilterCut(isData=False, year=year, skipBadPFMuon=args.noBadPFMuonFilter, skipBadChargedCandidate=args.noBadChargedCandidateFilter, skipVertexFilter = True), getLeptonSelection(mode)])
				#sample.scale = lumi_scale
			##elif sample.name == "WWToLNuQQ":
			#elif sample.name == "VV":
			#	print sample.name, " using lumi %s"%lumi_scale
			#	sample.weight         = lambda event, sample: event.reweightPU * event.reweightBTag_SF * event.reweightL1Prefire * event.reweightLeptonSF * event.reweightwPt
			#	sample.scale = lumi_scale 
			#	sample.setSelectionString([getFilterCut(isData=False, year=year, skipBadPFMuon=args.noBadPFMuonFilter, skipBadChargedCandidate=args.noBadChargedCandidateFilter, skipVertexFilter = True, skipULFilter= True), getLeptonSelection(mode)])
			#	sample.style = styles.fillStyle(sample.color)

			else:
				sample.read_variables += ['year/I', ]
				sample.weight         = lambda event, sample: event.reweightPU * event.reweightBTag_SF * event.reweightL1Prefire * event.reweightLeptonSF * event.reweightwPt * lumi_year[event.year]/1000  
				#sample.scale = lumi_scale 
				sample.setSelectionString([getFilterCut(isData=False, year=year, skipBadPFMuon=args.noBadPFMuonFilter, skipBadChargedCandidate=args.noBadChargedCandidateFilter, skipVertexFilter = True), getLeptonSelection(mode)])
				sample.style = styles.fillStyle(sample.color)
		else:
			if "T2tt" in sample.name:
				sample.style = styles.errorStyle( color=sample.color, markerSize = 0.6)
				sample.weight         = lambda event, sample: event.reweightPU * event.reweightBTag_SF * event.reweightL1Prefire * event.reweightLeptonSF * event.reweightwPt
				sample.scale = lumi_scale
				sample.setSelectionString([getFilterCut(isData=False, year=year, skipBadPFMuon=args.noBadPFMuonFilter, skipBadChargedCandidate=args.noBadChargedCandidateFilter, skipVertexFilter = True), getLeptonSelection(mode),])
			else:

				sample.weight = lambda event, sample: event.reweightPU * event.reweightBTag_SF * event.reweightL1Prefire * event.reweightLeptonSF * event.reweightwPt
				sample.scale = lumi_scale
				sample.setSelectionString([getFilterCut(isData=False, year=year, skipBadPFMuon=args.noBadPFMuonFilter, skipBadChargedCandidate=args.noBadChargedCandidateFilter, skipVertexFilter = True), getLeptonSelection(mode),])
			
				sample.style = styles.fillStyle(sample.color)
	#stack_ = Stack( samples, data_sample ) 
	#stack_ = Stack( samples )
	#stack_ = Stack( samples, T2tt_500_470, T2tt_500_420 )

	stack_ = Stack( samples, data_sample, T2tt_500_470, T2tt_500_420 )
	# stack_ = Stack( samples, data_sample, T2tt_500_470,  T2tt_LL_400_380, T2tt_LL_350_335, T2tt_LL_300_290)

	if args.small:
		for sample in samples + [data_sample] + signals:
			sample.normalization = 1.
			sample.reduceFiles( factor = 50 )
			#sample.scale /= sample.normalization

	# Use some defaults
	Plot.setDefaults(stack = stack_, weight = (staticmethod(weight_)), selectionString = cutInterpreter.cutString(args.selection), addOverFlowBin='upper', histo_class=ROOT.TH1D)
	Plot2D.setDefaults( weight = (staticmethod(weight_)), selectionString = cutInterpreter.cutString(args.selection) )
	plots   = []
	plots2D = []

	plots.append(Plot(
	    texX = 'p_{T}(l_{1}) (GeV)', texY = 'Number of Events ',
	    attribute = TreeVariable.fromString( "l1_pt/F" ),
	    binning=[40,0,200],
	  ))
	plots.append(Plot(
	    texX = '#eta(l_{1}) (GeV)', texY = 'Number of Events ',
	    attribute = TreeVariable.fromString( "l1_eta/F" ),
	    binning=[15,-3,3],
	  ))
	plots.append(Plot(
	    texX = '#phi(l_{1}) (GeV)', texY = 'Number of Events ',
	    attribute = TreeVariable.fromString( "l1_phi/F" ),
	    binning=[20,-pi,pi],
	  ))
	plots.append(Plot(
	    texX = 'dxy(l_{1}) (cm)', texY = 'Number of Events ',
	    attribute = TreeVariable.fromString( "l1_dxy/F" ),
	    binning=[20,-.02,.02],
	  ))
	plots.append(Plot(name= 'loose_l1_dxy',
	    texX = 'loose_dxy(l_{1}) (cm)', texY = 'Number of Events ',
	    attribute = TreeVariable.fromString( "l1_dxy/F" ),
	    binning= [100,-10,10],
	  ))
	plots.append(Plot(
	    texX = 'loose_abs_dxy_full(l_{1}) (cm)', texY = 'Number of Events ',
	    name = 'l1_abs_dxy_full_nodxydz', attribute = lambda event, sample: event.l1_abs_dxy,
	    binning= [50,0,10],
	  ))
	plots.append(Plot(
	    texX = 'loose_abs_dxy(l_{1}) (cm)', texY = 'Number of Events ',
	    name = 'l1_abs_dxy_nodxydz', attribute = lambda event, sample: event.l1_abs_dxy,
	    binning= [49,0.2,10],
	  ))
	plots.append(Plot(
	    texX = 'loose_abs_low_dxy(l_{1}) (cm)', texY = 'Number of Events ',
	    name = 'l1_abs_low_dxy_nodxydz', attribute = lambda event, sample: event.l1_abs_dxy,
	    binning= [20,0,0.4],
	  ))
	plots.append(Plot(
	    texX = 'dz(l_{1}) (cm)', texY = 'Number of Events ',
	    attribute = TreeVariable.fromString( "l1_dz/F" ),
	    binning=[20,-.1,.1],
	  ))
	plots.append(Plot(name = 'loose_l1_dz',
	    texX = 'loose_dz(l_{1}) (cm)', texY = 'Number of Events ',
	    attribute = TreeVariable.fromString( "l1_dz/F" ),
	    binning=[48,-12,12],
	  ))
	plots.append(Plot(
	    texX = 'loose_abs_dz(l_{1}) (cm)', texY = 'Number of Events ',
	    name = 'l1_abs_dz_nodxydz', attribute = lambda event, sample: event.l1_abs_dz,
	    binning=[23,0.5,12],
	  ))
	plots.append(Plot(
	    texX = 'loose_abs_full_dz(l_{1}) (cm)', texY = 'Number of Events ',
	    name = 'l1_abs_full_dz_nodxydz', attribute = lambda event, sample: event.l1_abs_dz,
	    binning=[24,0,12],
	  ))
	plots.append(Plot(
	    texX = 'loose_abs_low_dz(l_{1}) (cm)', texY = 'Number of Events ',
	    name = 'l1_abs_low_dz_nodxydz', attribute = lambda event, sample: event.l1_abs_dz,
	    binning=[6,0,0.6],
	  ))
	plots.append(Plot(
	    texX = 'dzErr', texY = 'Number of Events ',
	    attribute = TreeVariable.fromString( "l1_dzErr/F" ),
	    binning=[24,0,12],
	  ))
	plots.append(Plot(
	    texX = 'dxyErr', texY = 'Number of Events ',
	    attribute = TreeVariable.fromString( "l1_dxyErr/F" ),
	    binning=[50,0,10],
	  ))
	plots.append(Plot(
	    texX = 'relIso03_all(l_{1})', texY = 'Number of Events ',
	    attribute = TreeVariable.fromString( "l1_relIso03/F" ),
	    binning=[30,0,5],
	  ))
	plots.append(Plot(
	    texX = 'miniRelIso_all(l_{1}) (GeV)', texY = 'Number of Events ',
	    attribute = TreeVariable.fromString( "l1_miniRelIso/F" ),
	    binning=[30,0,.5],
	  ))
	plots.append(Plot(
	    texX = 'ISR Jet p_{T} (GeV)', texY = 'Number of Events ',
	    attribute = TreeVariable.fromString( "ISRJets_pt/F" ),
	    binning=[45,100,1000],
	  ))
	plots.append(Plot(
	    texX = 'MET (GeV)', texY = 'Number of Events ',
	    attribute = TreeVariable.fromString( "met_pt/F" ),
	    binning=[40,200,1000],
	  ))
	plots.append(Plot(
	    texX = '#phi MET (GeV)', texY = 'Number of Events ',
	    attribute = TreeVariable.fromString( "met_phi/F" ),
	    binning=[20,-pi,pi],
	  ))
	plots.append(Plot(
	    texX = 'H_{T} (GeV)', texY = 'Number of Events ',
	    attribute = TreeVariable.fromString( "HT/F" ),
	    binning=[40,200,1000],
	  ))
	plots.append(Plot(
	    texX = 'M_{T} (GeV)', texY = 'Number of Events / 20 GeV',
	    attribute = TreeVariable.fromString( "mt/F" ),
	    binning=[40,0,200],
	  ))
	plots.append(Plot(
	    texX = 'Flag_BadPFMuonDzFilter', texY = 'Number of Events ',
	    name = 'Flag_BadPFMuonDzFilter', attribute = lambda event, sample: event.Flag_BadPFMuonDzFilter,
	    binning=[2,0,2],
	  ))
	plots.append(Plot(
	    texX = 'segment compatibility', texY = 'Number of Events ',
	    name = 'Muon_segmentComp', attribute = lambda event, sample: event.l1_segmentComp,
	    binning=[20,0,5],
	  ))
	plots.append(Plot(
	    texX = 'nStations', texY = 'Number of Events ',
	    name = 'Muon_nStations', attribute = lambda event, sample: event.l1_nStations,
	    binning=[10,0,10],
	  ))
	plots.append(Plot(
	    texX = 'tracker layers', texY = 'Number of Events ',
	    name = 'Muon_nTrackerLayers', attribute = lambda event, sample: event.l1_nTrackerLayers,
	    binning=[15,0,15],
	  ))
	plots.append(Plot(
	    texX = 'isGlobal', texY = 'Number of Events ',
	    name = 'Muon_isGlobal', attribute = lambda event, sample: event.l1_isGlobal,
	    binning=[2,0,2],
	  ))
	plots.append(Plot(
	    texX = 'isPF', texY = 'Number of Events ',
	    name = 'Muon_isPFCand', attribute = lambda event, sample: event.l1_isPF,
	    binning=[2,0,2],
	  ))
	plots.append(Plot(
	    texX = 'isTracker', texY = 'Number of Events ',
	    name = 'Muon_isTracker', attribute = lambda event, sample: event.l1_isTrackr,
	    binning=[2,0,2],
	  ))

	#plots.append(Plot(
	#    texX = 'Gen mu_p_{T}(l_{1}) (GeV)', texY = 'Number of Events ',
	#    name = 'GenMuPt', attribute = lambda event, sample: event.l1_muonGenPt,
	#    binning=[40,0,200],
	#  ))
	#plots.append(Plot(
	#    texX = ' mu_p_{T}/ muGen_p_{T}', texY = 'Number of Events ',
	#    name = 'RecoMuPtToGenMuPt', attribute = lambda event, sample: event.l1_muonPt_ratio,
	#    binning=[40,0,2],
	#  ))
	##plots.append(Plot(
	##    texX = 'M_{T} (GeV)', texY = 'Number of Events / 20 GeV',
	##    name = 'mt_mod', attribute = lambda event, sample: event.mtmod,
	##    binning=[40,0,300],
	##  ))

	plots.append(Plot(
	    texX = 'cos(#Delta#phi(l_{1},E_{T}^{miss})) (GeV)', texY = 'Number of Events ',
	    name = 'coslmetphi', attribute = lambda event, sample: cos(event.l1_phi - event.met_phi),
	    binning=[10,-1,1],
	  ))
	plots.append(Plot(
	    texX = '#Delta#phi(l_{1},E_{T}^{miss}) (GeV)', texY = 'Number of Events ',
	    name = 'dphilmet', attribute = lambda event, sample: event.l1_phi - event.met_phi,
	    binning=[20,-pi,pi],
	  ))
	plots.append(Plot(
	    texX = '#Delta#phi(l_{1},E_{T}^{miss}) (GeV)', texY = 'Number of Events ',
	    name = 'deltaPhilmet', attribute = lambda event, sample: deltaPhi(event.l1_phi ,event.met_phi),
	    binning=[20,0,pi],
	  ))
	plots.append(Plot(
	    texX = 'p_{T}(leading jet) (GeV)', texY = 'Number of Events / 30 GeV',
	    name = 'jet1_pt', attribute = lambda event, sample: event.JetGood_pt[0],
	    binning=[45,100,1000],
	  ))
	plots.append(Plot(
	    texX = '#eta(leading jet) (GeV)', texY = 'Number of Events',
	    name = 'jet1_eta', attribute = lambda event, sample: event.JetGood_eta[0],
	    binning=[10,-3,3],
	  ))
	plots.append(Plot(
	    texX = '#phi(leading jet) (GeV)', texY = 'Number of Events',
	    name = 'jet1_phi', attribute = lambda event, sample: event.JetGood_phi[0],
	    binning=[10,-pi,pi],
	  ))
	plots.append(Plot(
	    texX = 'log(1+HI)/log(1+5)', texY = 'Number of Events',
	    name = 'hybridIsolation', attribute = lambda event, sample: log(1+(event.l1_relIso03*(min(event.l1_pt,25))))/log(1+5),
	    binning=[20,0,4],
	  ))
	#plots.append(Plot(
	#    texX = 'dR between l1 and leading JetGood', texY = 'Number of Events ',
	#    name = 'deltaR', attribute = lambda event, sample: event.dR,
	#    binning=[10,-1,1],
	#  ))
	plots.append(Plot(
	    texX = 'pt Ratio between l1 and leading JetGood', texY = 'Number of Events ',
	    name = 'ptRatio', attribute = lambda event, sample: (event.JetGood_pt[0] / event.l1_pt),
	    binning=[10,0,10],
	  ))

	plots.append(Plot(
	    texX = 'dxy Significance', texY = 'Number of Events ',
	    name = 'dxySig', attribute = lambda event, sample: event.l1_dxySig,
	    binning=[50,0,10],
	  ))
	plots.append(Plot(
	    texX = 'dz Significance', texY = 'Number of Events ',
	    name = 'dzSig', attribute = lambda event, sample: event.l1_dzSig,
	    binning=[24,0,12],
	  ))
	# plots.append(Plot(name='stop_ct0p3_Lxy',
	#     texX = 'Lxy(stop_{1}_ct0p3) (cm)', texY = 'Number of Events ',
	#     attribute = TreeVariable.fromString( "stop1_Lxy/F" ),
	#     stack = Stack(T2tt_LL_400_380),
	#     binning=[100,0,10],
	#   ))
	# plots.append(Plot(name='stop_ct15_Lxy',
	#     texX = 'Lxy(stop_{1}_ct15) (cm)', texY = 'Number of Events ',
	#     attribute = TreeVariable.fromString( "stop1_Lxy/F" ),
	#     stack = Stack(T2tt_LL_350_335),
	#     binning=[100,0,100],
	#   ))
	# plots.append(Plot(name='stop_ct8m_Lxy',
	#     texX = 'Lxy(stop_{1}_ct8m) (cm)', texY = 'Number of Events ',
	#     attribute = TreeVariable.fromString( "stop1_Lxy/F" ),
	#     stack = Stack(T2tt_LL_300_290),
	#     binning=[800,0,4000],
	#   ))
	# plots.append(Plot(name= 'stop_ct15_dt',
	#     texX = 'dt(stop_{1}_ct15)', texY = 'Number of Events ',
	#     attribute = TreeVariable.fromString( "stop1_dt/F" ),
	#     stack = Stack(T2tt_LL_350_335),
	#     binning=[100,0,100],
	#   ))
	# plots.append(Plot(name = 'stop_ct8m_dt',
	#     texX = 'dt(stop_{1}_ct8m)', texY = 'Number of Events ',
	#     attribute = TreeVariable.fromString( "stop1_dt/F" ),
	#     stack = Stack(T2tt_LL_300_290),
	#     binning=[800,0,4000],
	#   ))
	# plots.append(Plot( name = 'stop_ct0p3_dt',
	#     texX = 'dt(stop_{1}_ct0p3)', texY = 'Number of Events ',
	#     attribute = TreeVariable.fromString( "stop1_dt/F" ),
	#     stack = Stack(T2tt_LL_400_380),
	#     binning=[100,0,10],
	#   ))
	#plots.append(Plot(
	#    texX = 'p_{T}(clean-leading jet) (GeV)', texY = 'Number of Events / 30 GeV',
	#    name = 'cleanjet1_pt', attribute = lambda event, sample: event.cleanJets_pt,
	#    binning=[45,100,1000],
	#  ))
	#plots.append(Plot(
	#    texX = '#eta(clean-leading jet) (GeV)', texY = 'Number of Events',
	#    name = 'cleanjet1_eta', attribute = lambda event, sample: event.cleanJets_eta,
	#    binning=[10,-3,3],
	#  ))
	#plots.append(Plot(
	#    texX = '#phi(clean-leading jet) (GeV)', texY = 'Number of Events',
	#    name = 'cleanjet1_phi', attribute = lambda event, sample: event.cleanJets_phi,
	#    binning=[10,-pi,pi],
	#  ))
	#plots.append(Plot(
	#    texX = 'number of clean jets', texY = 'Number of Events',
	#    name = 'nJetsClean', attribute = lambda event, sample: event.nJetsClean,
	#    binning=[10,0,10],
	#  ))
	#plots.append(Plot(
	#    texX = 'min(#Delta#phi(E_{T}^{miss},Jet)) (GeV)', texY = 'Number of Events ',
	#    name = 'min(dphimetjet)', attribute = lambda event, sample: event.dPhi,
	#    binning=[20,0,pi],addOverFlowBin = 'both',
	#  ))
	#plots.append(Plot(
	#    texX = 'min(#Delta#phi(E_{T}^{miss},Jet)) (GeV)', texY = 'Number of Events ',
	#    name = 'min(dphimetjet)npitopi', attribute = lambda event, sample: event.dPhi,
	#    binning=[20,-pi,pi],addOverFlowBin = 'both',
	#  ))
	plots.append(Plot(
	    texX = '#Delta#phi(E_{T}^{miss}, leading jet) (GeV)', texY = 'Number of Events ',
	    name = 'dphimetj0', attribute = lambda event, sample: deltaPhi(event.met_phi, event.JetGood_phi[0]),
	    binning=[20,0,pi],
	  ))
	plots.append(Plot(
	    texX = '#Delta#phi(E_{T}^{miss}, sub-leading jet) (GeV)', texY = 'Number of Events ',
	    name = 'dphimetj1', attribute = lambda event, sample: deltaPhi(event.met_phi, event.JetGood_phi[1]),
	    binning=[20,0,pi],
	  ))

	plots.append(Plot(
	    texX = 'min(#Delta#phi(E_{T}^{miss},Jet)) (GeV)', texY = 'Number of Events ',
	    name = 'min(dPhiMetJet)', attribute = TreeVariable.fromString("dPhiMetJet/F"),
	    binning=[20,0,pi], addOverFlowBin = 'both',
	  ))
	plots.append(Plot(
	    texX = 'lead/subleadJet', texY = 'Number of Events ',
	    name = 'whichJetformindphi', attribute = TreeVariable.fromString("metJet/I"),
	    binning=[3,0,3], 
	  ))
	plots.append(Plot(
	    texX = 'p_{T}(lowEl) (GeV)', texY = 'Number of Events ',
	    name = 'lowPtEl_pt', attribute = lambda event, sample: event.el_pt,
	    binning=[40,0,200],
	  ))
	if args.selection.count('njet2'):
		plots.append(Plot(
		    texX = 'p_{T}(sub-leading jet) (GeV)', texY = 'Number of Events ',
		    name = 'jet2_pt', attribute = lambda event, sample: event.JetGood_pt[1],
		    binning=[45,0,1000],
		  ))
		plots.append(Plot(
		    texX = '#eta(sub-leading jet) (GeV)', texY = 'Number of Events',
		    name = 'jet2_eta', attribute = lambda event, sample: event.JetGood_eta[1],
		    binning=[10,-3,3],
		  ))
		plots.append(Plot(
		    texX = '#phi(sub-leading jet) (GeV)', texY = 'Number of Events',
		    name = 'jet2_phi', attribute = lambda event, sample: event.JetGood_phi[1],
		    binning=[10,-pi,pi],
		  ))
	plots.append(Plot(
	    texX = 'C_{T1} (GeV)', texY = 'Number of Events ',
	    attribute = TreeVariable.fromString( "CT1/F" ),
	    binning=[45,100,1000],
	  ))
	plots.append(Plot(
	    texX = 'number of jets', texY = 'Number of Events',
	    attribute = TreeVariable.fromString('nJetGood/I'),
	    binning=[10,0,10],
	  ))
	plots.append(Plot(
	    texX = 'number of btagged jets', texY = 'Number of Events',
	    attribute = TreeVariable.fromString('nBTag/I'),
	    binning=[10,0,10],
	  ))
	plots.append(Plot(
	    texX = 'number of ISR jets', texY = 'Number of Events',
	    attribute = TreeVariable.fromString('nISRJets/I'),
	    binning=[3,0,3],
	  ))
	plots.append(Plot(
	   name = 'PV_npvsGood', texX = 'N_{PV} (good)', texY = 'Number of Events',
	   attribute = TreeVariable.fromString( "PV_npvsGood/I" ),
	   binning=[100,0,100],
	  ))
	plots.append(Plot(
	    name = 'yield', texX = 'yield', texY = 'Number of Events',
	    attribute = lambda event, sample: 0.5 + index ,
	    binning=[3, 0, 3],
	  ))

	plots2D.append(Plot2D(
		name = "WJets l1_dz vs dxy",
		texX  = 'l1_dz', texY = "l1_dxy",
		stack = Stack (samples[0]),
		attribute = (
			TreeVariable.fromString( "l1_dz/F" ),
			TreeVariable.fromString( "l1_dxy/F" ),
			),
		binning = [50,-12,12, 50,-10,10],
	  ))

	plots2D.append(Plot2D(
		name = "WJets l1_dz vs dzErr",
		texX  = 'l1_dz', texY = "l1_dzErr",
		stack = Stack (samples[0]),
		attribute = (
			lambda event, sample: event.l1_abs_dz,
			TreeVariable.fromString( "l1_dzErr/F" ),
			),
		binning = [24,0,12, 24,0,12],
	  ))

	plots2D.append(Plot2D(
		name = "WJets l1_dxy vs dxyErr",
		texX  = 'l1_dxy', texY = "l1_dxyErr",
		stack = Stack (samples[0]),
		attribute = (
			lambda event, sample: event.l1_abs_dxy,
			TreeVariable.fromString( "l1_dxyErr/F" ),
			),
		binning = [50,0,10, 50,0,10],
	  ))

	plots2D.append(Plot2D(
		name = "WJets pfRelIso03_all vs dz",
		texX  = 'l1_pfRelIso03', texY = "l1_dz",
		stack = Stack (samples[0]),
		attribute = (
			TreeVariable.fromString( "l1_relIso03/F" ),
			TreeVariable.fromString( "l1_dz/F" ),
			),
		binning = [30,0,5, 50,-10,10],
	  ))
	plots2D.append(Plot2D(
		name = "WJets pfRelIso03_all vs dxy",
		texX  = 'l1_pfRelIso03', texY = "l1_dxy",
		stack = Stack (samples[0]),
		attribute = (
			TreeVariable.fromString( "l1_relIso03/F" ),
			TreeVariable.fromString( "l1_dxy/F" ),
			),
		binning = [30,0,5, 50,-10,10],
	  ))

	plots2D.append(Plot2D(
		name = "T2tt_500_420 l1_dz vs dxy",
		texX  = 'l1_dz', texY = "l1_dxy",
		stack = Stack (T2tt_500_420),
		attribute = (
			TreeVariable.fromString( "l1_dz/F" ),
			TreeVariable.fromString( "l1_dxy/F" ),
			),
		binning = [50,-12,12, 50,-10,10],
	  ))

	plots2D.append(Plot2D(
		name = "T2tt_500_420 pfRelIso03_all vs dz",
		texX  = 'l1_pfRelIso03', texY = "l1_dz",
		stack = Stack (T2tt_500_420),
		attribute = (
			TreeVariable.fromString( "l1_relIso03/F" ),
			TreeVariable.fromString( "l1_dz/F" ),
			),
		binning = [30,0,5, 50,-10,10],
	  ))
	plots2D.append(Plot2D(
		name = "T2tt_500_420 pfRelIso03_all vs dxy",
		texX  = 'l1_pfRelIso03', texY = "l1_dxy",
		stack = Stack (T2tt_500_420),
		attribute = (
			TreeVariable.fromString( "l1_relIso03/F" ),
			TreeVariable.fromString( "l1_dxy/F" ),
			),
		binning = [30,0,5, 50,-10,10],
	  ))

	plots2D.append(Plot2D(
		name = "T2tt_500_420 l1_dz vs dzErr",
		texX  = 'l1_dz', texY = "l1_dzErr",
		stack = Stack (T2tt_500_420),
		attribute = (
			lambda event, sample: event.l1_abs_dz,
			TreeVariable.fromString( "l1_dzErr/F" ),
			),
		binning = [24,0,12, 24,0,12],
	  ))

	plots2D.append(Plot2D(
		name = "T2tt_500_420 l1_dxy vs dxyErr",
		texX  = 'l1_dxy', texY = "l1_dxyErr",
		stack = Stack (T2tt_500_420),
		attribute = (
			lambda event, sample: event.l1_abs_dxy,
			TreeVariable.fromString( "l1_dxyErr/F" ),
			),
		binning = [50,0,10, 50,0,10],
	  ))

	plots2D.append(Plot2D(
		name = "T2tt_500_470 l1_dz vs dxy",
		texX  = 'l1_dz', texY = "l1_dxy",
		stack = Stack (T2tt_500_470),
		attribute = (
			TreeVariable.fromString( "l1_dz/F" ),
			TreeVariable.fromString( "l1_dxy/F" ),
			),
		binning = [50,-12,12, 50,-10,10],
	  ))

	plots2D.append(Plot2D(
		name = "T2tt_500_470 pfRelIso03_all vs dz",
		texX  = 'l1_pfRelIso03', texY = "l1_dz",
		stack = Stack (T2tt_500_470),
		attribute = (
			TreeVariable.fromString( "l1_relIso03/F" ),
			TreeVariable.fromString( "l1_dz/F" ),
			),
		binning = [30,0,5, 50,-10,10],
	  ))
	plots2D.append(Plot2D(
		name = "T2tt_500_470 pfRelIso03_all vs dxy",
		texX  = 'l1_pfRelIso03', texY = "l1_dxy",
		stack = Stack (T2tt_500_470),
		attribute = (
			TreeVariable.fromString( "l1_relIso03/F" ),
			TreeVariable.fromString( "l1_dxy/F" ),
			),
		binning = [30,0,5, 50,-10,10],
	  ))

	plots2D.append(Plot2D(
		name = "T2tt_500_470 l1_dz vs dzErr",
		texX  = 'l1_dz', texY = "l1_dzErr",
		stack = Stack (T2tt_500_470),
		attribute = (
			lambda event, sample: event.l1_abs_dz,
			TreeVariable.fromString( "l1_dzErr/F" ),
			),
		binning = [24,0,12, 24,0,12],
	  ))

	plots2D.append(Plot2D(
		name = "T2tt_500_470 l1_dxy vs dxyErr",
		texX  = 'l1_dxy', texY = "l1_dxyErr",
		stack = Stack (T2tt_500_470),
		attribute = (
			lambda event, sample: event.l1_abs_dxy,
			TreeVariable.fromString( "l1_dxyErr/F" ),
			),
		binning = [50,0,10, 50,0,10],
	  ))

	# plots2D.append(Plot2D(
	# 	name = "T2tt_LL_300_290 l1_dz vs dxy",
	# 	texX  = 'l1_dz', texY = "l1_dxy",
	# 	stack = Stack (T2tt_LL_300_290),
	# 	attribute = (
	# 		TreeVariable.fromString( "l1_dz/F" ),
	# 		TreeVariable.fromString( "l1_dxy/F" ),
	# 		),
	# 	binning = [50,-12,12, 50,-10,10],
	#   ))

	# plots2D.append(Plot2D(
	# 	name = "T2tt_LL_300_290 pfRelIso03_all vs dz",
	# 	texX  = 'l1_pfRelIso03', texY = "l1_dz",
	# 	stack = Stack (T2tt_LL_300_290),
	# 	attribute = (
	# 		TreeVariable.fromString( "l1_relIso03/F" ),
	# 		TreeVariable.fromString( "l1_dz/F" ),
	# 		),
	# 	binning = [30,0,5, 50,-10,10],
	#   ))
	# plots2D.append(Plot2D(
	# 	name = "T2tt_LL_300_290 pfRelIso03_all vs dxy",
	# 	texX  = 'l1_pfRelIso03', texY = "l1_dxy",
	# 	stack = Stack (T2tt_LL_300_290),
	# 	attribute = (
	# 		TreeVariable.fromString( "l1_relIso03/F" ),
	# 		TreeVariable.fromString( "l1_dxy/F" ),
	# 		),
	# 	binning = [30,0,5, 50,-10,10],
	#   ))

	# plots2D.append(Plot2D(
	# 	name = "T2tt_LL_300_290 l1_dz vs dzErr",
	# 	texX  = 'l1_dz', texY = "l1_dzErr",
	# 	stack = Stack (T2tt_LL_300_290),
	# 	attribute = (
	# 		lambda event, sample: event.l1_abs_dz,
	# 		TreeVariable.fromString( "l1_dzErr/F" ),
	# 		),
	# 	binning = [24,0,12, 24,0,12],
	#   ))

	# plots2D.append(Plot2D(
	# 	name = "T2tt_LL_300_290 l1_dxy vs dxyErr",
	# 	texX  = 'l1_dxy', texY = "l1_dxyErr",
	# 	stack = Stack (T2tt_LL_300_290),
	# 	attribute = (
	# 		lambda event, sample: event.l1_abs_dxy,
	# 		TreeVariable.fromString( "l1_dxyErr/F" ),
	# 		),
	# 	binning = [50,0,10, 50,0,10],
	#   ))
	# plots2D.append(Plot2D(
	# 	name = "T2tt_LL_400_380 l1_dz vs dxy",
	# 	texX  = 'l1_dz', texY = "l1_dxy",
	# 	stack = Stack (T2tt_LL_400_380),
	# 	attribute = (
	# 		TreeVariable.fromString( "l1_dz/F" ),
	# 		TreeVariable.fromString( "l1_dxy/F" ),
	# 		),
	# 	binning = [50,-12,12, 50,-10,10],
	#   ))

	# plots2D.append(Plot2D(
	# 	name = "T2tt_LL_400_380 pfRelIso03_all vs dz",
	# 	texX  = 'l1_pfRelIso03', texY = "l1_dz",
	# 	stack = Stack (T2tt_LL_400_380),
	# 	attribute = (
	# 		TreeVariable.fromString( "l1_relIso03/F" ),
	# 		TreeVariable.fromString( "l1_dz/F" ),
	# 		),
	# 	binning = [30,0,5, 50,-10,10],
	#   ))
	# plots2D.append(Plot2D(
	# 	name = "T2tt_LL_400_380 pfRelIso03_all vs dxy",
	# 	texX  = 'l1_pfRelIso03', texY = "l1_dxy",
	# 	stack = Stack (T2tt_LL_400_380),
	# 	attribute = (
	# 		TreeVariable.fromString( "l1_relIso03/F" ),
	# 		TreeVariable.fromString( "l1_dxy/F" ),
	# 		),
	# 	binning = [30,0,5, 50,-10,10],
	#   ))

	# plots2D.append(Plot2D(
	# 	name = "T2tt_LL_400_380 l1_dz vs dzErr",
	# 	texX  = 'l1_dz', texY = "l1_dzErr",
	# 	stack = Stack (T2tt_LL_400_380),
	# 	attribute = (
	# 		lambda event, sample: event.l1_abs_dz,
	# 		TreeVariable.fromString( "l1_dzErr/F" ),
	# 		),
	# 	binning = [24,0,12, 24,0,12],
	#   ))

	# plots2D.append(Plot2D(
	# 	name = "T2tt_LL_400_380 l1_dxy vs dxyErr",
	# 	texX  = 'l1_dxy', texY = "l1_dxyErr",
	# 	stack = Stack (T2tt_LL_400_380),
	# 	attribute = (
	# 		lambda event, sample: event.l1_abs_dxy,
	# 		TreeVariable.fromString( "l1_dxyErr/F" ),
	# 		),
	# 	binning = [50,0,10, 50,0,10],
	#   ))

	# plots2D.append(Plot2D(
	# 	name = "T2tt_LL_350_335 l1_dz vs dxy",
	# 	texX  = 'l1_dz', texY = "l1_dxy",
	# 	stack = Stack (T2tt_LL_350_335),
	# 	attribute = (
	# 		TreeVariable.fromString( "l1_dz/F" ),
	# 		TreeVariable.fromString( "l1_dxy/F" ),
	# 		),
	# 	binning = [50,-12,12, 50,-10,10],
	#   ))

	# plots2D.append(Plot2D(
	# 	name = "T2tt_LL_350_335 pfRelIso03_all vs dz",
	# 	texX  = 'l1_pfRelIso03', texY = "l1_dz",
	# 	stack = Stack (T2tt_LL_350_335),
	# 	attribute = (
	# 		TreeVariable.fromString( "l1_relIso03/F" ),
	# 		TreeVariable.fromString( "l1_dz/F" ),
	# 		),
	# 	binning = [30,0,5, 50,-10,10],
	#   ))
	# plots2D.append(Plot2D(
	# 	name = "T2tt_LL_350_335 pfRelIso03_all vs dxy",
	# 	texX  = 'l1_pfRelIso03', texY = "l1_dxy",
	# 	stack = Stack (T2tt_LL_350_335),
	# 	attribute = (
	# 		TreeVariable.fromString( "l1_relIso03/F" ),
	# 		TreeVariable.fromString( "l1_dxy/F" ),
	# 		),
	# 	binning = [30,0,5, 50,-10,10],
	#   ))

	# plots2D.append(Plot2D(
	# 	name = "T2tt_LL_350_335 l1_dz vs dzErr",
	# 	texX  = 'l1_dz', texY = "l1_dzErr",
	# 	stack = Stack (T2tt_LL_350_335),
	# 	attribute = (
	# 		lambda event, sample: event.l1_abs_dz,
	# 		TreeVariable.fromString( "l1_dzErr/F" ),
	# 		),
	# 	binning = [24,0,12, 24,0,12],
	#   ))

	# plots2D.append(Plot2D(
	# 	name = "T2tt_LL_350_335 l1_dxy vs dxyErr",
	# 	texX  = 'l1_dxy', texY = "l1_dxyErr",
	# 	stack = Stack (T2tt_LL_350_335),
	# 	attribute = (
	# 		lambda event, sample: event.l1_abs_dxy,
	# 		TreeVariable.fromString( "l1_dxyErr/F" ),
	# 		),
	# 	binning = [50,0,10, 50,0,10],
	#   ))
	plots2D.append(Plot2D(
		name = "QCD l1_dz vs dxy",
		texX  = 'l1_dz', texY = "l1_dxy",
		stack = Stack (samples[5]),
		attribute = (
			TreeVariable.fromString( "l1_dz/F" ),
			TreeVariable.fromString( "l1_dxy/F" ),
			),
		binning = [50,-12,12, 50,-10,10],
	  ))

	plots2D.append(Plot2D(
		name = "QCD pfRelIso03_all vs dz",
		texX  = 'l1_pfRelIso03', texY = "l1_dz",
		stack = Stack (samples[5]),
		attribute = (
			TreeVariable.fromString( "l1_relIso03/F" ),
			TreeVariable.fromString( "l1_dz/F" ),
			),
		binning = [30,0,5, 50,-10,10],
	  ))
	plots2D.append(Plot2D(
		name = "QCD pfRelIso03_all vs dxy",
		texX  = 'l1_pfRelIso03', texY = "l1_dxy",
		stack = Stack (samples[5]),
		attribute = (
			TreeVariable.fromString( "l1_relIso03/F" ),
			TreeVariable.fromString( "l1_dxy/F" ),
			),
		binning = [30,0,5, 50,-10,10],
	  ))

	plots2D.append(Plot2D(
		name = "QCD l1_dz vs dzErr",
		texX  = 'l1_dz', texY = "l1_dzErr",
		stack = Stack (samples[5]),
		attribute = (
			lambda event, sample: event.l1_abs_dz,
			TreeVariable.fromString( "l1_dzErr/F" ),
			),
		binning = [24,0,12, 24,0,12],
	  ))

	plots2D.append(Plot2D(
		name = "QCD l1_dxy vs dxyErr",
		texX  = 'l1_dxy', texY = "l1_dxyErr",
		stack = Stack (samples[5]),
		attribute = (
			lambda event, sample: event.l1_abs_dxy,
			TreeVariable.fromString( "l1_dxyErr/F" ),
			),
		binning = [50,0,10, 50,0,10],
	  ))
#	plots2D.append(Plot2D(
#		name = "Data_Jet_eta_vs_phi",
#		texX  = '#eta', texY = "#phi",
#		stack = Stack ([data_sample]),
#		attribute = (
#			lambda event, sample: event.JetGood_eta[0],
#			lambda event, sample: event.JetGood_phi[0],
#			),
#		binning = [10,-3,3, 10,-pi,pi],
#	  ))
#	plots2D.append(Plot2D(
#		name = "MC_Jet_eta_vs_phi",
#		texX  = '#eta', texY = "#phi",
#		stack = Stack (samples),
#		attribute = (
#			lambda event, sample: event.JetGood_eta[0],
#			lambda event, sample: event.JetGood_phi[0],
#			),
#		binning = [10,-3,3, 10,-pi,pi],
#	  ))
#	plots2D.append(Plot2D(
#		name = "Data_l1_eta_vs_phi",
#		texX  = '#eta', texY = "#phi",
#		stack = Stack ([data_sample]),
#		attribute = (
#			TreeVariable.fromString( "l1_eta/F" ),
#			TreeVariable.fromString( "l1_phi/F" ),
#			),
#		binning = [10,-3,3, 10,-pi,pi],
#	  ))
#	plots2D.append(Plot2D(
#		name = "MC_l1_eta_vs_phi",
#		texX  = '#eta', texY = "#phi",
#		stack = Stack (samples),
#		attribute = (
#			TreeVariable.fromString( "l1_eta/F" ),
#			TreeVariable.fromString( "l1_phi/F" ),
#			),
#		binning = [10,-3,3, 10,-pi,pi],
#	  ))
#	plots2D.append(Plot2D(
#		name = "Data_MET_eta_vs_phi",
#		texX  = 'MET #eta', texY = "MET #phi",
#		stack = Stack ([data_sample]),
#		attribute = (
#			lambda event, sample: event.MET_eta,
#			TreeVariable.fromString( "met_phi/F" ),
#			),
#		binning = [10,-3,3, 10,-pi,pi],
#	  ))
#	plots2D.append(Plot2D(
#		name = "MC_MET_eta_vs_phi",
#		texX  = 'MET #eta', texY = "MET #phi",
#		stack = Stack (samples),
#		attribute = (
#			lambda event, sample: event.met_eta,
#			TreeVariable.fromString( "met_phi/F" ),
#			),
#		binning = [10,-3,3, 10,-pi,pi],
#	  ))
#	plots2D.append(Plot2D(
#		name = "Data_cosdphi_vs_Mt",
#		texX  = 'cos(#Delta#phi(l_{1},E_{T}^{miss}))', texY = "M_{t} (GeV)",
#		stack = Stack ([data_sample]),
#		attribute = (
#			lambda event, sample: cos(event.l1_phi - event.met_phi),
#			TreeVariable.fromString( "mt/F" ),
#			),
#		binning = [20,-1,1, 40,0,300],
#	  ))
#	plots2D.append(Plot2D(
#		name = "MC_cosdphi_vs_Mt",
#		texX  = 'cos(#Delta#phi(l_{1},E_{T}^{miss}))', texY = "M_{t} (GeV)",
#		stack = Stack (samples),
#		attribute = (
#			lambda event, sample: cos(event.l1_phi - event.met_phi),
#			TreeVariable.fromString( "mt/F" ),
#			),
#		binning = [20,-1,1, 40,0,300],
#	  ))


	plotting.fill(plots+plots2D, read_variables = read_variables, sequence = sequence)
	#plotting.fill(plots, read_variables = read_variables, sequence = sequence)

	#Get normalization yields from yield histogram
	for plot in plots:
		if plot.name == "yield":
			for i, l in enumerate(plot.histos):
				for j, h in enumerate(l):
					yields[mode][plot.stack[i][j].name] = h.GetBinContent(h.FindBin(0.5+index))
					h.GetXaxis().SetBinLabel(1, "#mu")
					h.GetXaxis().SetBinLabel(2, "e")
	for s in samples:
		print "INFO: Yield for %s: %f" % (s.name, yields[mode][s.name])
	yields[mode]["MC"] = sum(yields[mode][s.name] for s in samples)
	if isnan(yields[mode]["MC"]):
		print "ERROR: MC Yield is nan"
		dataMCScale = 1
	elif yields[mode]["MC"] == 0:
		print "ERROR: MC Yield is 0"
		dataMCScale = 1
	else:
		dataMCScale        = yields[mode]["data"]/yields[mode]["MC"]
	## if plotting only MC
	#dataMCScale = 1

	drawPlots(plots, mode, dataMCScale)
	
	for plot in plots2D:
		plotting.draw2D(
				plot=plot,
				plot_directory=os.path.join(plot_directory, 'analysisPlots', args.targetDir, args.era ,mode+"log",args.selection) ,
				logX = False, logY = False, logZ = True,
				drawObjects = drawObjects( True, float('nan')),
				)

	allPlots[mode] = plots

# Add the different channels into all	
yields['all'] = {}
allPlots['all']= {}
for y in yields[allModes[0]]:
	try:	yields['all'][y] = sum(yields[c][y] for c in (['mu','e']))
	except: yields['all'][y] = 0

if isnan(yields['all']["MC"]):
	print "ERROR: MC Yield is nan"
	dataMCScale = 1
elif yields['all']["MC"] == 0:
	print "ERROR: MC Yield is 0"
	dataMCScale = 1
else:
	dataMCScale        = yields['all']["data"]/yields['all']["MC"]

## if only plotting MC and data
#dataMCScale = 1

for plot in allPlots['mu']:
	for plot2 in (p for p in allPlots['e'] if p.name == plot.name): 
		for i, j in enumerate(list(itertools.chain.from_iterable(plot.histos))):
			for k, l in enumerate(list(itertools.chain.from_iterable(plot2.histos))):
				if i==k:
					j.Add(l)
	
drawPlots(allPlots['mu'], 'all', dataMCScale)

### For saving specific histograms in root files with simplified names ###

plots_root = ["l1_abs_full_dz_nodxydz", "l1_abs_low_dz_nodxydz", "l1_abs_dxy_full_nodxydz", "l1_abs_low_dxy_nodxydz" ]

print "Now write results in root file."
plot_dir = os.path.join(plot_directory, 'analysisPlots', 'HInoDxyDz', args.targetDir, args.era, args.selection)
if not os.path.exists(plot_dir):
	try:
		os.makedirs(plot_dir)
	except:
		print 'Could not create', plot_dir
outfilename = plot_dir+'/Results.root'
print "Saving in", outfilename
outfile = ROOT.TFile(outfilename, 'recreate')
outfile.cd()
for plot in allPlots['mu']:
	if plot.name in plots_root:
		for idx, histo_list in enumerate(plot.histos):
			for j, h in enumerate(histo_list):
				histname = h.GetName()
				process = histname
				if "WJetsToLNu_HT" in histname: process = "WJets"
				elif "Top_pow" in histname: process = "Top"
				elif "singleTop" in histname: process = "singleTop"
				elif "ZInv" in histname: process = "ZInv"
				elif "DY_HT_LO" in histname: process = "DY_HT_LO"
				elif "QCD_HT" in histname: process = "QCD"
				elif "VV" in histname: process = "VV"
				elif "TTX" in histname: process = "TTX"
				elif "T2tt_500_470" in histname: process = "T2tt_500_470"
				elif "T2tt_500_450" in histname: process = "T2tt_500_450"
				elif "T2tt_500_420" in histname: process = "T2tt_500_470"
				elif "T2tt_LL_400_380" in histname: process = "T2tt_LL_400_380"
				elif "T2tt_LL_350_335" in histname: process = "T2tt_LL_350_335"
				elif "T2tt_LL_300_290" in histname: process = "T2tt_LL_300_290"
				elif "data" in histname: process = "data"
				h.Write(plot.name+"__"+process)
outfile.Close()
logger.info( "Done with prefix %s and selectionString %s", args.selection, cutInterpreter.cutString(args.selection) )
