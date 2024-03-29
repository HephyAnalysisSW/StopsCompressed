#!/usr/bin/env python

""" 
Get cardfile result plots
"""

# Standard imports
import ROOT
ROOT.gROOT.SetBatch(True)
import os, sys
from array import *
# Helpers
from plotHelpers                      import *

# Analysis
from Analysis.Tools.cardFileWriter.CombineResults_Priya    import CombineResults

# StopsCompressed (inspired and stolen with immense pleasure from TTGammaEFT and StopsDilepton :D )
from StopsCompressed.Tools.user            import plot_directory, analysis_results
# from StopsCompressed.Analysis.regions_splitCR	   import controlRegions, signalRegions, regionMapping
from StopsCompressed.Analysis.SetupHelpers import *
from StopsCompressed.samples.color import color

#from TTGammaEFT.Analysis.SetupHelpers import allRegions, processesMisIDPOI, default_processes

# RootTools
from RootTools.core.standard          import *

# Arguments
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument("--small",                action="store_true",                            help="small?")
argParser.add_argument("--logLevel",             action="store",                default="INFO",  help="log level?", choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "TRACE", "NOTSET"])
argParser.add_argument("--blinded",              action="store_true")
argParser.add_argument("--overwrite",            action="store_true",                            help="Overwrite existing output files, bool flag set to True  if used")
argParser.add_argument("--postFit",              action="store_true",                            help="Apply pulls?")
argParser.add_argument("--expected",             action="store_true",                            help="Run expected?")
argParser.add_argument("--preliminary",          action="store_true", default=True,              help="preliminary?")
argParser.add_argument("--systOnly",             action="store_true",                            help="correlation matrix with systematics only?")
argParser.add_argument("--year",                 action="store",      type=int, default=2016,    help="Which year?")
#argParser.add_argument("--carddir",              action='store',                default='control2016/cardFiles/T2tt/expected',      help="which cardfile directory?")
# argParser.add_argument("--carddir",              action='store',                default='fitAllregion_test3/cardFiles/T2tt/expected',      help="which cardfile directory?")
argParser.add_argument("--carddir",              action='store',                default='Sensitivity',      help="which cardfile directory?")
# argParser.add_argument("--carddir",              action='store',                default='fitAllregion_test3/cardFiles/T2tt/observed_signalInjected',      help="which cardfile directory?")

argParser.add_argument("--cardfile",             action='store',                default='T2tt_500_440',      help="which cardfile?")
argParser.add_argument("--substituteCard",       action='store',                default=None,    help="which cardfile to substitute the plot with?")
argParser.add_argument("--plotRegions",          action='store', nargs="*",     default=None,    help="which regions to plot?")
argParser.add_argument("--plotChannels",         action='store', nargs="*",     default=None,    help="which regions to plot?")
argParser.add_argument("--plotNuisances",        action='store', nargs="*",     default=None,    help="plot specific nuisances?")
argParser.add_argument("--cores",                action="store", default=1,               type=int,                               help="Run on n cores in parallel")
argParser.add_argument("--bkgOnly",              action='store_true',                            help="background fit?")
argParser.add_argument("--sorted",               action='store_true',           default=False,   help="sort histogram for each bin?")
argParser.add_argument("--plotRegionPlot",       action='store_true',           default=False,   help="plot RegionPlot")
argParser.add_argument("--plotImpacts",          action='store_true',           default=False,   help="plot Impacts")
argParser.add_argument("--plotCovMatrix",        action='store_true',           default=False,   help="plot covariance matrix")
argParser.add_argument("--plotCorrelations",     action='store_true',           default=False,   help="plot Correlation matrix")
argParser.add_argument("--bkgSubstracted",       action='store_true',           default=False,   help="plot region plot background substracted")

argParser.add_argument("--l1pT_CR_split",       action='store_true',           default=False,   help="plot region plot background substracted")
argParser.add_argument("--mT_cut_value",       action='store',            default=95, choices=[95,100,105], type=int,   help="plot region plot background substracted")
argParser.add_argument("--extra_mT_cut",        action='store_true',           default=False,   help="plot region plot background substracted")
argParser.add_argument("--CT_cut_value",       action='store',            default=400, type=int,choices=[400,450],   help="plot region plot background substracted")
argParser.add_argument("--R1only",        action='store_true',           default=False,   help="")
argParser.add_argument("--R2only",        action='store_true',           default=False,   help="")


args = argParser.parse_args()

_NCR = 12
if (args.l1pT_CR_split) :
    _NBINS = 68
    if (args.mT_cut_value == 95) :
        if (args.extra_mT_cut) :
            _NBINS = 88
            _NCR = 16
            if (args.R1only) :
                _NBINS = 44
                _NCR = 8
                from StopsCompressed.Analysis.regions_splitCR_4mTregions_R1only import controlRegions, signalRegions, regionMapping
            elif (args.R2only) :
                _NCR = 8
                _NBINS = 44
                from StopsCompressed.Analysis.regions_splitCR_4mTregions_R2only import controlRegions, signalRegions, regionMapping
            else :
                from StopsCompressed.Analysis.regions_splitCR_4mTregions import controlRegions, signalRegions, regionMapping
        
        else :  
            if (args.CT_cut_value ==450) :
                from StopsCompressed.Analysis.regions_splitCR_CT450	         import controlRegions, signalRegions, regionMapping           
            else :
                from StopsCompressed.Analysis.regions_splitCR	         import controlRegions, signalRegions, regionMapping
    elif (args.mT_cut_value == 100) :
        from StopsCompressed.Analysis.regions_splitCR_mT100	   import controlRegions, signalRegions, regionMapping
    elif (args.mT_cut_value == 105) :
        from StopsCompressed.Analysis.regions_mt105_splitCR	   import controlRegions, signalRegions, regionMapping

else :
    _NBINS = 56
    if (args.mT_cut_value == 95) :
        from StopsCompressed.Analysis.regions	   import controlRegions, signalRegions, regionMapping
    elif (args.mT_cut_value == 100) :
        from StopsCompressed.Analysis.regions_mT100	   import controlRegions, signalRegions, regionMapping
    elif (args.mT_cut_value == 105) :
        from StopsCompressed.Analysis.regions_mt105	   import controlRegions, signalRegions, regionMapping




# logger
import Analysis.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(    args.logLevel, logFile = None )
logger_rt = logger_rt.get_logger( args.logLevel, logFile = None )

# make sure the list of nuisances is always in the same order
if args.plotNuisances: args.plotNuisances.sort()

if args.plotChannels and "all" in args.plotChannels: args.plotChannels += ["e","mu"]
if args.plotChannels and "e"   in args.plotChannels: args.plotChannels += ["e"]
if args.plotChannels and "mu"  in args.plotChannels: args.plotChannels += ["mu"]

# define luminosity for the chosen year
if   args.year == 2016: lumi_scale = 35.92
elif args.year == 2017: lumi_scale = 41.53
elif args.year == 2018: lumi_scale = 59.74





plotDirectory = os.path.join( plot_directory, "fit", str(args.year),"nbins{}_mt{}_extramT{}_CT{}_R1only{}_R2only{}".format(_NBINS,args.mT_cut_value,args.extra_mT_cut,args.CT_cut_value,args.R1only,args.R2only), args.cardfile, args.carddir.split("/")[-1] )
cardFile      = os.path.join( analysis_results,str(args.year), args.carddir,   args.cardfile+".txt" )
cardFileShape = os.path.join( analysis_results,str(args.year), args.carddir,   args.cardfile+"_shapeCard.txt" )
logger.info("Plotting from cardfile %s"%cardFile)


###Processes###
processes = { 
	'WJets': { "process":'WJets',	"color": color.WJetsToLNu ,	"texName":'W(l,#nu) + Jets (HT)'},
	'Top'  : { "process":'Top',	"color":color.Top_pow,		"texName":'t#bar{t}/t'},
	'ZInv' : { "process":'ZInv',	"color":color.ZInv,		"texName":'Z(#nu,#nu + Jets)'},
	'QCD'  : {"process":'QCD',	"color":color.QCD_HT,		"texName":'QCD (HT)'},
	#'Others': {"process":'Others',	"color":color.others,		"texName":'Others'}, #YELLOW
	'Others': {"process":'Others',	"color":color.other,		"texName":'Others'}
	}


# replace the combineResults object by the substituted card object
# Results = CombineResults( cardFile=cardFile, plotDirectory=plotDirectory, year=args.year, bkgOnly=args.bkgOnly, isSearch=False )
logger.debug("initializing combine Results")
Results = CombineResults( cardFile=cardFile, cardFileShape=cardFileShape, plotDirectory=plotDirectory, year=args.year, bkgOnly=args.bkgOnly, isSearch=True,createMissingInputs=True )

if args.substituteCard:
    logger.info("substituting card") 
    subCardFile = os.path.join( cache_directory, "analysis", str(args.year), args.carddir, args.substituteCard+".txt" )
    subCardFile = Results.createRebinnedResults( subCardFile )
    del Results
    Results     = CombineResults( cardFile=subCardFile, plotDirectory=plotDirectory, year=args.year, bkgOnly=args.bkgOnly, isSearch=False )

# get list of labels
labelFormater   = lambda x:x.split(" ")[1].split(":")[0]

labels = [ ( i, label ) for i, label in enumerate(Results.getBinLabels( labelFormater=lambda x:x.split(" "))[Results.channels[0]])]
#if args.plotRegions:  labels = filter( lambda (i,(ch, lab, reg)): reg in args.plotRegions, labels )
#if args.plotChannels: labels = filter( lambda (i,(ch, lab, reg)): ch in args.plotChannels, labels )

crName    = [ cr for i, (year, lep, cr) in labels ]
plotBins  = [ i  for i, (year, lep, cr) in labels ]
crLabel   = map( lambda (i,(year, ch, lab)): ", ".join( [ ch.replace("mu","#mu").replace("tight","") ] ), labels )
ptLabels  = map( lambda (i,(year, ch, lab)): "", labels )
nBins     = len(crLabel)


###
### PLOTS
###

# region plot, sorted/not sorted, w/ or w/o +-1sigma changes in one nuisance
def plotRegions( sorted=True ):
    
    resHisto = (Results.getRegionHistos( postFit=args.postFit, plotBins=plotBins, nuisances=args.plotNuisances, addStatOnlyHistos=False, bkgSubstracted=args.bkgSubstracted, labelFormater=labelFormater ))
    
    F = ROOT.TFile("myfile.root", "recreate")
    for hist_name in resHisto["Bin0"].keys() :
        resHisto["Bin0"][hist_name].Write("{}".format(hist_name))

    F.Close()
    
    hists = {}

    print "keys: {}".format(resHisto["Bin0"].keys())    
    for proc in resHisto["Bin0"].keys() :
        hists[proc] = ROOT.TH1F("{}".format(proc),"",len([i for i in range(_NBINS)]),array('d',[i for i in range(_NBINS+1)]))
    
    
    
    shift = 0
    for j, creg in enumerate(["Bin{}".format(i) for i in range(_NCR)])  :
        print "shift: {}".format(shift)
        for proc in resHisto[creg].keys() :
            for b in range(regionMapping[j]+1) :
                hists[proc].SetBinContent(b+1 + shift, resHisto[creg][proc].GetBinContent(b+1) )
                hists[proc].SetBinError(b+1 + shift, resHisto[creg][proc].GetBinError(b+1) )
                
        shift += regionMapping[j]+1#resHisto[creg][proc].GetNbinsX()

    labels = [
                str(k) for k in range(0,_NBINS)
		      ]
    for p in hists.keys() : 
    
        for i in range(hists[p].GetNbinsX()):

            
            hists[p].GetXaxis().SetBinLabel( i+1, labels[i] )
            hists[p].LabelsOption("v","X") #"vu" for 45 degree labels



    hists["data"].style        = styles.errorStyle( ROOT.kBlack )
    hists["data"].legendText   = "data" if not args.bkgSubstracted else "data (syst + total error)"
    hists["data"].legendOption = "ep" if args.bkgSubstracted else "p"

    
    
    hists["signal"].style        = styles.lineStyle( ROOT.kRed, width=5 )
    hists["signal"].legendText   = "signal ({})".format(args.cardfile) if not args.bkgSubstracted else "signal"
    hists["signal"].legendOption = "ep" if args.bkgSubstracted else "ep"

    for h_key, h in hists.iteritems():
        if "total" in h_key or h_key not in processes: continue
        hists[h_key].legendText  = processes[h_key]["texName"]
        hists[h_key].style = styles.fillStyle( processes[h_key]["color"], errors=False )
        hists[h_key].LabelsOption("v","X")

    # some settings and things like e.g. uncertainty boxes
    minMax             = 0.6
    if not args.bkgSubstracted: boxes, ratio_boxes = getUncertaintyBoxes( hists["total_background"], minMax )
    
    drawObjects_       = drawObjects( nBins=nBins, isData=(not args.expected), lumi_scale=lumi_scale, postFit=args.postFit, cardfile=args.substituteCard if args.substituteCard else args.cardfile, preliminary=args.preliminary )
    if not args.bkgSubstracted: drawObjects_ += boxes 
    #drawObjects_      += drawDivisions( crLabel, misIDPOI=("misIDPOI" in args.cardfile) ) 
    #drawObjects_      += drawPTDivisions( crLabel, ptLabels )

    histModifications  = []
    histModifications += [lambda h: h.GetYaxis().SetTitleSize(formatSettings(nBins)["textsize"])]
    histModifications += [lambda h: h.GetYaxis().SetLabelSize(formatSettings(nBins)["ylabelsize"])]
    histModifications += [lambda h: h.GetYaxis().SetTitleOffset(formatSettings(nBins)["textoffset"])]
    #histModifications += [ setPTBinLabels(ptLabels, crName, fac=formatSettings(nBins)["offsetfactor"]*hists["total"].GetMaximum())]

    ratioHistModifications  = []
    ratioHistModifications += [lambda h: h.GetYaxis().SetTitleSize(formatSettings(nBins)["textsize"])]
    ratioHistModifications += [lambda h: h.GetYaxis().SetLabelSize(formatSettings(nBins)["ylabelsize"])]
    ratioHistModifications += [lambda h: h.GetYaxis().SetTitleOffset(formatSettings(nBins)["textoffset"])]
    ratioHistModifications += [lambda h: h.GetXaxis().SetTitleSize(formatSettings(nBins)["textsize"])]
    ratioHistModifications += [lambda h: h.GetXaxis().SetLabelSize(formatSettings(nBins)["xlabelsize"])]
    ratioHistModifications += [lambda h: h.GetXaxis().SetLabelOffset(0.035)]

    # get histo list
    # plots_list = []
    # ratioHistos_list = []
    # for i in range (12) :
    #     plots_i, ratioHistos_i = Results.getRegionHistoList( hists[i], processes=processes, noData=False, sorted=sorted, bkgSubstracted=args.bkgSubstracted )

    #     plots_list.append(plots_i)
    #     ratioHistos_list.append(ratioHistos_i)
    #     # if args.bkgSubstracted: plots += [[hists["empty"]]]

    # plots = [item for sublist in plots_list for item in sublist]
    # ratioHistos = [item for sublist in ratioHistos_list for item in sublist]
    
    plots, ratioHistos = Results.getRegionHistoList( hists, processes=processes, noData=False, sorted=sorted, bkgSubstracted=args.bkgSubstracted )

    addon = []
    if args.bkgSubstracted: addon += ["bkgSub"]
    if args.substituteCard: addon += ["rebinned"] + [ cr for cr in args.substituteCard.split("_") if cr not in args.cardfile.split("_") ]
    if args.plotNuisances:  addon += args.plotNuisances
    if args.postFit:        addon += ["postFit"]

    # plot name
    if   args.plotRegions and args.plotChannels: plotName = "_".join( ["regions"] + addon + args.plotRegions + [ch for ch in args.plotChannels if not "tight" in ch] )
    elif args.plotRegions:                       plotName = "_".join( ["regions"] + addon + args.plotRegions )
    elif args.plotChannels:                      plotName = "_".join( ["regions"] + addon + [ch for ch in args.plotChannels if not "tight" in ch] )
    else:                                        plotName = "_".join( ["controlRegions"] + addon )
    
    
    plotting.draw(
        Plot.fromHisto( plotName,
                plots,
                texX = "",
                texY = "Observed - Background" if args.bkgSubstracted else "Number of Events",
        ),
        logX = False, logY = True, sorting = False, 
        plot_directory    = plotDirectory,
        legend            = [ (0.2, 0.86 if args.bkgSubstracted else formatSettings(nBins)["legylower"], 0.9, 0.9), formatSettings(nBins)["legcolumns"] ],
        widths            = { "x_width":formatSettings(nBins)["padwidth"], "y_width":formatSettings(nBins)["padheight"], "y_ratio_width":formatSettings(nBins)["padratio"] },
        yRange            = ( 0.01, hists["total"].GetMaximum()*formatSettings(nBins)["heightFactor"] ),
        ratio             = { "yRange": ((1-minMax)*0.99, (1+minMax)*1.01), "texY":"Theory/Data" if args.bkgSubstracted else "Data/MC", "histos":ratioHistos, "drawObjects":ratio_boxes if not args.bkgSubstracted else [], "histModifications":ratioHistModifications },
        drawObjects       = drawObjects_,
        histModifications = histModifications,
        copyIndexPHP      = False,
        extensions = ["png", "pdf", "root"],# if args.bkgSubstracted else ["png"], # pdfs are quite large for sorted histograms (disco plot)
    )

    del hists

# covariance matrix 2D plot
def plotCovariance():
    # get the results
    covhist = Results.getCovarianceHisto( postFit=args.postFit, labelFormater=labelFormater )

    histModifications  = []
    histModifications += [lambda h:h.GetYaxis().SetLabelSize(12)]
    histModifications += [lambda h:h.GetXaxis().SetLabelSize(12)]
    histModifications += [lambda h:h.GetZaxis().SetLabelSize(0.03)]

    canvasModifications  = []
    canvasModifications += [lambda c:c.SetLeftMargin(0.25)]
    canvasModifications += [lambda c:c.SetBottomMargin(0.25)]

    for log in [True, False]:
        drawObjects_ = drawCoObjects( lumi_scale=lumi_scale, bkgOnly=args.bkgOnly, postFit=args.postFit, incl=("incl" in args.cardfile), preliminary=args.preliminary )
        plotName     = "_".join( ["covarianceMatrix", "log" if log else "lin"] )

        plotting.draw2D(
            Plot2D.fromHisto( plotName,
                [[covhist]],
                texX = "",
                texY = "",
            ),
        logX = False, logY = False, logZ = log, 
        plot_directory      = plotDirectory,
        widths              = {"x_width":800, "y_width":800},
        zRange              = (0.000001,1) if log else (0,1),
        drawObjects         = drawObjects_,
        histModifications   = histModifications,
        canvasModifications = canvasModifications,
        copyIndexPHP        = True,
    )

    del covhist

# correlation of nuisances 2D plot
def plotCorrelations( systOnly ):
    # get the results
    corrhist     = Results.getCorrelationHisto( systOnly=systOnly )
    drawObjects_ = drawCoObjects( lumi_scale=lumi_scale, bkgOnly=args.bkgOnly, postFit=args.postFit, incl=("incl" in args.cardfile), preliminary=args.preliminary )

    addon = ""
    if systOnly:      addon += "_systOnly"
    if args.bkgOnly:  addon += "_bkgOnly"

    histModifications   = []
    histModifications  += [lambda h:h.GetYaxis().SetLabelSize(12)]
    histModifications  += [lambda h:h.GetXaxis().SetLabelSize(12)]
    histModifications  += [lambda h:h.GetZaxis().SetLabelSize(0.03)]

    canvasModifications  = []
    canvasModifications += [lambda c:c.SetLeftMargin(0.25)]
    canvasModifications += [lambda c:c.SetBottomMargin(0.25)]

    drawObjects_ = drawCoObjects( lumi_scale=lumi_scale, bkgOnly=args.bkgOnly, postFit=args.postFit, incl=("incl" in args.cardfile), preliminary=args.preliminary )

    plotting.draw2D(
        Plot2D.fromHisto("correlationMatrix"+addon,
            [[corrhist]],
            texX = "",
            texY = "",
        ),
        logX = False, logY = False, logZ = False, 
        plot_directory      = plotDirectory, 
        widths              = {"x_width":800, "y_width":800},
        zRange              = (-1,1),
        drawObjects         = drawObjects_,
        histModifications   = histModifications,
        canvasModifications = canvasModifications,
        copyIndexPHP        = True,
    )

    del corrhist

# impact plot
def plotImpacts():
    Results.getImpactPlot( expected=args.expected, printPNG=True, cores=args.cores )


if args.plotRegionPlot:
    print "doplot"
    plotRegions( sorted=False )
if args.plotCovMatrix:
    print "do-covar"
    # plotCovariance()
if args.plotCorrelations and args.postFit:
    print "correlation"
    # plotCorrelations( systOnly=False )
    # plotCorrelations( systOnly=True )
if args.plotImpacts and args.postFit:
    print "plot impacts"
    plotImpacts()
