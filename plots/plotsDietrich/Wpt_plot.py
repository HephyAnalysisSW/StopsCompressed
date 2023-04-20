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

from math   import pi, sqrt, sin, cos, atan2, log
from RootTools.core.standard import *
from StopsCompressed.Tools.user             import plot_directory
from Analysis.Tools.metFilters              import getFilterCut
#from Analysis.Tools.metFilters              import getFilterCut
from StopsCompressed.Tools.cutInterpreter   import cutInterpreter
from Analysis.Tools.puProfileCache import *
from StopsCompressed.Tools.helpers           import deltaR, deltaPhi,ptRatio
from StopsCompressed.Tools.objectSelection   import muonSelector, eleSelector,  getGoodMuons, getGoodElectrons, getGoodTaus, getAllJets

from Analysis.Tools.DirDB                import DirDB


#
# Arguments
#
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',           		action='store',      default='INFO',          nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--era',                		action='store',      default="Run2018",  	type=str )
argParser.add_argument('--small',              		action='store_true', 			help='Run only on a small subset of the data?')#, default = True)
argParser.add_argument('--targetDir',          		action='store',      default='UL_v10')
#argParser.add_argument('--selection',          		action='store',      default='nISRJets1p-ntau0-lepSel-deltaPhiJets-jet3Veto-met200-ht300')
argParser.add_argument('--selection',          		action='store',      default='nISRJets1p-ntau0-lepSel-dphimetjet0p5-jet3Veto-met200-ht300')
argParser.add_argument('--reweightPU',         		action='store',      default=None, 		  choices=['VDown', 'Down', 'Central', 'Up', 'VUp', 'VVUp'])
argParser.add_argument('--badMuonFilters',     		action='store',      default="Summer2016",  	  help="Which bad muon filters" )
argParser.add_argument('--noBadPFMuonFilter',           action='store_true', default=False)
argParser.add_argument('--noBadChargedCandidateFilter', action='store_true', default=False)
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
if args.postHEM:                      args.targetDir += "_postHEM"

#
# Make samples, will be searched for in the postProcessing directory
#
from Analysis.Tools.puReweighting import getReweightingFunction

if "2016" in args.era:
    year = 2016
elif "2017" in args.era:
    year = 2017
elif "2018" in args.era:
    year = 2018
logger.info( "Working in year %i", year )

if args.era == "Run2016preVFP":
	from StopsCompressed.samples.nanoTuples_UL16APV_postProcessed import *
	samples = [WJetsToLNu_HT_16APV]	
 
	from StopsCompressed.samples.nanoTuples_RunUL16APV_postProcessed import *
	data_sample = Run2016preVFP  

	signals = []
elif args.era == "Run2016postVFP":
	from StopsCompressed.samples.nanoTuples_UL16_postProcessed import *
	samples = [WJetsToLNu_HT_16]

	from StopsCompressed.samples.nanoTuples_RunUL16_postProcessed import *
	data_sample = Run2016postVFP  
	signals = []
elif args.era == "Run2017":
	from StopsCompressed.samples.nanoTuples_UL17_postProcessed import *
	samples = [WJetsToLNu_HT_17]
	from StopsCompressed.samples.nanoTuples_RunUL17_postProcessed import *
	data_sample = Run2017
	signals = []
elif args.era == "Run2018":
	from StopsCompressed.samples.nanoTuples_UL18_postProcessed import *
	samples = [WJetsToLNu_HT_18]
	from StopsCompressed.samples.nanoTuples_RunUL18_postProcessed import *
	data_sample = Run2018
	signals = []
    
# Text on the plots
#
tex = ROOT.TLatex()
tex.SetNDC()
tex.SetTextSize(0.04)
tex.SetTextAlign(11) # align right
#lumi_scale = 35.9

def drawObjects( plotData, dataMCScale):
    lines = [
      (0.15, 0.95, 'CMS Preliminary' if plotData else 'CMS Simulation'), 
      (0.45, 0.95, ' L=%3.1f fb{}^{-1}(13 TeV) Scale %3.2f'% ( lumi_scale , dataMCScale) )
    ]
    return [tex.DrawLatex(*l) for l in lines] 

def drawPlots(plots,mode, dataMCScale):
	helper = ROOT.TFile("help_{}_{}.root".format(mode,args.selection),"recreate")
  	for log in [False, True]:
		plot_directory_ = os.path.join(plot_directory, 'analysisPlots', args.targetDir, args.era ,mode +("log" if log else ""), args.selection)
		for plot in plots:
			for h in plot.histos :
				if log :
					h[0].Write()
				print [ h[x].GetName() for x in range(len(h))]
				
			_drawObjects = []
			plotting.draw(
				plot,
				plot_directory = plot_directory_,
				# ratio = {'yRange':(0.1,1.9)},
				ratio = None,
				logX = False, logY = log, sorting = False,
				yRange = (0.03, "auto") if log else (0.001, "auto"),
				scaling = {},
				legend = ( (0.18,0.88-0.03*sum(map(len, plot.histos)),0.9,0.88), 2),
				drawObjects = drawObjects( True, dataMCScale) + _drawObjects,
				copyIndexPHP = True, extensions = ["png","pdf", "root"],
			)
	helper.Close()

# Read variables and sequences
read_variables = [
            "weight/F", "l1_pt/F","lep_wPt/F", "l1_eta/F" , "l1_phi/F", "l1_pdgId/I", "l1_muIndex/I", "reweightHEM/F","l1_miniRelIso/F", "l1_relIso03/F", "nlep/I",
	    "lep[pt/F, eta/F, phi/F]",
            "JetGood[pt/F, eta/F, phi/F, genPt/F]", 
            "Jet[pt/F, eta/F, phi/F, jetId/I]", 
            "met_pt/F", "met_phi/F","CT1/F", "HT/F","mt/F", 'l1_dxy/F', 'l1_dz/F', 'dphij0j1/F','ISRJets_pt/F', 'nISRJets/I','nSoftBJets/I','nHardBJets/I', "nBTag/I", "nJetGood/I", "PV_npvsGood/I","event/I","run/I"]
read_variables += [
            "nMuon/I","nElectron/I","nJet/I",
            "Muon[dxy/F,dxyErr/F,dz/F,dzErr/F,eta/F,ip3d/F,jetRelIso/F,mass/F,miniPFRelIso_all/F,miniPFRelIso_chg/F,pfRelIso03_all/F,pfRelIso03_chg/F,pfRelIso04_all/F,phi/F,pt/F,ptErr/F,segmentComp/F,sip3d/F,mvaTTH/F,charge/I,jetIdx/I,nStations/I,nTrackerLayers/I,pdgId/I,tightCharge/I,highPtId/b,inTimeMuon/O,isGlobal/O,isPFcand/O,isTracker/O,mediumId/O,mediumPromptId/O,miniIsoId/b,multiIsoId/b,mvaId/b,pfIsoId/b,softId/O,softMvaId/O,tightId/O,tkIsoId/b,triggerIdLoose/O]"
            "Electron[dxy/F,dxyErr/F,dz/F,dzErr/F,eta/F,ip3d/F,jetRelIso/F,mass/F,miniPFRelIso_all/F,miniPFRelIso_chg/F,pfRelIso03_all/F,pfRelIso03_chg/F,pfRelIso04_all/F,phi/F,pt/F,ptErr/F,segmentComp/F,sip3d/F,mvaTTH/F,charge/I,jetIdx/I,nStations/I,nTrackerLayers/I,pdgId/I,tightCharge/I,highPtId/b,inTimeMuon/O,isGlobal/O,isPFcand/O,isTracker/O,mediumId/O,mediumPromptId/O,miniIsoId/b,multiIsoId/b,mvaId/b,pfIsoId/b,softId/O,softMvaId/O,tightId/O,tkIsoId/b,triggerIdLoose/O]"
            ]

sequence = []

# FR_file = ROOT.TFile("/users/janik.andrejkovic/public/HEPHY_Analysis/CMSSW_10_2_18/src/tWZ/plots/plotsJanik/fakes/TL_metTo50-mTTo40.root")
# TightToLoose = FR_file.Get("TL")
def mtwithdphi(event, sample):
	event.mtmod = float('nan')
	if deltaPhi(event.l1_phi ,event.met_phi) < 1.7: 
		event.mtmod            = sqrt (2 * event.l1_pt * event.met_pt * (1 - cos(event.l1_phi - event.met_phi) ) )
def delR(event,sample):
	event.dR = float("nan")
	event.dR = sqrt(((deltaPhi(event.l1_phi,event.JetGood_phi[0])**2) + ((event.l1_eta - event.JetGood_eta[0])**2)))
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
# def frHybridIso(event,sample) :
# 	if event.l1_pt <= 25 :
# 		event.HI = event.l1_relIso03*event.l1_pt
# 	else :
# 		event.HI = event.l1_relIso03*25.

# 	event.tight = 0.
# 	event.loose = 0.
# 	event.TLratio = 1.
# 	if event.HI <= 5 :
# 		event.tight = 1.
# 	elif event.HI > 5 and event.HI <= 20 :
# 		event.loose = 1.
# 		event.TLratio = TightToLoose.GetBinContent(TightToLoose.GetXaxis().FindBin(event.l1_pt),TightToLoose.GetYaxis().FindBin(abs(event.l1_eta)))
		
def getLeptonSelection( mode ):
	if   mode == 'mu': return "abs(l1_pdgId)==13"
	elif mode == 'e' : return "abs(l1_pdgId)==11"
def IsoCutWeight (Tight=True, inclusive=False, TL=False) :
    def myIsoWeight(event, sample ):
        if inclusive :
            return event.weight
        else :
            if event.HI <= 5 and Tight == True:
                return event.weight
            elif event.HI > 5 and event.HI <= 20 and Tight == False:
				if TL :
					print(event.TLratio)
					return event.weight * event.TLratio
				else :
					return event.weight        
            else:
                return 0
        
    return myIsoWeight

# sequence.append(delR)
# sequence.append(frHybridIso)



yields   = {}
allPlots = {}
allModes = ['mu','e']
for index, mode in enumerate(allModes):
	yields[mode] = {}
	data_sample.setSelectionString([getFilterCut(isData=True, year=year, skipBadPFMuon=args.noBadPFMuonFilter, skipBadChargedCandidate=args.noBadChargedCandidateFilter, skipVertexFilter = True), getLeptonSelection(mode)])
	if args.preHEM:
		data_sample.addSelectionString("run<319077")
	if args.postHEM:
		data_sample.addSelectionString("run>=319077")
	lumi_scale                 = data_sample.lumi/1000
	if args.preHEM:   lumi_scale *= 0.37
	if args.postHEM:  lumi_scale *= 0.63
	data_sample.scale          = 1.
	data_sample.style          = styles.errorStyle(ROOT.kBlack)
	data_sample.name 	   = "data"
	
	weight_ = lambda event, sample: event.weight*event.reweightHEM

	for sample in samples :
		sample.read_variables  = ['reweightPU/F', 'Pileup_nTrueInt/F','reweightLeptonSF/F', 'reweightBTag_SF/F','reweightL1Prefire/F','reweightnISR/F', 'reweightwPt/F', 'reweightwPtUp/F', 'reweightwPtDown/F']
		sample.read_variables += ['reweightPU%s/F'%args.reweightPU if args.reweightPU != "Central" else "reweightPU/F"]
		pu_getter = operator.attrgetter('reweightPU' if args.reweightPU=='Central' else "reweightPU%s"%args.reweightPU)
		# sample.weight         = lambda event, sample: event.tight * pu_getter(event) * event.reweightBTag_SF * event.reweightL1Prefire * event.reweightnISR * event.reweightwPt * event.reweightLeptonSF
		sample.weight         = lambda event, sample: pu_getter(event) * event.reweightBTag_SF * event.reweightL1Prefire * event.reweightnISR * event.reweightLeptonSF
		sample.scale = lumi_scale 
		sample.setSelectionString([getFilterCut(isData=False, year=year, skipBadPFMuon=args.noBadPFMuonFilter, skipBadChargedCandidate=args.noBadChargedCandidateFilter, skipVertexFilter = True), getLeptonSelection(mode)])
		sample.style = styles.fillStyle(sample.color)
	
	stack_ = Stack( samples ) 
	
	
	if args.small:
		for sample in samples + [data_sample] + signals : # + prediction:
			sample.normalization = 1.
			sample.reduceFiles( factor = 40 )
			sample.scale /= sample.normalization

	# Use some defaults
	Plot.setDefaults(stack = stack_, weight = (staticmethod(weight_)), selectionString = cutInterpreter.cutString(args.selection), addOverFlowBin='upper', histo_class=ROOT.TH1D)
	Plot2D.setDefaults( weight = (staticmethod(weight_)), selectionString = cutInterpreter.cutString(args.selection) )
	plots   = []
	plots2D = []
 
	plots.append(Plot(
        name = "l1pt",
        texX = 'p_{T}(l_{1}) - nominal (GeV)', texY = 'Number of Events ',
        attribute = TreeVariable.fromString( "l1_pt/F" ),
        # weight = lambda event, sample: event.reweightwPt ,
		weight = lambda event, sample: 1.,
        # weight=IsoCutWeight(Tight=True, inclusive=False),

        binning=[400,0,2000],
    ))
    #     plots.append(Plot(
	# 		name = "l1pt_up",
	# 		texX = 'p_{T}(l_{1}) - up (GeV)', texY = 'Number of Events ',
	# 		attribute = TreeVariable.fromString( "l1_pt/F" ),
	# 		weight = lambda event, sample: event.reweightwPtUp ,
	# 		# weight=IsoCutWeight(Tight=True, inclusive=False),

	# 		binning=[400,0,2000],
	# 	))

    #     plots.append(Plot(
	# 		name = "l1pt_down",
	# 		texX = 'p_{T}(l_{1}) - down (GeV)', texY = 'Number of Events ',
	# 		attribute = TreeVariable.fromString( "l1_pt/F" ),
	# 		weight = lambda event, sample: event.reweightwPtDown ,
	# 		# weight=IsoCutWeight(Tight=True, inclusive=False),

	# 		binning=[400,0,2000],
	# 	))

    #     plots.append(Plot(
	# 		name = "Wpt",
	# 		texX = 'W-p_{T}(l_{1}) - nominal (GeV)', texY = 'Number of Events ',
	# 		attribute = TreeVariable.fromString( "lep_wPt/F" ),
	# 		weight = lambda event, sample: event.reweightwPt ,
	# 		# weight=IsoCutWeight(Tight=True, inclusive=False),

	# 		binning=[1000,0,10000],
	# 	))
    #     plots.append(Plot(
	# 		name = "Wpt_up",
	# 		texX = 'W-p_{T}(l_{1}) - up (GeV)', texY = 'Number of Events ',
	# 		attribute = TreeVariable.fromString( "lep_wPt/F" ),
	# 		weight = lambda event, sample: event.reweightwPtUp ,
	# 		# weight=IsoCutWeight(Tight=True, inclusive=False),

	# 		binning=[1000,0,10000],
	# 	))

    #     plots.append(Plot(
	# 		name = "Wpt_down",
	# 		texX = 'W-p_{T}(l_{1}) - down (GeV)', texY = 'Number of Events ',
	# 		attribute = TreeVariable.fromString( "lep_wPt/F" ),
	# 		weight = lambda event, sample: event.reweightwPtDown ,
	# 		# weight=IsoCutWeight(Tight=True, inclusive=False),

	# 		binning=[1000,0,10000],
	# 	))

	plots.append(Plot(
		name = 'yield', 
		texX = 'yield', texY = 'Number of Events',
		attribute = lambda event, sample: 0.5 + index ,
		binning=[3, 0, 3]
	))

	
	
	plotting.fill(plots, read_variables = read_variables, sequence = sequence)

	#Get normalization yields from yield histogram
	for plot in plots:
		if plot.name == "yield":
			for i, l in enumerate(plot.histos):
				for j, h in enumerate(l):
					yields[mode][plot.stack[i][j].name] = h.GetBinContent(h.FindBin(0.5+index))
					h.GetXaxis().SetBinLabel(1, "#mu")
					h.GetXaxis().SetBinLabel(2, "e")
	for s in samples:
		print mode, s.name, yields[mode][s.name]
	yields[mode]["MC"] = sum(yields[mode][s.name] for s in samples)
	# yields[mode]["QCD-predcited"] = sum(yields[mode][s.name] for s in prediction)
	# dataMCScale        = yields[mode]["data"]/yields[mode]["MC"] if yields[mode]["MC"] != 0 else float('nan')
	# QCDScale        = yields[mode]["QCD-predcited"]/yields[mode]["MC"] if yields[mode]["MC"] != 0 else float('nan')
	dataMCScale = 1
	# drawPlots(plots, mode, dataMCScale)
	# print "QCD scale {}".format(QCDScale)
	drawPlots(plots, mode, dataMCScale)
	
	for plot in plots2D:
		plotting.draw2D(
				plot=plot,
				plot_directory=os.path.join(plot_directory, 'analysisPlots', args.targetDir, args.era ,mode+"log",args.selection) ,
				logX = False, logY = False, logZ = True,
				drawObjects = drawObjects( True, float('nan')),
				)

	allPlots[mode] = plots
	
	# ffile = ROOT.TFile("PtEtaMap_{}.root".format(mode),"RECREATE")
	# plots2D[0].histos[0][0].Write("PtEtaMap")
	# plots2D[1].histos[0][0].Write("PtEtaMapTight") # tight hybrid iso
	# plots2D[2].histos[0][0].Write("PtEtaMapLoose") # loose hybrid iso

	# ffile.Close()

# Add the different channels into all	
# yields['all'] = {}
# for y in yields[allModes[0]]:
# 	try:	yields['all'][y] = sum(yields[c][y] for c in (['mu','e']))
# 	except: yields['all'][y] = 0
# # s = yields['all']["data"]/yields['all']["MC"] if yields['all']["MC"] != 0 else float('nan')
dataMCScale = 1
for plot in allPlots['mu']:
	for plot2 in (p for p in allPlots['e'] if p.name == plot.name): 
		for i, j in enumerate(list(itertools.chain.from_iterable(plot.histos))):
			for k, l in enumerate(list(itertools.chain.from_iterable(plot2.histos))):
				if i==k:
					j.Add(l)
drawPlots(allPlots['mu'], 'all', dataMCScale)



# FR_file.Close()
