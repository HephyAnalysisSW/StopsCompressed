from ROOT import *
from math import *
import os,sys

#datatag = "2016_80X_v5"

binning = [5., 10., 20., 35., 50., 100., 200., 500]
#etabinning = [0., 0.8, 1.442, 1.566, 2.0, 2.5]
etabins = {
"0p8"	 : "el_sc_eta>=0&&el_sc_eta<0.8",
"0p8_1p4": "el_sc_eta>=0.8&&el_sc_eta<1.442",
#"1p4_1p5": "el_sc_eta>=1.442&&el_sc_eta<1.566",
"1p5_2p0": "el_sc_eta>=1.566&&el_sc_eta<2.0",
"2p0_2p5": "el_sc_eta>=2.0&&el_sc_eta<2.5",
"m0p8"	 : "el_sc_eta>=-0.8&&el_sc_eta<0",
"m0p8_m1p4": "el_sc_eta>=-1.442&&el_sc_eta<-0.8",
#"m1pm4_m1p5": "el_sc_eta>=-1.566&&el_sc_eta<-1.442",
"m1p5_m2p0": "el_sc_eta>=-2.0&&el_sc_eta<-1.566",
"m2p0_m2p5": "el_sc_eta>=-2.5&&el_sc_eta<-2.0",
"all"	 : "el_sc_eta>=-2.5&&el_sc_eta<=2.5"
}

mode = "Data"
if len(sys.argv)>1: mode = sys.argv[1]
if mode != "Data" and mode != "MC":
    print "wrong mode"
    sys.exit()

stage = "IdSpec"
#stage = "IpIso"
if len(sys.argv)>2: stage = sys.argv[2]
if stage != "IpIso" and stage != "Id" and stage != "IdSpec":
    print "wrong stage"
    sys.exit()

year  = "2016"
if len(sys.argv)>3: year = sys.argv[3]
if year != "2016" and year != "2017" and year != "2018":
    print "wrong year"
    sys.exit()

vfp  = "postVFP"
if len(sys.argv)>4: vfp = sys.argv[4]
if vfp != "preVFP" and vfp != "postVFP":
    print "wrong vfp"
    sys.exit()

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
    histname = histname.replace(".","p")
    hz = TH1F(histname,"",60,60,120)
    t.Draw("mass>>"+histname,cut,"goff")
    return hz
if year == "2016":
    if vfp == "preVFP":
        datatag = "2016_80X_v5_preVFP"
    else:
        datatag = "2016_80X_v5_postVFP"
elif year == "2017":
    datatag ="2017_94X"
elif year == "2018":
    datatag ="2018_94_pre3"
#old 2016 Effective Area
#EAval = [0.1752,0.1862,0.1411,0.1534,0.1903,0.2243,0.2687]
#EAeta = [0.,1.,1.479,2.,2.2,2.3,2.4,2.5]

EAval = [0.1440,0.1562,0.1032,0.0859,0.1116,0.1321,0.1654]
EAeta = [0.,1.,1.479,2.,2.2,2.3,2.4,2.5]
EAlist = []
for i in xrange(len(EAval)):
    EAlist.append("((el_abseta>={0:5.3f}&&el_abseta<{1:5.3f})*{2:6.4f})".format(EAeta[i],EAeta[i+1],EAval[i]))
EA = "+".join(EAlist)
relISO = "(el_chIso+max(0.0,(el_neuIso+el_phoIso-PU)))/el_pt"
relISO = relISO.replace("PU","event_rho*"+EA)
HISO = relISO+"*min(el_pt,25.)"

if stage == "Id":
    ID = "el_abseta<2.5&&(tag_Ele_q*el_q)==-1"
    PASS = "passingVeto94XV2"
    # PASS = "passingVetoNoIso94XV2"
elif stage == "IpIso":
    ID = "el_abseta<2.5&&passingVeto94XV2"
    #ID = "el_abseta<2.5&&passingVetoNoIso94XV2"
    PASS = "abs(el_dxy)<0.02&&abs(el_dz)<0.1&&"+HISO+"<5."
elif stage == "IdSpec":
    ID = "el_abseta<2.5&&(tag_Ele_q*el_q)==-1&&el_dr03TkSumPt<4"
    PASS = "passingVeto94XV2"
    #legacy TnP with SUSY IDs No Iso
    #PASS = "passingVetoNoIso94XV2"
    #PASS = "passingVeto"

FAIL = "!("+PASS+")"

TRIGZ = "1"
EXTRZ = "tag_Ele_abseta<2.1&&tag_Ele_pt>30&&abs(tag_Ele_dxy)<0.02&&abs(tag_Ele_dz)<0.2"

t = TChain("tnpEleIDs/fitter_tree")
#t = TChain("GsfElectronToEleID/fitter_tree")

if year == "2016":
    if mode == "Data":
        if vfp == "preVFP":
            # legacy 2016 pre VFP:
            t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_ntuples/UL2016_SingleEle_Run2016B.root")
            t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_ntuples/UL2016_SingleEle_Run2016B_ver2.root")
            t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_ntuples/UL2016_SingleEle_Run2016C.root")
            t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_ntuples/UL2016_SingleEle_Run2016D.root")
            t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_ntuples/UL2016_SingleEle_Run2016E.root")
            t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_ntuples/UL2016_SingleEle_Run2016F.root")
        else:
            # post VFP
            t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_ntuples/UL2016_SingleEle_Run2016F_postVFP.root")
            t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_ntuples/UL2016_SingleEle_Run2016G.root")
            t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_ntuples/UL2016_SingleEle_Run2016H.root")
    else:
        if vfp == "preVFP":
            #legacy MC tuples including (Pre VFP):
            t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_ntuples/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_preVFP_UL2016.root")
        else:
            # post VFP
            t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_ntuples/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_postVFP_UL2016.root")

elif year == "2017":
    if mode =="Data":
        #Moriond18
        t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2017_MINIAOD_Nm1/SingleEle_RunBCDEF.root")
    else:
        #t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/Run2017/electrons/merged/DY1_LO.root")
        t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2017_MINIAOD_Nm1/DYJetsToLL_madgraphMLM.root")

elif year == "2018":
    if mode =="Data":
        t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2018_MINIAOD_Nm1/EGamma_RunABCD.root")
    else:
        t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2018_MINIAOD_Nm1/DYJetsToLL_madgraphMLM.root")

makeDir("/groups/hephy/cms/felix.lang/StopsCompressed/results/%s/hists"%datatag)
fout = TFile("/groups/hephy/cms/felix.lang/StopsCompressed/results/%s/hists/ele_histos_%s_%s.root"%(datatag,mode,stage),"recreate")

hlist = []

for ipt in range(len(binning)-1):
    ptlow = binning[ipt]
    pthigh = binning[ipt+1]
    PTCUT = "el_pt>{0:f}&&el_pt<={1:f}".format(ptlow,pthigh)
    print ptlow,pthigh

    for etabin,etacut in etabins.items():
        print "eta dict: ", etabin, etacut
        cut = "&&".join([TRIGZ,ID,EXTRZ,PTCUT,etacut])
        hlist.append(gethist(t,"&&".join([cut,PASS]),ptlow,pthigh,"pass",etabin))
        hlist.append(gethist(t,"&&".join([cut,FAIL]),ptlow,pthigh,"fail",etabin))


fout.Write()
fout.Close()


