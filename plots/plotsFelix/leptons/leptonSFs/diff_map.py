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

inputFile = "/groups/hephy/cms/felix.lang/StopsCompressed/results/%s/finalplots/%s_%s.root"%(datatag,inputFileName,flavor)
if not os.path.isfile(inputFile):
    print "input file %s does not exist"%inputFile
    sys.exit()

def makeDir(path):
    if "." in path[-5:]:
        path = path.replace(os.path.basename(path),"")
    if os.path.isdir(path):
        return
    else:
        os.makedirs(path)

histName = "%s_SF_%s_2D"%(flavor,stage)

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
    #ptbins = h['0p9'].GetXaxis().GetXbins().GetArray()
    ptbins = array.array("d", [10., 20., 35., 50., 100., 200., 500])
    etabins = array.array("d", [0., 0.9, 1.2, 2.1, 2.4])

else:
    nx = h['0p8'].GetNbinsX()
    #ptbins = h['0p8'].GetXaxis().GetXbins().GetArray()
    ptbins = array.array("d", [10., 20., 35., 50., 100., 200., 500])
    #print ptbins
    etabins = array.array("d", [-2.5, -2.0, -1.566, -1.422, -0.8, 0., 0.8, 1.442, 1.566, 2.0, 2.5])

if flavor == "muon":
    matrix = np.array([[h[i].GetBinContent(nx-j) for i in ['0p9', '0p9_1p2', ' 1p2_2p1', '2p1_2p4']] for j in range(nx)])
else:
    matrix = np.array([[h[i].GetBinContent(nx-j) for i in ['m2p0_m2p5','m1p5_m2p0','m1pm4_m1p5','m0p8_m1p4','m0p8','0p8','0p8_1p4','1p4_1p5','1p5_2p0','2p0_2p5']] for j in range(nx)])
    if year == "2016":
        if vfp == "preVFP":
            lit = np.array([[1.012, 1.026, 1.000, 0.999, 0.997, 1.005, 1.009, 1.000, 0.995, 1.016],
                            [1.012, 1.026, 1.000, 0.999, 0.997, 1.005, 1.009, 1.000, 0.995, 1.016],
                            [1.001, 1.000, 1.000, 0.990, 0.983, 0.990, 0.994, 1.000, 1.001, 0.988],
                            [1.000, 1.001, 1.000, 0.993, 0.984, 0.990, 0.995, 1.000, 1.001, 0.996],
                            [1.003, 1.000, 1.000, 0.992, 0.985, 0.988, 0.998, 1.000, 0.998, 0.998],
                            [1.036, 1.032, 1.000, 1.024, 0.980, 0.967, 1.052, 1.000, 1.024, 1.051]])
            factors = np.abs(matrix[:-1] / lit - 1) * 100
        else:
            lit = np.array([[1.018, 1.018, 1.000, 1.007, 1.010, 1.003, 1.007, 1.000, 0.990, 1.006],
                            [1.018, 1.018, 1.000, 1.007, 1.010, 1.003, 1.007, 1.000, 0.990, 1.006],
                            [0.987, 1.001, 1.000, 0.989, 0.989, 0.992, 0.990, 1.000, 0.994, 0.983],
                            [0.992, 0.997, 1.000, 0.990, 0.989, 0.991, 0.992, 1.000, 0.994, 0.989],
                            [0.993, 0.992, 1.000, 0.988, 0.983, 0.987, 0.986, 1.000, 0.981, 0.991],
                            [1.022, 1.015, 1.000, 1.005, 0.970, 0.976, 1.014, 1.000, 1.029, 1.015]])
            factors = np.abs(matrix[:-1] / lit - 1) * 100
    elif year == "2017":
        lit = np.array([[1.051, 1.019, 1.000, 1.009, 1.020, 1.010, 1.026, 1.000, 0.989, 1.040],
                        [0.996, 1.001, 1.000, 1.006, 1.003, 1.003, 1.001, 1.000, 1.006, 1.003],
                        [0.997, 0.997, 1.000, 0.988, 0.988, 0.992, 0.990, 1.000, 0.997, 0.991],
                        [0.997, 0.994, 1.000, 0.989, 0.989, 0.991, 0.990, 1.000, 0.993, 1.000],
                        [0.991, 0.996, 1.000, 0.985, 0.981, 0.987, 0.990, 1.000, 0.993, 0.993],
                        [1.024, 1.036, 1.000, 1.029, 0.986, 0.990, 1.018, 1.000, 1.030, 1.060]])
        factors = np.abs(matrix[:-1] / lit - 1) * 100
    elif year == "2018":
        lit = np.array([[1.006, 1.018, 1.000, 1.013, 1.000, 1.005, 1.007, 1.000, 0.996, 0.980],
                       [1.007, 1.002, 1.000, 1.010, 1.001, 1.007, 1.008, 1.000, 1.001, 0.995],
                       [0.994, 0.994, 1.000, 0.984, 0.989, 0.990, 0.983, 1.000, 0.994, 0.987],
                       [0.998, 0.994, 1.000, 0.984, 0.988, 0.989, 0.984, 1.000, 0.992, 0.992],
                       [1.000, 0.990, 1.000, 0.975, 0.982, 0.984, 0.977, 1.000, 0.984, 0.994],
                       [1.038, 1.027, 1.000, 1.013, 0.985, 0.968, 1.014, 1.000, 1.018, 1.027]])
        factors = np.abs(matrix[:-1]/lit - 1) * 100

if flavor == "muon":
    SF = ROOT.TH2F(histName, histName, nx, ptbins, len(etabins)-1, etabins)
    SF.SetTitle(histName)
    SF.GetXaxis().SetTitle("p_{T} (GeV)")
    SF.GetYaxis().SetTitle("|#eta|")
    SF.GetZaxis().SetTitle("difference (%)")
    SF.GetXaxis().SetTitleOffset(1.2)
    SF.GetYaxis().SetTitleOffset(1.2)
    SF.GetZaxis().SetTitleOffset(1.2)
    #SF.GetZaxis().SetRangeUser(-5, 15)
    SF.SetMarkerSize(0.8)
    for i in range(nx-1):
        for j in range(4):
            SF.SetBinContent(j+1, i+1, factors[i][j])

else:
    SF = ROOT.TH2F(histName, histName , len(etabins)-1, etabins, nx-1, ptbins)
    SF.SetTitle(histName)
    SF.GetYaxis().SetTitle("p_{T} (GeV)")
    SF.GetXaxis().SetTitle("|#eta|")
    SF.GetZaxis().SetTitle("SF")
    SF.GetXaxis().SetTitleOffset(1.2)
    SF.GetYaxis().SetTitleOffset(1.2)
    SF.GetZaxis().SetTitleOffset(1.2)
    #SF.GetZaxis().SetRangeUser(0.94, 1.06)
    #keeping same z scale for comparison
    SF.SetMarkerSize(0.8)

    for i in range(nx-1):
        for j in range(10):
            if j == 2 or j == 7:
                SF.SetBinContent(j+1, i+1, 1)
                continue
            SF.SetBinContent(j+1, i+1, factors[i][j])
            print(factors[i][j])
            #SF.SetBinError(j+1, i+1, 0)


c = ROOT.TCanvas("c", "Canvas", 1800, 1500)

c = ROOT.TCanvas("c", "Canvas", 1800, 1500)
ROOT.gStyle.SetPalette(1)
SF.Draw("COLZ TEXT89") #CONT1-5 #plots the graph with axes and points

#if logy: ROOT.gPad.SetLogz()
ROOT.gPad.SetLogy()
c.Modified()
c.Update()

if year == "2016":
    if vfp == "preVFP":
        savedir = "/groups/hephy/cms/felix.lang/www/StopsCompressed/TnP/final/2016_80X_v5_preVFP/2DleptonSF_diff"
    else:
        savedir = "/groups/hephy/cms/felix.lang/www/StopsCompressed/TnP/final/2016_80X_v5_postVFP/2DleptonSF_diff"
elif year == "2017":
    savedir = "/groups/hephy/cms/felix.lang/www/StopsCompressed/TnP/final/2017_94X/2DleptonSF_diff"
elif year == "2018":
    savedir = "/groups/hephy/cms/felix.lang/www/StopsCompressed/TnP/final/2018_94_pre3/2DleptonSF_diff"

makeDir(savedir)
makeDir(savedir + '/root')
makeDir(savedir + '/pdf')

c.SaveAs("%s/2DleptonSF%s.png"      %(savedir, suffix))
c.SaveAs("%s/pdf/2DleptonSF%s.pdf"  %(savedir, suffix))
c.SaveAs("%s/root/2DleptonSF%s.root"%(savedir, suffix))

f.Close()