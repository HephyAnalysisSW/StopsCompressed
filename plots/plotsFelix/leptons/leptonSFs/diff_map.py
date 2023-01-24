import ROOT
import os, sys
import array
import numpy as np

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
if year != "2016" and year != "2017" and year != "2018":
    print "wrong year"
    sys.exit()

vfp  = "postVFP"
if len(sys.argv)>5: vfp = sys.argv[5]
if vfp != "preVFP" and vfp != "postVFP":
    print "wrong vfp"
    sys.exit()

if year == "2016":
    if vfp == "preVFP":
        datatag = "2016_80X_v5_preVFP"
    else:
        datatag = "2016_80X_v5_postVFP"
elif year == "2017":
	datatag ="2017_94X"
elif year == "2018":
	datatag ="2018_94_pre3"

inputFile = "/groups/hephy/cms/felix.lang/StopsCompressed/results/%s/finalplots/%s.root"%(datatag,inputFileName)
if not os.path.isfile(inputFile):
    print "input file %s does not exist"%inputFile
    sys.exit()

suffix = "_%s_%s_%s"%(inputFileName, flavor, stage)

f = ROOT.TFile(inputFile, "update")

h = {}
if flavor == 'muon':
    for etabin in ['0p9', '0p9_1p2', ' 1p2_2p1', '2p1_2p4']:
        h[etabin] = f.Get("%s_SF_%s_%s"%(flavor,stage,etabin))
else:
    for etabin in ['0p8', '0p8_1p4', '1p4_1p5', '1p5_2p0','2p0_2p5', 'm0p8', 'm0p8_m1p4', 'm1pm4_m1p5','m1p5_m2p0','m2p0_m2p5']:
        h[etabin] = f.Get("%s_SF_%s_%s"%(flavor,stage,etabin))

if flavor == "muon":
    nx = h['0p9'].GetNbinsX()
    ptbins = h['0p9'].GetXaxis().GetXbins().GetArray()
    etabins = array.array("d", [0., 0.9, 1.2, 2.1, 2.4])

else:
    nx = h['0p8'].GetNbinsX()
    ptbins = h['0p8'].GetXaxis().GetXbins().GetArray()
    #ptbins = array.array("d", [10., 20., 35., 50., 100., 200., 500])
    #print ptbins
    etabins = array.array("d", [-2.5, -2.0, -1.566, -1.422, -0.8, 0., 0.8, 1.442, 1.566, 2.0, 2.5])

# if flavor == "muon":
#     SF = ROOT.TH2F(histName, histName, nx, ptbins, len(etabins)-1, etabins)
#     SF.SetTitle(histName)
#     SF.GetXaxis().SetTitle("p_{T} (GeV)")
#     SF.GetYaxis().SetTitle("|#eta|")
#     SF.GetZaxis().SetTitle("SF")
#     SF.GetXaxis().SetTitleOffset(1.2)
#     SF.GetYaxis().SetTitleOffset(1.2)
#     SF.GetZaxis().SetTitleOffset(1.2)
#     SF.GetZaxis().SetRangeUser(0.94, 1.06)
#     SF.SetMarkerSize(0.8)
#     for i in range(nx):
#         i+=1
#         SF.SetBinContent(i, 1, h['0p9'].GetBinContent(i))
#         print "value for 1st", h['0p9'].GetBinContent(i)
#         SF.SetBinError(i,   1, h['0p9'].GetBinError(i))
#
#         SF.SetBinContent(i, 2, h['0p9_1p2'].GetBinContent(i))
#         print "value for 2nd", h['0p9_1p2'].GetBinContent(i)
#         SF.SetBinError(i,   2, h['0p9_1p2'].GetBinError(i))
#
#         SF.SetBinContent(i, 3, h['1p2_2p1'].GetBinContent(i))
#         print "value for 3rd", h['1p2_2p1'].GetBinContent(i)
#         SF.SetBinError(i,   3, h['1p2_2p1'].GetBinError(i))
#
#         SF.SetBinContent(i, 4, h['2p1_2p4'].GetBinContent(i))
#         print "value for 4th", h['2p1_2p4'].GetBinContent(i)
#         SF.SetBinError(i,   4, h['2p1_2p4'].GetBinError(i))
# else:
#     SF = ROOT.TH2F(histName, histName , len(etabins)-1, etabins, nx, ptbins)
#     SF.SetTitle(histName)
#     SF.GetYaxis().SetTitle("p_{T} (GeV)")
#     SF.GetXaxis().SetTitle("|#eta|")
#     SF.GetZaxis().SetTitle("SF")
#     SF.GetXaxis().SetTitleOffset(1.2)
#     SF.GetYaxis().SetTitleOffset(1.2)
#     SF.GetZaxis().SetTitleOffset(1.2)
#     SF.GetZaxis().SetRangeUser(0.94, 1.06)
#     #keeping same z scale for comparison
#     #SF.GetZaxis().SetRangeUser(0.75,1.25)
#     SF.SetMarkerSize(0.8)
#
#     for i in range(nx):
#         i+=1
#         SF.SetBinContent(1, i, h['m2p0_m2p5'].GetBinContent(i))
#         print "value for 1st", h['m2p0_m2p5'].GetBinContent(i)
#         a =
#         SF.SetBinError(1,   i, h['m2p0_m2p5'].GetBinError(i))
#
#         SF.SetBinContent(2, i, h['m1p5_m2p0'].GetBinContent(i))
#         print "value for 2nd", h['m1p5_m2p0'].GetBinContent(i)
#         SF.SetBinError(2,   i, h['m1p5_m2p0'].GetBinError(i))
#
#         # SF.SetBinContent(3, i, h['m1pm4_m1p5'].GetBinContent(i))
#         # print "value for 3rd", h['m1pm4_m1p5'].GetBinContent(i)
#         # SF.SetBinError(3,   i, h['m1pm4_m1p5'].GetBinError(i))
#
#         SF.SetBinContent(3, i, 0)
#         print "value for 3rd", 0
#         SF.SetBinError(3,   i, 0)
#
#         SF.SetBinContent(4, i, h['m0p8_m1p4'].GetBinContent(i))
#         print "value for 4th", h['m0p8_m1p4'].GetBinContent(i)
#         SF.SetBinError(4,   i, h['m0p8_m1p4'].GetBinError(i))
#
#         SF.SetBinContent(5, i, h['m0p8'].GetBinContent(i))
#         print "value for 5th", h['m0p8'].GetBinContent(i)
#         SF.SetBinError(5,   i, h['m0p8'].GetBinError(i))
#
#         SF.SetBinContent(6, i, h['0p8'].GetBinContent(i))
#         print "value for 6th", h['0p8'].GetBinContent(i)
#         SF.SetBinError(6,   i, h['0p8'].GetBinError(i))
#
#         SF.SetBinContent(7, i, h['0p8_1p4'].GetBinContent(i))
#         print "value for 7th", h['0p8_1p4'].GetBinContent(i)
#         SF.SetBinError(7,   i, h['0p8_1p4'].GetBinError(i))
#
#         # SF.SetBinContent(8, i, h['1p4_1p5'].GetBinContent(i))
#         # print "value for 8th", h['1p4_1p5'].GetBinContent(i)
#         # SF.SetBinError(8,   i, h['1p4_1p5'].GetBinError(i))
#
#         SF.SetBinContent(8, i, 0)
#         print "value for 8th", 0
#         SF.SetBinError(8,   i, 0)
#
#         SF.SetBinContent(9, i, h['1p5_2p0'].GetBinContent(i))
#         print "value for 9th", h['1p5_2p0'].GetBinContent(i)
#         SF.SetBinError(9,   i, h['1p5_2p0'].GetBinError(i))
#
#         SF.SetBinContent(10, i, h['2p0_2p5'].GetBinContent(i))
#         print "value for 10th", h['2p0_2p5'].GetBinContent(i)
#         SF.SetBinError(10,   i, h['2p0_2p5'].GetBinError(i))

if flavor == "muon":
    matrix = np.array[[h['m2p0_m2p5'].GetBinContent(i+1) for i in range(nx)] for j in ['0p9', '0p9_1p2', ' 1p2_2p1', '2p1_2p4']]
else:
    matrix = np.array[[h['m2p0_m2p5'].GetBinContent(i+1) for i in range(nx)] for j in ['0p8', '0p8_1p4', '1p4_1p5', '1p5_2p0','2p0_2p5', 'm0p8', 'm0p8_m1p4', 'm1pm4_m1p5','m1p5_m2p0','m2p0_m2p5']]
    if year == 2018:
        lit = np.array[[1.006, 1.018, 1.000, 1.013, 1.000, 1.005, 1.007, 1.000, 0.996, 0.980],
                       [1.007, 1.002, 1.000, 1.010, 1.001, 1.007, 1.008, 1.000, 1.001, 0.995],
                       [0.994, 0.994, 1.000, 0.984, 0.989, 0.990, 0.983, 1.000, 0.994, 0.987],
                       [0.998, 0.994, 1.000, 0.984, 0.988, 0.989, 0.984, 1.000, 0.992, 0.992],
                       [1.000, 0.990, 1.000, 0.975, 0.982, 0.984, 0.977, 1.000, 0.984, 0.994],
                       [1.038, 1.027, 1.000, 1.013, 0.985, 0.968, 1.014, 1.000, 1.018, 1.027]]

print (matrix)
print (lit)

