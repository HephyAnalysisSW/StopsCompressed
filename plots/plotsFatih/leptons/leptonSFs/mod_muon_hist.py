from ROOT import *
from math import *
import os, sys

#datatag = "2016_80X_v5"

#binning = [3.5, 5., 10., 20., 30., 45., 60., 120.]
binning = [3.5, 5., 10., 20., 25., 30., 40., 50., 60., 120.]
#etabinning = [0., 0.9, 1.2, 2.1, 2.4]
etabins = {
"0p9": "abseta<0.9",
"0p9_1p2": "abseta>=0.9&&abseta<1.2",
"1p2_2p1": "abseta>=1.2&&abseta<2.1",
"2p1_2p4": "abseta>=2.1&&abseta<2.4",
#"all": "abseta<2.4"
}

mode = "MC"
if len(sys.argv)>1: mode = sys.argv[1]
if mode != "Data" and mode != "MC":
    print "wrong mode"
    sys.exit()
    
stage = "IpIsoSpec"
if len(sys.argv)>2: stage = sys.argv[2]
if stage != "IpIso" and stage != "Id" and stage != "IpIsoSpec":
    print "wrong stage"
    sys.exit()

year = "2016"
if len(sys.argv)>3: year = sys.argv[3]
if year != "2016" and year != "2017" and year!= "2018":
	print "wrong year"
	sys.exit()

if year == "2016":
	datatag = "2016_80X_v5"
elif year =="2017":
	datatag = "2017_94X"
elif year =="2018":
	datatag = "2018_94_pre3"

def makeDir(path):
    if "." in path[-5:]:
        path = path.replace(os.path.basename(path),"")
        print path
    if os.path.isdir(path):
        return
    else:
        os.makedirs(path)

def gethist(t,cut,lowedge,highedge,tag,etabin):
    histname = "h_{0:.1f}_{1:.1f}_{3}_{2}".format(lowedge,highedge,tag,etabin)
#    histname = "h_{0:.1f}_{1:.1f}_{2}".format(lowedge,highedge,tag)
    histname = histname.replace(".","p")
    hz = TH1F(histname,"",60,60,120)
    t.Draw("mass>>"+histname,cut,"goff")
    return hz

if stage == "Id":
    ID = "TM&&dzPV<0.5&&dB<0.2&&abseta<2.4&&JetPtRatio>0.4&&JetBTagCSV<0.4&&segmentCompatibility>0.4"
    PASS = "Loose"
elif stage == "IpIso":
    ID = "Loose&&dzPV<0.5&&dB<0.2&&abseta<2.4"
    PASS = "((combRelIsoPF03dBeta*pt)<5||combRelIsoPF03dBeta<0.2)&&dB<0.02&&dzPV<0.1"
elif stage == "IpIsoSpec":
    ID = "Loose&&dzPV<0.5&&dB<0.2&&abseta<2.4&&JetPtRatio>0.4&&JetBTagCSV<0.4&&segmentCompatibility>0.4"
    PASS = "((combRelIsoPF03dBeta*pt)<5||combRelIsoPF03dBeta<0.2)&&dB<0.02&&dzPV<0.1"    

FAIL = "!("+PASS+")"

TRIGZ = "(tag_IsoMu27||tag_IsoMu24_eta2p1||tag_IsoTkMu27||tag_IsoTkMu24_eta2p1)"
EXTRZ = "pair_probeMultiplicity==1&&pair_deltaR>0.5&&tag_abseta<2.1&&abs(pair_dz)<1&&tag_pt>15&&tag_combRelIsoPF03dBeta<0.1&&(charge*tag_charge)==-1"

t = TChain("tpTree/fitter_tree")
#t.Add("/data/tnp/tnpJPsi_Run2012A.root")
#t.Add("/data/tnp/tnpJPsi_Run2012B.root")
#t.Add("/data/tnp/tnpJPsi_Run2012C.root")
#t.Add("/data/tnp/tnpJPsi_Run2012D.root")
#t.Add("/data/tnp/tnpJPsi_MC53X.root")

if year == "2016": 

	if mode =="Data":
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2016/80x_v5/data/TnPTree_80XRereco_Run2016B_GoldenJSON_Run276098to276384.root")
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2016/80x_v5/data/TnPTree_80XRereco_Run2016C_GoldenJSON_Run276098to276384.root")
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2016/80x_v5/data/TnPTree_80XRereco_Run2016D_GoldenJSON_Run276098to276384.root")
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2016/80x_v5/data/TnPTree_80XRereco_Run2016E_GoldenJSON_Run276098to276384.root")
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2016/80x_v5/data/TnPTree_80XRereco_Run2016F_GoldenJSON_Run276098to276384.root")
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2016/80x_v5/data/TnPTree_80XRereco_Run2016G_GoldenJSON_Run278819to280384.root")
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2016/80x_v5/data/TnPTree_80XRereco_Run2016H_GoldenJSON_Run284036to284044.root")
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2016/80x_v5/data/TnPTree_80XRereco_Run2016H_v2_GoldenJSON_Run281613to284035.root")
	else:
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2016/80x_v5/mc/MC_Moriond17_DY_tranch4Premix_part1.root")
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2016/80x_v5/mc/MC_Moriond17_DY_tranch4Premix_part2.root")
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2016/80x_v5/mc/MC_Moriond17_DY_tranch4Premix_part3.root")
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2016/80x_v5/mc/MC_Moriond17_DY_tranch4Premix_part4.root")
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2016/80x_v5/mc/MC_Moriond17_DY_tranch4Premix_part5.root")
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2016/80x_v5/mc/MC_Moriond17_DY_tranch4Premix_part6.root")
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2016/80x_v5/mc/MC_Moriond17_DY_tranch4Premix_part7.root")
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2016/80x_v5/mc/MC_Moriond17_DY_tranch4Premix_part8.root")
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2016/80x_v5/mc/MC_Moriond17_DY_tranch4Premix_part9.root")
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2016/80x_v5/mc/MC_Moriond17_DY_tranch4Premix_part10.root")
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2016/80x_v5/mc/MC_Moriond17_DY_tranch4Premix_part11.root")
elif year =="2017":
	if mode == "Data":
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2017/94X/Data/TnPTree_17Nov2017_SingleMuon_Run2017Bv1_Full_GoldenJSON.root")
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2017/94X/Data/TnPTree_17Nov2017_SingleMuon_Run2017Cv1_Full_GoldenJSON.root")
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2017/94X/Data/TnPTree_17Nov2017_SingleMuon_Run2017Dv1_Full_GoldenJSON.root")
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2017/94X/Data/TnPTree_17Nov2017_SingleMuon_Run2017Ev1_Full_GoldenJSON.root")
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2017/94X/Data/TnPTree_17Nov2017_SingleMuon_Run2017Fv1_Full_GoldenJSON.root")
	else:
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2017/94X/MC/TnPTree_94X_DYJetsToLL_M50_Madgraph.root")
elif year == "2018":
	if mode == "Data":
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2018/94_pre3/TnPTreeZ_17Sep2018_SingleMuon_Run2018Av2_GoldenJSON.root")
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2018/94_pre3/TnPTreeZ_17Sep2018_SingleMuon_Run2018Bv1_GoldenJSON.root")
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2018/94_pre3/TnPTreeZ_17Sep2018_SingleMuon_Run2018Cv1_GoldenJSON.root")
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2018/94_pre3/TnPTreeZ_SingleMuon_Run2018Dv2_GoldenJSON_Upto323523.root")
	else:
	    t.Add("/scratch/priya.hussain/StopsCompressed/TnP/Run2018/94_pre3/TnPTreeZ_102XAutumn18_DYJetsToLL_M50_MadgraphMLM.root")

makeDir("/scratch/priya.hussain/StopsCompressed/results/%s/hists"%datatag) 
#fout = TFile("/scratch/priya.hussain/StopsCompressed/results/%s/hists/mu_hists_%s_%s.root"%(datatag,mode,stage),"recreate")
fout = TFile("/scratch/priya.hussain/StopsCompressed/results/%s/hists/mu_hists_%s_%s.root"%(datatag,mode,stage),"update")

hlist = []

for ipt in range(len(binning)-1):
    ptlow = binning[ipt]
    pthigh = binning[ipt+1]
    PTCUT = "pt>{0:f}&&pt<={1:f}".format(ptlow,pthigh)
    print ptlow,pthigh

    for etabin,etacut in etabins.items():
	print "eta dict: ", etabin, etacut
        cut = "&&".join([TRIGZ,ID,EXTRZ,PTCUT,etacut])
	print etabin, cut
        hlist.append(gethist(t,"&&".join([cut,PASS]),ptlow,pthigh,"pass",etabin))
        hlist.append(gethist(t,"&&".join([cut,FAIL]),ptlow,pthigh,"fail",etabin))
    

fout.Write()
fout.Close()


