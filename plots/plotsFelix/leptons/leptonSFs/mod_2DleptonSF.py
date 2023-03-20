import ROOT
import os, sys
import array

import time
import numpy as np
from itertools import product

ROOT.gStyle.SetOptStat(0) #1111 adds histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis

inputFileName = "hephy_scale_factors"
if len(sys.argv)>1: inputFileName = sys.argv[1]
#inputFile = "/scratch/priya.hussain/StopsCompressed/results/2017_94X/finalplots/noIso/%s.root"%inputFileName
#inputFile = "/groups/hephy/cms/felix.lang/StopsCompressed/results/%s/finalplots/%s.root"%(datatag,inputFileName)
#inputFile = "/scratch/priya.hussain/StopsCompressed/results/2018_94_pre3/finalplots/noIso/%s.root"%inputFileName
#inputFile = "/scratch/priya.hussain/StopsCompressed/results/2016_80X_v5/finalplots/cent/%s.root"%inputFileName
#inputFile = "/scratch/priya.hussain/StopsCompressed/results/2016_80X_v5/finalplots/legacy/%s.root"%inputFileName
# if not os.path.isfile(inputFile):
#     print "input file %s does not exist"%inputFile
#     sys.exit()

flavor = "ele"
if len(sys.argv)>2: flavor = sys.argv[2]
if flavor != "muon" and flavor != "ele":
    print "wrong flavor"
    sys.exit()

stage = "Id"
if len(sys.argv)>3: stage = sys.argv[3]
if stage != "IpIso" and stage != "Id" and stage != "IdSpec" and stage != "IpIsoSpec":
    print "wrong stage"
    sys.exit()

year = "2017"
if len(sys.argv)>4: year = sys.argv[4]
if year != "2016preVFP" and year != "2016postVFP" and year != "2017" and year != "2018":
    print "wrong year"
    sys.exit()

if year == "2016preVFP":
    datatag = "2016_80X_v5_preVFP"
elif year == "2016postVFP":
    datatag = "2016_80X_v5_postVFP"
elif year == "2017":
	datatag ="2017_94X"
elif year == "2018":
	datatag ="2018_94_pre3"

inputFile = "/groups/hephy/cms/felix.lang/StopsCompressed/results/%s/finalplots/%s_%s.root"%(datatag,inputFileName,flavor)
if not os.path.isfile(inputFile):
    print "input file %s does not exist"%inputFile
    sys.exit()

suffix = "_%s_%s_%s"%(inputFileName, flavor, stage)

f = ROOT.TFile(inputFile, "update")

h = {}
if flavor == 'muon':
    for etabin in ['0p9', '0p9_1p2', '1p2_2p1', '2p1_2p4']:
        h[etabin] = f.Get("%s_SF_%s_%s"%(flavor,stage,etabin))
        print h[etabin]
else:
    for etabin in ['0p8', '0p8_1p4', '1p4_1p5', '1p5_2p0','2p0_2p5', 'm0p8', 'm0p8_m1p4', 'm1pm4_m1p5','m1p5_m2p0','m2p0_m2p5']:
        h[etabin] = f.Get("%s_SF_%s_%s"%(flavor,stage,etabin))
        print h[etabin]

def makeDir(path):
    if "." in path[-5:]:
        path = path.replace(os.path.basename(path),"")
    if os.path.isdir(path):
        return
    else:
        os.makedirs(path)

# get binning
if flavor == "muon":
    nx = h['0p9'].GetNbinsX()
    ptbins = h['0p9'].GetXaxis().GetXbins().GetArray()

    etabins = array.array("d", [0., 0.9, 1.2, 2.1, 2.4])
    print len(etabins)
else:
    nx = h['0p8'].GetNbinsX()
    ptbins = h['0p8'].GetXaxis().GetXbins().GetArray()
    #ptbins = array.array("d", [10., 20., 35., 50., 100., 200., 500])
    #print ptbins
    etabins = array.array("d", [-2.5, -2.0, -1.566, -1.422, -0.8, 0., 0.8, 1.442, 1.566, 2.0, 2.5])


# 2D SF plot
histName = "%s_SF_%s_2D"%(flavor,stage)
#SF = ROOT.TH2F(histName, histName, nx, ptbins, len(etabins)-1, etabins)
#SF.SetTitle(histName)
#SF.GetXaxis().SetTitle("p_{T} (GeV)")
#SF.GetYaxis().SetTitle("|#eta|")
#SF.GetZaxis().SetTitle("SF")
#SF.GetXaxis().SetTitleOffset(1.2)
#SF.GetYaxis().SetTitleOffset(1.2)
#SF.GetZaxis().SetTitleOffset(1.2)
#SF.GetZaxis().SetRangeUser(0.6,1)
#SF.SetMarkerSize(0.8)

if flavor == "muon":
    SF = ROOT.TH2F(histName, histName, len(etabins)-1, etabins, nx, ptbins)
    SF.SetTitle(histName)
    SF.GetYaxis().SetTitle("p_{T} (GeV)")
    SF.GetXaxis().SetTitle("|#eta|")
    SF.GetZaxis().SetTitle("SF")
    SF.GetXaxis().SetTitleOffset(1.2)
    SF.GetYaxis().SetTitleOffset(1.2)
    SF.GetZaxis().SetTitleOffset(1.2)
    #SF.GetZaxis().SetRangeUser(0.2, 1.5)
    SF.SetMarkerSize(0.8)
    for i in range(nx):
        i+=1
        SF.SetBinContent(1, i, round(h['0p9'].GetBinContent(i), 5))
        print "value for 1st", h['0p9'].GetBinContent(i)
        SF.SetBinError(1,   i, round(h['0p9'].GetBinError(i), 5))

        SF.SetBinContent(2, i, round(h['0p9_1p2'].GetBinContent(i), 5))
        print "value for 2nd", h['0p9_1p2'].GetBinContent(i)
        SF.SetBinError(2,   i, round(h['0p9_1p2'].GetBinError(i), 5))

        SF.SetBinContent(3, i, round(h['1p2_2p1'].GetBinContent(i), 5))
        print "value for 3rd", h['1p2_2p1'].GetBinContent(i)
        SF.SetBinError(3,   i, round(h['1p2_2p1'].GetBinError(i), 5))

        SF.SetBinContent(4, i, round(h['2p1_2p4'].GetBinContent(i), 5))
        print "value for 4th", h['2p1_2p4'].GetBinContent(i)
        SF.SetBinError(4,   i, round(h['2p1_2p4'].GetBinError(i), 5))
else:
    SF = ROOT.TH2F(histName, histName , len(etabins)-1, etabins, nx, ptbins)
    SF.SetTitle(histName)
    SF.GetYaxis().SetTitle("p_{T} (GeV)")
    SF.GetXaxis().SetTitle("|#eta|")
    SF.GetZaxis().SetTitle("SF")
    SF.GetXaxis().SetTitleOffset(1.2)
    SF.GetYaxis().SetTitleOffset(1.2)
    SF.GetZaxis().SetTitleOffset(1.2)
    #SF.GetZaxis().SetRangeUser(0.94, 1.06)
    #keeping same z scale for comparison
    #SF.GetZaxis().SetRangeUser(0.75,1.25)
    SF.SetMarkerSize(0.8)

    for i in range(nx):
        i+=1
        SF.SetBinContent(1, i, round(h['m2p0_m2p5'].GetBinContent(i), 5))
        print "value for 1st", h['m2p0_m2p5'].GetBinContent(i)
        SF.SetBinError(1,   i, round(h['m2p0_m2p5'].GetBinError(i), 5))

        SF.SetBinContent(2, i, round(h['m1p5_m2p0'].GetBinContent(i), 5))
        print "value for 2nd", h['m1p5_m2p0'].GetBinContent(i)
        SF.SetBinError(2,   i, round(h['m1p5_m2p0'].GetBinError(i), 5))

        # SF.SetBinContent(3, i, h['m1pm4_m1p5'].GetBinContent(i))
        # print "value for 3rd", h['m1pm4_m1p5'].GetBinContent(i)
        # SF.SetBinError(3,   i, h['m1pm4_m1p5'].GetBinError(i))

        SF.SetBinContent(3, i, 0)
        print "value for 3rd", 0
        SF.SetBinError(3,   i, 0)

        SF.SetBinContent(4, i, round(h['m0p8_m1p4'].GetBinContent(i), 5))
        print "value for 4th", h['m0p8_m1p4'].GetBinContent(i)
        SF.SetBinError(4,   i, round(h['m0p8_m1p4'].GetBinError(i), 5))

        SF.SetBinContent(5, i, round(h['m0p8'].GetBinContent(i), 5))
        print "value for 5th", h['m0p8'].GetBinContent(i)
        SF.SetBinError(5,   i, round(h['m0p8'].GetBinError(i), 5))

        SF.SetBinContent(6, i, round(h['0p8'].GetBinContent(i), 5))
        print "value for 6th", h['0p8'].GetBinContent(i)
        SF.SetBinError(6,   i, round(h['0p8'].GetBinError(i), 5))

        SF.SetBinContent(7, i, round(h['0p8_1p4'].GetBinContent(i), 5))
        print "value for 7th", h['0p8_1p4'].GetBinContent(i)
        SF.SetBinError(7,   i, round(h['0p8_1p4'].GetBinError(i), 5))

        # SF.SetBinContent(8, i, h['1p4_1p5'].GetBinContent(i))
        # print "value for 8th", h['1p4_1p5'].GetBinContent(i)
        # SF.SetBinError(8,   i, h['1p4_1p5'].GetBinError(i))

        SF.SetBinContent(8, i, 0)
        print "value for 8th", 0
        SF.SetBinError(8,   i, 0)

        SF.SetBinContent(9, i, round(h['1p5_2p0'].GetBinContent(i), 5))
        print "value for 9th", h['1p5_2p0'].GetBinContent(i)
        SF.SetBinError(9,   i, round(h['1p5_2p0'].GetBinError(i), 5))

        SF.SetBinContent(10, i, round(h['2p0_2p5'].GetBinContent(i), 5))
        print "value for 10th", h['2p0_2p5'].GetBinContent(i)
        SF.SetBinError(10,   i, round(h['2p0_2p5'].GetBinError(i), 5))

#c = ROOT.TCanvas("c", "Canvas", 1800, 1500)
c = ROOT.TCanvas("c", "Canvas", 1800, 1500)
ROOT.gStyle.SetPalette(1)
levelslow = [0, 0.94]
levelshigh = [0.94 + (idx+1) * 0.006 for idx in range(20)]
levelslow.extend(levelshigh)
levels = array.array("d", levelslow)
SF.SetContour(len(levels), levels)
SF.Draw("COLZ TEXT45E") #CONT1-5 #plots the graph with axes and points
SF.GetZaxis().SetRangeUser(0.0, 1.2)

#if logy: ROOT.gPad.SetLogz()
ROOT.gPad.SetLogy()
c.Modified()
c.Update()

if year == "2016preVFP":
    savedir = "/groups/hephy/cms/felix.lang/www/StopsCompressed/TnP/final/2016_80X_v5_preVFP/2DleptonSF"
if year == "2016postVFP":
    savedir = "/groups/hephy/cms/felix.lang/www/StopsCompressed/TnP/final/2016_80X_v5_postVFP/2DleptonSF"
elif year == "2017":
    savedir = "/groups/hephy/cms/felix.lang/www/StopsCompressed/TnP/final/2017_94X/2DleptonSF"
elif year == "2018":
    savedir = "/groups/hephy/cms/felix.lang/www/StopsCompressed/TnP/final/2018_94_pre3/2DleptonSF"

#Save canvas
#savedir = "/groups/hephy/cms/felix.lang/www/StopsCompressed/TnP/final/2017_94X/2DleptonSF"
#savedir = "/groups/hephy/cms/felix.lang/www/StopsCompressed/TnP/final/2017_94X/2DleptonSF"
#savedir = "/groups/hephy/cms/felix.lang/www/StopsCompressed/TnP/final/2018_94_pre3/2DleptonSF/noIso"
#savedir = "/groups/hephy/cms/felix.lang/www/StopsCompressed/TnP/final/2016_80X_v5/2DleptonSF/legacy/comp"
#savedir = "/groups/hephy/cms/felix.lang/www/StopsCompressed/TnP/final/2016_80X_v5/2DleptonSF/mod"

makeDir(savedir)
makeDir(savedir + '/root')
makeDir(savedir + '/pdf')

c.SaveAs("%s/2DleptonSF%s.png"      %(savedir, suffix))
c.SaveAs("%s/pdf/2DleptonSF%s.pdf"  %(savedir, suffix))
c.SaveAs("%s/root/2DleptonSF%s.root"%(savedir, suffix))

# adds histogram to original file
f.Write(histName, ROOT.TObject.kOverwrite)
f.Close()
