from ROOT import *
from math import *
import os, sys
import array
import time
import numpy as np
import ROOT
from itertools import product


def makeDir(path):
    if "." in path[-5:]:
        path = path.replace(os.path.basename(path), "")
        print path
    if os.path.isdir(path):
        return
    else:
        os.makedirs(path)


class ScalingFactor:  # TODO: possible optimizations: time.sleep functions from two methods to one

    def __init__(self, to_run, flavor, arg1, arg2, arg3, arg4, arg5):
        self.flavor = flavor
        if self.flavor != "ele" and self.flavor != "muon":
            print flavor
            print "wrong flavor"
            sys.exit()
        modes = ["Data", "MC"]
        if self.flavor == "ele":
            stages = ["Id", "IpIso", "IdSpec"]
            etabins = ['all', '0p8', '0p8_1p4', '1p4_1p5', '1p5_2p0', '2p0_2p5', 'm0p8', 'm0p8_m1p4', 'm1pm4_m1p5', 'm1p5_m2p0', 'm2p0_m2p5']
        else:
            stages = ["Id", "IpIso", "IpIsoSpec"]
            etabins = ['all', '0p9', '0p9_1p2', '1p2_2p1', '2p1_2p4']
        years = ["2016", "2017", "2018"]
        vfps = ["preVFP", "postVFP"]

        args = [arg1, arg2, arg3, arg4, arg5]
        if "2016" in args:
            if "preVFP" in args:
                self.datatag = "2016_80X_v5_preVFP"
            else:
                self.datatag = "2016_80X_v5_postVFP"
        elif "2017" in args:
            self.datatag = "2017_94X"
        else:
            self.datatag = "2018_94_pre3"

        if to_run == "hist":
            self.check_args = list(map(lambda x: list(x), product(modes, stages, years, vfps)))
            self.hist(arg1, arg2, arg3, arg4)
        elif to_run == "fit":
            self.check_args = list(map(lambda x: list(x), product(modes, stages, etabins, years, vfps)))
            self.fit(arg1, arg2, arg3, arg4, arg5)
        elif to_run == "ploteff":
            self.check_args = list(map(lambda x: list(x), product(stages, etabins, years, vfps)))
            self.ploteff(arg1, arg2, arg3, arg4)
        elif to_run == "2DleptonSF":
            self.check_args = list(map(lambda x: list(x), product(stages, years, vfps)))
            self.leptonsf2d(arg1, arg2, arg3, arg4)
        else:
            print("Please select one of the following methods to run: 'hist', 'fit', 'ploteff', '2DleptonSF'.")
            exit()
        return

    def hist(self, mode="Data", stage="Id", year="2016", vfp="postVFP"):
        if [mode, stage, year, vfp] not in self.check_args:
            print "wrong input"
            print([mode, stage, year, vfp])
            print "not in"
            print(self.check_args)
            sys.exit()

        def gethist(t, cut, lowedge, highedge, tag, etabin):
            histname = "h_{0:.1f}_{1:.1f}_{3}_{2}".format(lowedge, highedge, tag, etabin)
            histname = histname.replace(".", "p")
            hz = TH1F(histname, "", 60, 60, 120)
            t.Draw("mass>>" + histname, cut, "goff")
            return hz

        if self.flavor == "ele":

            binning = [5., 10., 20., 35., 50., 100., 200., 500]
            etabins = {
                "0p8": "el_sc_eta>=0&&el_sc_eta<0.8",
                "0p8_1p4": "el_sc_eta>=0.8&&el_sc_eta<1.442",
                # "1p4_1p5": "el_sc_eta>=1.442&&el_sc_eta<1.566",
                "1p4_1p5": "el_sc_eta>=1.442&&el_sc_eta<1.566",
                "1p5_2p0": "el_sc_eta>=1.566&&el_sc_eta<2.0",
                "2p0_2p5": "el_sc_eta>=2.0&&el_sc_eta<2.5",
                "m0p8": "el_sc_eta>=-0.8&&el_sc_eta<0",
                "m0p8_m1p4": "el_sc_eta>=-1.442&&el_sc_eta<-0.8",
                # "m1pm4_m1p5": "el_sc_eta>=-1.566&&el_sc_eta<-1.442",
                "m1pm4_m1p5": "el_sc_eta>=-1.566&&el_sc_eta<-1.442",
                "m1p5_m2p0": "el_sc_eta>=-2.0&&el_sc_eta<-1.566",
                "m2p0_m2p5": "el_sc_eta>=-2.5&&el_sc_eta<-2.0",
                "all": "el_sc_eta>=-2.5&&el_sc_eta<=2.5"
            }
            # old 2016 Effective Area
            # EAval = [0.1752,0.1862,0.1411,0.1534,0.1903,0.2243,0.2687]
            # EAeta = [0.,1.,1.479,2.,2.2,2.3,2.4,2.5]

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
                # PASS = "passingCutBasedVetoNoIso94XV2"
            elif stage == "IpIso":
                #ID = "el_abseta<2.5&&passingCutBasedVeto94XV2"
                ID = "el_abseta<2.5&&passingVeto94XV2"
                PASS = "abs(el_dxy)<0.02&&abs(el_dz)<0.1&&"+HISO+"<5."
            elif stage == "IdSpec":
                ID = "el_abseta<2.5&&(tag_Ele_q*el_q)==-1&&el_dr03TkSumPt<4"
                #PASS = "passingCutBasedVeto94XV2"
                #legacy TnP with SUSY IDs No Iso
                PASS = "passingVeto94XV2"
                #PASS = "passingVeto"

            FAIL = "!("+PASS+")"

            TRIGZ = "1"
            EXTRZ = "tag_Ele_abseta<2.1&&tag_Ele_pt>30&&abs(tag_Ele_dxy)<0.02&&abs(tag_Ele_dz)<0.2"

            t = TChain("tnpEleIDs/fitter_tree")
            #t = TChain("GsfElectronToEleID/fitter_tree")

            if year == "2016":
                if mode =="Data":
                    if vfp == "preVFP":
                        t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_ntuples/UL2016_SingleEle_Run2016B.root")
                        t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_ntuples/UL2016_SingleEle_Run2016B_ver2.root")
                        t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_ntuples/UL2016_SingleEle_Run2016C.root")
                        t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_ntuples/UL2016_SingleEle_Run2016D.root")
                        t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_ntuples/UL2016_SingleEle_Run2016E.root")
                        t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_ntuples/UL2016_SingleEle_Run2016F.root")
                    else:
                        t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_ntuples/UL2016_SingleEle_Run2016F_postVFP.root")
                        t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_ntuples/UL2016_SingleEle_Run2016G.root")
                        t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_ntuples/UL2016_SingleEle_Run2016H.root")
                else:
                    if vfp == "preVFP":
                        t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_ntuples/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_preVFP_UL2016.root")
                    else:
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

            makeDir("/groups/hephy/cms/fatih.okcu/StopsCompressed/results/%s/hists"%self.datatag)
            fout = TFile("/groups/hephy/cms/fatih.okcu/StopsCompressed/results/%s/hists/ele_histos_%s_%s.root"%(self.datatag,mode,stage),"recreate")

            hlist = []

            for ipt in range(len(binning) - 1):
                ptlow = binning[ipt]
                pthigh = binning[ipt + 1]
                PTCUT = "el_pt>{0:f}&&el_pt<={1:f}".format(ptlow, pthigh)
                print ptlow, pthigh

                for etabin, etacut in etabins.items():
                    print "eta dict: ", etabin, etacut
                    cut = "&&".join([TRIGZ, ID, EXTRZ, PTCUT, etacut])
                    hlist.append(gethist(t, "&&".join([cut, PASS]), ptlow, pthigh, "pass", etabin))
                    hlist.append(gethist(t, "&&".join([cut, FAIL]), ptlow, pthigh, "fail", etabin))

            fout.Write()
            fout.Close()
        else:
            binning = [3.5, 5., 10., 20., 25., 30., 40., 50., 60., 120.]
            # etabinning = [0., 0.9, 1.2, 2.1, 2.4]
            etabins = {
                "0p9": "abseta<0.9",
                "0p9_1p2": "abseta>=0.9&&abseta<1.2",
                "1p2_2p1": "abseta>=1.2&&abseta<2.1",
                "2p1_2p4": "abseta>=2.1&&abseta<2.4",
                # "all": "abseta<2.4"
            }

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
                if mode == "Data":
                    if vfp == "preVFP":
                        # legacy 2016 pre VFP:
                        t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_Muon/SingleMuon_Run2016Bver2_HIPM/tnpZ_Data_hadd.root")
                        t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_Muon/SingleMuon_Run2016C_HIPM/tnpZ_Data_hadd.root")
                        t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_Muon/SingleMuon_Run2016D_HIPM/tnpZ_Data_hadd.root")
                        t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_Muon/SingleMuon_Run2016E_HIPM/tnpZ_Data_hadd.root")
                        t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_Muon/SingleMuon_Run2016F_HIPM/tnpZ_Data_hadd.root")
                    else:
                        # post VFP
                        t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_Muon/SingleMuon_Run2016F/tnpZ_Data_hadd.root")
                        t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_Muon/SingleMuon_Run2016G/tnpZ_Data_hadd.root")
                        t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_Muon/SingleMuon_Run2016H/tnpZ_Data_hadd.root")
                else:
                    if vfp == "preVFP":
                        # legacy MC tuples including (Pre VFP):
                        t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_Muon/DY_M50_Madgraph_preVFP/tnpZ_MC_hadd.root")
                    else:
                        # post VFP
                        t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2016_Muon/DY_M50_Madgraph/tnpZ_MC_hadd.root")
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
                    t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2018_Muon/SingleMuon_Run2018A/tnpZ_Data_hadded.root")
                    t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2018_Muon/SingleMuon_Run2018B/tnpZ_Data_hadded.root")
                    t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2018_Muon/SingleMuon_Run2018C/tnpZ_Data_hadded.root")
                    t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2018_Muon/SingleMuon_Run2018D/tnpZ_Data_hadded.root")
                else:
                    t.Add("/groups/hephy/cms/priya.hussain/StopsCompressed/TnP/UL2018_Muon/DY_M50_Madgraph_STA/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_UL18MC.root")

            makeDir("/groups/hephy/cms/fatih.okcu/StopsCompressed/results/%s/hists"%self.datatag)
            fout = TFile("/groups/hephy/cms/fatih.okcu/StopsCompressed/results/%s/hists/mu_hists_%s_%s.root"%(self.datatag,mode,stage),"recreate")
            # fout = TFile("/groups/hephy/cms/fatih.okcu/StopsCompressed/results/%s/hists/mu_hists_%s_%s.root"%(self.datatag,mode,stage),"update")

            hlist = []

            for ipt in range(len(binning) - 1):
                ptlow = binning[ipt]
                pthigh = binning[ipt + 1]
                PTCUT = "pt>{0:f}&&pt<={1:f}".format(ptlow, pthigh)
                print ptlow, pthigh

                for etabin, etacut in etabins.items():
                    print "eta dict: ", etabin, etacut
                cut = "&&".join([TRIGZ, ID, EXTRZ, PTCUT, etacut])
            print etabin, cut
            hlist.append(gethist(t, "&&".join([cut, PASS]), ptlow, pthigh, "pass", etabin))
            hlist.append(gethist(t, "&&".join([cut, FAIL]), ptlow, pthigh, "fail", etabin))

            fout.Write()
            fout.Close()
        return

    def fit(self, mode="Data", stage="Id", etabin="all", year="2016", vfp="postVFP"):
        if [mode, stage, etabin, year, vfp] not in self.check_args:
            print "wrong input"
            print([mode, stage, etabin, year, vfp])
            print "not in"
            print(self.check_args)
            sys.exit()

        if self.flavor == 'ele':
            # binning = [5., 10., 20., 30., 45., 60., 100., 200.]
            binning = [5., 10., 20., 35., 50., 100., 200., 500]
            # etabinning = [0., 0.8, 1.442, 1.566, 2.0, 2.5]

            x1 = array.array("d", binning)
            nb = len(x1) - 1
            x2 = -999

            makeDir("/groups/hephy/cms/fatih.okcu/StopsCompressed/results/%s/fits" % self.datatag)

            pout = ["lowedge", "pthigh", "mean", "sigma", "alpha", "n", "sigma2", "gaus1f", "a", "signal", "bkg"]

            fpout = open(
                "/groups/hephy/cms/fatih.okcu/StopsCompressed/results/%s/fits/el_%s_%s.params" % (self.datatag, mode, stage),
                "w")
            sout = "\t".join(pout)
            fpout.write(sout + "\n")
            # 2017&2018 noISo hists location
            # fin = TFile("/scratch/priya.hussain/StopsCompressed/results/%s/hists/noIso/ele_histos_%s_%s.root"%(self.datatag,mode,stage))
            # 2016 legacy hists location
            fin = TFile("/groups/hephy/cms/fatih.okcu/StopsCompressed/results/%s/hists/ele_histos_%s_%s.root" % (self.datatag, mode, stage))
            print fin

            def getsigZ(hz,lowedge,pl=False):
            #    x = RooRealVar("x","Mass (GeV/c^{2})", 75.,130.)
            #    hz = TH1F("hz","",55,75,130)
                x = RooRealVar("x","Mass (GeV/c^{2})", 60.,130.)
                rdh = RooDataHist("rdh","",RooArgList(x),hz)
                x.setRange("R1",86,96)
            #    x.setRange("R1",60,120)

                meang = RooRealVar("meang", "meang", 91., 88, 94)
                sigma1 = RooRealVar("sigma1", "sigma1", 2., 1.5, 2.5)
                sigma2 = RooRealVar("sigma2", "sigma2", 4., 3., 7.)
                n = RooRealVar("n", "", 1.,0.,50.)
                alpha = RooRealVar("alpha", "", 1.,0.,5.)
            #    gaus1 = RooCBShape("gaus1","gaus1",x,meang,sigma1,alpha,n)
                gaus1 = RooGaussian("gaus1","gaus1",x,meang,sigma1)
                gaus2 = RooGaussian("gaus2","gaus2",x,meang,sigma2)
                gaus1f = RooRealVar("gaus1f","gaus1f",0.8,0.4,1.)
            #    gaus1f = RooRealVar("gaus1f","gaus1f",1.)
                dgaus = RooAddPdf("dgaus","dgaus",gaus1,gaus2,gaus1f)

                amin = -0.08 if lowedge<50. else -0.035
                a = RooRealVar("a", "a",max(-0.06,amin), amin,-0.03)
            #    a = RooRealVar("a", "", -10.,10.)

                expo = RooExponential("expo","exponential",x,a)

            #    a0 = RooRealVar("a0", "", 1., -10.,10.)
            #    a1 = RooRealVar("a1", "", 0., -1.,1.)
            #    a2 = RooRealVar("a2", "", 0., -.1,.1)
            #    a3 = RooRealVar("a3", "", 0., -.01,.01)
            #    expo = RooChebychev("expo","exponential",x,RooArgList(a0,a1,a2,a3))

            #    a0 = RooRealVar("a0", "", 115,90.,120.)
            #    a1 = RooRealVar("a1", "", -20,-100.,100.)
            #    expo = RooArgusBG("expo","exponential",x,a0,a1)


                signal = RooRealVar("signal", "signal", 1000, 0., 1.e9)
                bkg = RooRealVar("bkg", "", 100,0., 1.e9)

                dgex = RooAddPdf("dgex","dgex",RooArgList(dgaus,expo),RooArgList(signal,bkg))

                lowedgefit = 60
                if lowedge == 30: lowedgefit = 80
                if lowedge == 25: lowedgefit = 78
                if lowedge == 20: lowedgefit = 75
                if lowedge >= 35: lowedgefit = 82
                if lowedge >= 45: lowedgefit = 82

                fitres = dgex.fitTo(rdh,RooFit.Save(),RooFit.Range(lowedgefit,130),RooFit.Extended())

                if pl:
                    xframe = x.frame()
                    rdh.plotOn(xframe)
                    dgex.plotOn(xframe)
                    dgex.plotOn(xframe,RooFit.Components("dgaus"),RooFit.LineStyle(kDotted))
                    dgex.plotOn(xframe,RooFit.Components("expo"),RooFit.LineStyle(kDashed))
                    xframe.Draw()

                soutlist = [lowedge,pthigh,meang.getVal(),sigma1.getVal(),sigma2.getVal(),gaus1f.getVal(),a.getVal(),signal.getVal(),bkg.getVal()]
                sout = "\t".join(str(x) for x in soutlist)
                fpout.write(sout+"\n")
            #    soutlist = [a0.getVal(),a1.getVal(),a2.getVal(),a3.getVal()]
            #    sout = "---->"+"\t".join(str(x) for x in soutlist)
            #    fpout.write(sout+"\n")

                return fitres.floatParsFinal().find("signal"),rdh.sumEntries("1","R1")

            def getsigCB(hz,lowedge,pl=False):

                x = RooRealVar("x","Mass (GeV/c^{2})", 60.,120.)
                rdh = RooDataHist("rdh","",RooArgList(x),hz)
                x.setRange("R1",86,96)

                amin = -0.08 if lowedge<45. else 0.
                amax = -0.02 if lowedge<45. else 0.
                a = RooRealVar("a", "a",max(-0.06,amin), amin,amax)
                expo = RooExponential("expo","exponential",x,a)

                mean = RooRealVar("meang", "meang", 90., 88, 92.)
                sigmamax = 5. #if lowedge>20. else 3.
                if '0p8' in etabin  and lowedge<6.:
                    sigmamax = 3.5
                print "?????", etabin, "!!!!!"
                sigma = RooRealVar("sigma", "sigma", 2.5, 2., sigmamax)

                ncent = 40. if lowedge<30 else 50.
                n = RooRealVar("n", "", ncent, ncent, ncent)
                alphacent = 0.5 + max(0.,lowedge-5.)/35.
                alphacent = min(1.5,alphacent)
                alpha = RooRealVar("alpha", "", alphacent,alphacent,alphacent)
                cball = RooCBShape("cball","crystal ball",x,mean,sigma,alpha,n)

                s2min = 5. if lowedge>6. else 7.5
                sigma2 = RooRealVar("sigma2", "sigma2", s2min+0.2, s2min, 8.)
                gaus2 = RooGaussian("gaus2","gaus2",x,mean,sigma2)
                gaus1f = RooRealVar("gaus1f","gaus1f",0.7,0.6,0.9)
                cbgaus = RooAddPdf("cbgaus","cbgaus",cball,gaus2,gaus1f)


            #    a = RooRealVar("a", "a", 0.,0.,1000.)
            #    b = RooRealVar("b", "b", 0.,-1000.,1000.)
            #    c = RooRealVar("c", "c", 0.,-1000.,1000.)
            #    d = RooRealVar("d", "d", 0.,-1000.,1000.)
            #    expo = RooChebychev("cheb","chebychev",x,RooArgList(a,b,c))

                signal = RooRealVar("signal", "signal", 100, 0., 1.e9)
                bkg = RooRealVar("bkg", "", 1,0., 1.e9)
                cbex = RooAddPdf("cbex","",RooArgList(cbgaus,expo),RooArgList(signal,bkg))

                lowedgefit = 60
                #if lowedge == 30: lowedgefit = 80
                if lowedge == 25: lowedgefit = 70
                if lowedge == 20: lowedgefit = 68
                #if lowedge == 25: lowedgefit = 78
                #if lowedge == 20: lowedgefit = 75
                #0p8:
                #if lowedge == 20: lowedgefit = 84
                if lowedge == 35: lowedgefit = 70
                if lowedge >= 45: lowedgefit = 79
                if lowedge == 50: lowedgefit = 82
                #2p02p5:
                #if lowedge == 50: lowedgefit = 78
                if lowedge >= 60: lowedgefit = 81
                #if lowedge >= 200: lowedgefit = 80
                fitres = cbex.fitTo(rdh,RooFit.Save(),RooFit.Range(lowedgefit,120),RooFit.PrintLevel(-1),RooFit.Extended())

                if pl:
                    xframe = x.frame()
                    rdh.plotOn(xframe)
                    cbex.plotOn(xframe)
                    cbex.plotOn(xframe,RooFit.Components("cbgaus"),RooFit.LineStyle(kDotted))
                    cbex.plotOn(xframe,RooFit.Components("expo"),RooFit.LineStyle(kDashed))
                    xframe.Draw()
                #chi2 = xframe.chiSquare(7)
                #chi2 = xframe.chiSquare()
                    #print "chi square: ", chi2
                print "mean:", mean.getVal()
                print "sigma:", sigma.getVal()
                print "alpha:", alpha.getVal()
                print "n:", n.getVal()
                print "sigma2:", sigma2.getVal()
                print "gaus1f:", gaus1f.getVal()
                print "a:", a.getVal()
            #    print "b:", b.getVal()
            #    print "c:", c.getVal()
            #    print "d:", d.getVal()
                print "signal:", signal.getVal()
                print "bkg:", bkg.getVal()

                soutlist = [lowedge,pthigh,mean.getVal(),sigma.getVal(),alpha.getVal(),n.getVal(),sigma2.getVal(),gaus1f.getVal(),a.getVal(),signal.getVal(),bkg.getVal()]
                sout = "\t".join(str(x) for x in soutlist)
                fpout.write(sout+"\n")

                return fitres.floatParsFinal().find("signal"),rdh.sumEntries("1","R1")


            fout = TFile("/groups/hephy/cms/fatih.okcu/StopsCompressed/results/%s/fits/ele_result_%s_%s_%s.root"%(self.datatag,mode,stage,etabin),"recreate")

            hpassfit = TH1F("hpassfit","",nb,x1)
            hpassfit.Sumw2()
            hfailfit = TH1F("hfailfit","",nb,x1)
            hfailfit.Sumw2()
            hpasscnt = TH1F("hpasscnt","",nb,x1)
            hfailcnt = TH1F("hfailcnt","",nb,x1)

            for ipt in range(len(binning)-1):
            #for ipt in [1]:
                aux_ptlow = binning[ipt]
                pthigh = binning[ipt+1]
                print aux_ptlow,pthigh
                savedir = "/groups/hephy/cms/fatih.okcu/www/StopsCompressed/TnP/%s/fits/%s/%s"%(self.datatag,mode,stage)
                makeDir(savedir)
                namestring = "{0:.1f}_{1:.1f}_{2}".format(aux_ptlow,pthigh,etabin)
                namestring = namestring.replace(".","p")

                histname = "h_"+namestring+"_pass"

                fitp,cntp = getsigCB(fin.Get(histname),aux_ptlow,True)
                gPad.SaveAs("%s/ele_passing_%s_%s_%s.png"%(savedir,namestring,mode,stage))
                histname = "h_"+namestring+"_fail"
                fitf,cntf = getsigCB(fin.Get(histname),aux_ptlow,True)
                gPad.SaveAs("%s/ele_failing_%s_%s_%s.png"%(savedir,namestring,mode,stage))

                hpassfit.SetBinContent(ipt+1,fitp.getVal())
                hpassfit.SetBinError(ipt+1,fitp.getError())
                hfailfit.SetBinContent(ipt+1,fitf.getVal())
                hfailfit.SetBinError(ipt+1,fitf.getError())
                print ">>>",fitp.getVal(),fitp.getError(),fitf.getVal(),fitf.getError()

                hpasscnt.SetBinContent(ipt+1,cntp)
                hfailcnt.SetBinContent(ipt+1,cntf)

            hhh = TH1F("hhh","",nb,x1)
            hhh.SetMinimum(0.7)
            hhh.SetMaximum(1.1)
            hhh.Draw()

            hallcnt = hpasscnt.Clone("hallcnt")
            hallcnt.Add(hfailcnt)
            effcnt = TEfficiency(hpasscnt,hallcnt)
            effcnt.Draw("same")

            hallfit = hpassfit.Clone("hallfit")
            hallfit.Add(hfailfit)
            efffit = TEfficiency(hpassfit,hallfit)
            efffit.SetLineColor(2)
            efffit.Draw("same")

            effcnt.Write("effcnt")
            efffit.Write("efffit")

            fout.Write()
            fout.Close()

            fpout.close()
            gPad.Update()
        else:
            # binning = [3.5, 5., 10., 20., 30., 45., 60., 120.]
            binning = [3.5, 5., 10., 20., 25., 30., 40., 50., 60., 120.]
            x1 = array.array("d", binning)
            nb = len(x1) - 1
            x2 = -999

            pout = ["lowedge", "pthigh", "mean", "sigma", "sigma2", "gaus1f", "a", "signal", "bkg"]

            makeDir("/groups/hephy/cms/fatih.okcu/StopsCompressed/results/%s/fits" % self.datatag)

            fpout = open("/groups/hephy/cms/fatih.okcu/StopsCompressed/results/%s/fits/mu_%s_%s.params" % (self.datatag, mode, stage), "w")
            sout = "\t".join(pout)
            fpout.write(sout + "\n")

            fin = TFile("/groups/hephy/cms/fatih.okcu/StopsCompressed/results/%s/hists/mu_hists_%s_%s.root" % (self.datatag, mode, stage))
            print fin


            def getsigZ(hz, lowedge, pl=False):
                #    x = RooRealVar("x","Mass (GeV/c^{2})", 75.,130.)
                #    hz = TH1F("hz","",55,75,130)
                x = RooRealVar("x", "Mass (GeV/c^{2})", 60., 130.)
                rdh = RooDataHist("rdh", "", RooArgList(x), hz)
                x.setRange("R1", 86, 96)
                #    x.setRange("R1",60,120)

                meang = RooRealVar("meang", "meang", 91., 88, 92)
                sigma1 = RooRealVar("sigma1", "sigma1", 2., 1.5, 2.5)
                sigma2 = RooRealVar("sigma2", "sigma2", 4., 3., 7.)
                n = RooRealVar("n", "", 1., 0., 50.)
                alpha = RooRealVar("alpha", "", 1., 0., 5.)
                #    gaus1 = RooCBShape("gaus1","gaus1",x,meang,sigma1,alpha,n)
                gaus1 = RooGaussian("gaus1", "gaus1", x, meang, sigma1)
                gaus2 = RooGaussian("gaus2", "gaus2", x, meang, sigma2)
                gaus1f = RooRealVar("gaus1f", "gaus1f", 0.8, 0.4, 1.)
                #    gaus1f = RooRealVar("gaus1f","gaus1f",1.)
                dgaus = RooAddPdf("dgaus", "dgaus", gaus1, gaus2, gaus1f)

                amin = -0.08 if lowedge < 50. else -0.035
                a = RooRealVar("a", "a", max(-0.06, amin), amin, -0.03)
                #    a = RooRealVar("a", "", -10.,10.)

                expo = RooExponential("expo", "exponential", x, a)

                #    a0 = RooRealVar("a0", "", 1., -10.,10.)
                #    a1 = RooRealVar("a1", "", 0., -1.,1.)
                #    a2 = RooRealVar("a2", "", 0., -.1,.1)
                #    a3 = RooRealVar("a3", "", 0., -.01,.01)
                #    expo = RooChebychev("expo","exponential",x,RooArgList(a0,a1,a2,a3))

                #    a0 = RooRealVar("a0", "", 115,90.,120.)
                #    a1 = RooRealVar("a1", "", -20,-100.,100.)
                #    expo = RooArgusBG("expo","exponential",x,a0,a1)

                signal = RooRealVar("signal", "signal", 1000, 0., 1.e9)
                bkg = RooRealVar("bkg", "", 100, 0., 1.e9)

                dgex = RooAddPdf("dgex", "dgex", RooArgList(dgaus, expo), RooArgList(signal, bkg))

                lowedgefit = 62
                if lowedge == 30: lowedgefit = 80
                if lowedge == 25: lowedgefit = 78
                if lowedge == 20: lowedgefit = 70
                # if lowedge == 20: lowedgefit = 75
                if lowedge >= 35: lowedgefit = 82
                if lowedge >= 45: lowedgefit = 85
                if lowedge >= 50: lowedgefit = 80
                # if lowedge >= 50: lowedgefit = 82
                fitres = dgex.fitTo(rdh, RooFit.Save(), RooFit.Range(lowedgefit, 130), RooFit.Extended())

                if pl:
                    xframe = x.frame()
                    rdh.plotOn(xframe)
                    dgex.plotOn(xframe)
                    dgex.plotOn(xframe, RooFit.Components("dgaus"), RooFit.LineStyle(kDotted))
                    dgex.plotOn(xframe, RooFit.Components("expo"), RooFit.LineStyle(kDashed))
                    xframe.Draw()
                # chi2 = xframe.chiSquare("dgex","rdh",3)
                # print "chi square: ", chi2

                soutlist = [lowedge, pthigh, meang.getVal(), sigma1.getVal(), sigma2.getVal(), gaus1f.getVal(), a.getVal(),
                            signal.getVal(), bkg.getVal()]
                sout = "\t".join(str(x) for x in soutlist)
                fpout.write(sout + "\n")
                #    soutlist = [a0.getVal(),a1.getVal(),a2.getVal(),a3.getVal()]
                #    sout = "---->"+"\t".join(str(x) for x in soutlist)
                #    fpout.write(sout+"\n")

                return fitres.floatParsFinal().find("signal"), rdh.sumEntries("1", "R1")


            def getsigCB(hz, lowedge, pl=False):
                x = RooRealVar("x", "Mass (GeV/c^{2})", 60., 120.)
                rdh = RooDataHist("rdh", "", RooArgList(x), hz)
                x.setRange("R1", 86, 96)

                amin = -0.08 if lowedge < 45. else 0.
                amax = -0.02 if lowedge < 45. else 0.
                a = RooRealVar("a", "a", max(-0.06, amin), amin, amax)
                expo = RooExponential("expo", "exponential", x, a)

                mean = RooRealVar("meang", "meang", 90., 88, 92.)
                sigmamax = 5.  # if lowedge>20. else 3.
                if '0p8' in etabin and lowedge < 6.:
                    sigmamax = 3.5
                    print
                    "?????", etabin, "!!!!!"
                sigma = RooRealVar("sigma", "sigma", 2.5, 2., sigmamax)

                ncent = 40. if lowedge < 30 else 50.
                n = RooRealVar("n", "", ncent, ncent, ncent)
                alphacent = 0.5 + max(0., lowedge - 5.) / 35.
                alphacent = min(1.5, alphacent)
                alpha = RooRealVar("alpha", "", alphacent, alphacent, alphacent)
                cball = RooCBShape("cball", "crystal ball", x, mean, sigma, alpha, n)

                s2min = 5. if lowedge > 6. else 7.5
                sigma2 = RooRealVar("sigma2", "sigma2", s2min + 0.2, s2min, 8.)
                gaus2 = RooGaussian("gaus2", "gaus2", x, mean, sigma2)
                gaus1f = RooRealVar("gaus1f", "gaus1f", 0.7, 0.6, 0.9)
                cbgaus = RooAddPdf("cbgaus", "cbgaus", cball, gaus2, gaus1f)

                #    a = RooRealVar("a", "a", 0.,0.,1000.)
                #    b = RooRealVar("b", "b", 0.,-1000.,1000.)
                #    c = RooRealVar("c", "c", 0.,-1000.,1000.)
                #    d = RooRealVar("d", "d", 0.,-1000.,1000.)
                #    expo = RooChebychev("cheb","chebychev",x,RooArgList(a,b,c))

                signal = RooRealVar("signal", "signal", 100, 0., 1.e9)
                bkg = RooRealVar("bkg", "", 1, 0., 1.e9)
                cbex = RooAddPdf("cbex", "", RooArgList(cbgaus, expo), RooArgList(signal, bkg))

                lowedgefit = 62
                if lowedge == 30: lowedgefit = 80
                if lowedge == 25: lowedgefit = 78
                if lowedge == 20: lowedgefit = 70
                # if lowedge == 20: lowedgefit = 75
                if lowedge >= 35: lowedgefit = 82
                if lowedge >= 45: lowedgefit = 85
                if lowedge >= 50: lowedgefit = 80
                # if lowedge >= 50: lowedgefit = 82
                fitres = dgex.fitTo(rdh, RooFit.Save(), RooFit.Range(lowedgefit, 120), RooFit.Extended())
                # fitres = cbex.fitTo(rdh, RooFit.Save(), RooFit.Range(lowedgefit, 120), RooFit.PrintLevel(-1), RooFit.Extended())

                if pl:
                    xframe = x.frame()
                    rdh.plotOn(xframe)
                    cbex.plotOn(xframe)
                    cbex.plotOn(xframe, RooFit.Components("cbgaus"), RooFit.LineStyle(kDotted))
                    cbex.plotOn(xframe, RooFit.Components("expo"), RooFit.LineStyle(kDashed))
                    xframe.Draw()
                # chi2 = xframe.chiSquare(7)
                # chi2 = xframe.chiSquare()
                # print "chi square: ", chi2
                print
                "mean:", mean.getVal()
                print
                "sigma:", sigma.getVal()
                print
                "alpha:", alpha.getVal()
                print
                "n:", n.getVal()
                print
                "sigma2:", sigma2.getVal()
                print
                "gaus1f:", gaus1f.getVal()
                print
                "a:", a.getVal()
                #    print "b:", b.getVal()
                #    print "c:", c.getVal()
                #    print "d:", d.getVal()
                print
                "signal:", signal.getVal()
                print
                "bkg:", bkg.getVal()

                soutlist = [lowedge, pthigh, mean.getVal(), sigma.getVal(), alpha.getVal(), n.getVal(), sigma2.getVal(),
                            gaus1f.getVal(), a.getVal(), signal.getVal(), bkg.getVal()]
                sout = "\t".join(str(x) for x in soutlist)
                fpout.write(sout + "\n")

                return fitres.floatParsFinal().find("signal"), rdh.sumEntries("1", "R1")


            fout = TFile("/groups/hephy/cms/fatih.okcu/StopsCompressed/results/%s/fits/muon_result_%s_%s_%s.root" % (self.datatag, mode, stage, etabin), "recreate")

            hpassfit = TH1F("hpassfit", "", nb, x1)
            hpassfit.Sumw2()
            hfailfit = TH1F("hfailfit", "", nb, x1)
            hfailfit.Sumw2()
            hpasscnt = TH1F("hpasscnt", "", nb, x1)
            hfailcnt = TH1F("hfailcnt", "", nb, x1)

            for ipt in range(len(binning) - 1):
                # for ipt in [1]:
                aux_ptlow = binning[ipt]
                pthigh = binning[ipt + 1]
                print aux_ptlow, pthigh

                savedir = "/groups/hephy/cms/fatih.okcu/www/StopsCompressed/TnP/%s/fits/%s/%s" % (self.datatag, mode, stage)
                makeDir(savedir)
                namestring = "{0:.1f}_{1:.1f}".format(aux_ptlow, pthigh)
                namestring = namestring.replace(".", "p")
                namestring += '_' + etabin

                histname = "h_" + namestring + "_pass"
                print 'histname', histname

                fitp, cntp = getsigZ(fin.Get(histname), aux_ptlow, True)
                gPad.SaveAs("%s/muon_passing_%s_%s_%s.png" % (savedir, namestring, mode, stage))
                histname = "h_" + namestring + "_fail"
                fitf, cntf = getsigZ(fin.Get(histname), aux_ptlow, True)
                gPad.SaveAs("%s/muon_failing_%s_%s_%s.png" % (savedir, namestring, mode, stage))

                hpassfit.SetBinContent(ipt + 1, fitp.getVal())
                hpassfit.SetBinError(ipt + 1, fitp.getError())
                hfailfit.SetBinContent(ipt + 1, fitf.getVal())
                hfailfit.SetBinError(ipt + 1, fitf.getError())
                print ">>>", fitp.getVal(), fitp.getError(), fitf.getVal(), fitf.getError()

                hpasscnt.SetBinContent(ipt + 1, cntp)
                hfailcnt.SetBinContent(ipt + 1, cntf)

            hhh = TH1F("hhh", "", nb, x1)
            hhh.SetMinimum(0.7)
            hhh.SetMaximum(1.1)
            hhh.Draw()

            hallcnt = hpasscnt.Clone("hallcnt")
            hallcnt.Add(hfailcnt)
            effcnt = TEfficiency(hpasscnt, hallcnt)
            effcnt.Draw("same")

            hallfit = hpassfit.Clone("hallfit")
            hallfit.Add(hfailfit)
            efffit = TEfficiency(hpassfit, hallfit)
            efffit.SetLineColor(2)
            efffit.Draw("same")

            effcnt.Write("effcnt")
            efffit.Write("efffit")

            fout.Write()
            fout.Close()

            fpout.close()
            gPad.Update()
        return

    def ploteff(self, stage="Id", etabin="all", year="2016", vfp="postVFP"):
        if [stage, etabin, year, vfp] not in self.check_args:
            print "wrong input"
            print([stage, etabin, year, vfp])
            print "not in"
            print(self.check_args)
            sys.exit()
        mineff = 0.3
        maxeff = 1.05
        minsf = 0.7
        maxsf = 1.05

        plotcount = 1
        # if len(sys.argv)>5: plotcount = int(sys.argv[5])
        if year == "2016":
            if vfp == "preVFP":
                self.datatag = "2016_80X_v5_preVFP"
            else:
                self.datatag = "2016_80X_v5_postVFP"
        elif year == "2017":
            self.datatag = "2017_94X"
        elif year == "2018":
            self.datatag = "2018_94_pre3"
        print year, self.datatag
        if self.flavor == "muon":
            # binning = [3.5, 5., 10., 20., 30., 45., 60., 120.]
            binning = [3.5, 5., 10., 20., 25., 30., 40., 50., 60., 120.]
            etabinning = [0., 0.9, 1.2, 2.1, 2.4]
            print binning
        else:
            # binning = [3.5, 5., 10., 20., 30., 45., 60., 100., 200.]
            binning = [5., 10., 20., 35., 50., 100., 200., 500]
            etabinning = [-2.5, -2.0, -1.566, -1.442, -0.8, 0., 0.8, 1.442, 1.566, 2.0, 2.5]
        x1 = array.array("d", binning)
        nb = len(x1) - 1

        def divideEff(e1, e2):
            n = e1.GetTotalHistogram().GetNbinsX()
            print n
            res = TGraphAsymmErrors(n)
            for i in range(n):
                a = e1.GetTotalHistogram().GetBinLowEdge(i + 1)
                w = e1.GetTotalHistogram().GetBinWidth(i + 1)
                v1 = e1.GetEfficiency(i + 1)
                u1 = e1.GetEfficiencyErrorUp(i + 1)
                d1 = e1.GetEfficiencyErrorLow(i + 1)
                v2 = e2.GetEfficiency(i + 1)
                u2 = e2.GetEfficiencyErrorUp(i + 1)
                d2 = e2.GetEfficiencyErrorLow(i + 1)
                if v1 * v2 == 0:
                    v = 0.
                    u = 0.
                    d = 0.
                else:
                    v = v1 / v2 if v2 > 0. else 0.
                    u = v * sqrt(pow(u1 / v1, 2) + pow(u2 / v2, 2))
                    d = v * sqrt(pow(d1 / v1, 2) + pow(d2 / v2, 2))
                print i, v, u, d
                x = a + 0.5 * w
                res.SetPoint(i, x, v)
                res.SetPointError(i, 0., 0., d, u)
            return res


        def gethistbin(h, x):
            if x > binning[-1]:
                ib = nb + 1
                return ib
            if x < binning[0]:
                ib = 0
                return ib
            for i in xrange(nb):
                if x > binning[i] and x < binning[i + 1]:
                    ib = i + 1
                    return ib
            return -999


        def converttohist(g, n):
            h = TH1F(n, "", nb, x1)
            h.Sumw2()
            for i in xrange(g.GetN()):
                x = Double(0.)
                y = Double(0.)
                g.GetPoint(i, x, y)
                eyh = g.GetErrorYhigh(i)
                eyl = g.GetErrorYlow(i)
                ey = max(eyh, eyl)
                ibin = gethistbin(h, x)
                h.SetBinContent(ibin, y)
                h.SetBinError(ibin, ey)
            h1c = h.Clone()
            h1c.Print("all")
            return h1c


        gStyle.SetOptStat(kFALSE)
        c1 = TCanvas("c1", "", 700, 700)
        leg = TLegend(0.4, 0.2, 0.85, 0.45)
        if self.flavor == 'muon':
            Hdummy = TH1F("Hdummy", "", 12, 0, 120)
        else:
            Hdummy = TH1F("Hdummy", "", 20, 0, 500)
        Hdummy.SetMinimum(mineff)
        Hdummy.SetMaximum(maxeff)
        Hdummy.SetXTitle("p_{T} (GeV)")
        Hdummy.SetYTitle("efficiency")
        Hdummy.GetYaxis().SetTitleOffset(1.4)
        Hdummy.Draw()

        if self.flavor == "ele":
            suffix = "_" + etabin
            print suffix
        else:
            suffix = "_" + etabin

        # makeDir("/groups/fatih.okcu/StopsCompressed/results/%s/fits/%s_result_MC_%s%s.root" % (self.datatag, self.flavor, stage, suffix))
        f = TFile("/groups/hephy/cms/fatih.okcu/StopsCompressed/results/%s/fits/%s_result_MC_%s%s.root" % (self.datatag, self.flavor, stage, suffix))
        effcntZMC = TEfficiency(f.Get("effcnt"))
        efffitZMC = TEfficiency(f.Get("efffit"))
        f.Close()
        f = TFile("/groups/hephy/cms/fatih.okcu/StopsCompressed/results/%s/fits/%s_result_Data_%s%s.root" % (self.datatag, self.flavor, stage, suffix))
        effcntZData = TEfficiency(f.Get("effcnt"))
        efffitZData = TEfficiency(f.Get("efffit"))
        f.Close()

        if plotcount:
            effcntZMC.SetMarkerStyle(20)
            effcntZMC.SetMarkerColor(2)
            effcntZMC.SetLineColor(2)
            effcntZMC.Draw("same")
            leg.AddEntry(effcntZMC, "Z MC counting T&P", "lpe")

            effcntZData.SetMarkerStyle(20)
            effcntZData.SetMarkerColor(kOrange)
            effcntZData.SetLineColor(kOrange)
            effcntZData.Draw("same")
            leg.AddEntry(effcntZData, "Z Data counting T&P", "lpe")

        efffitZMC.SetMarkerStyle(20)
        efffitZMC.SetMarkerColor(4)
        efffitZMC.SetLineColor(4)
        efffitZMC.Draw("same")
        leg.AddEntry(efffitZMC, "Z MC fit T&P", "lpe")

        efffitZData.SetMarkerStyle(20)
        efffitZData.SetMarkerColor(7)
        efffitZData.SetLineColor(7)
        efffitZData.Draw("same")
        leg.AddEntry(efffitZData, "Z Data fit T&P", "lpe")

        leg.Draw()
        gPad.Update()

        savedir = "/groups/hephy/cms/fatih.okcu/www/StopsCompressed/TnP/%s/finalplots/%s" % (self.datatag, stage)
        makeDir(savedir)
        makeDir("/groups/hephy/cms/fatih.okcu/StopsCompressed/results/%s/finalplots" % self.datatag)

        c1.SaveAs("/groups/hephy/cms/fatih.okcu/StopsCompressed/results/%s/finalplots/%s_eff_%s_%s.png" % (self.datatag, self.flavor, stage, etabin))
        c1.SaveAs("%s/%s_eff_%s_%s.png" % (savedir, self.flavor, stage, etabin))
        fout = TFile("/groups/hephy/cms/fatih.okcu/StopsCompressed/results/%s/finalplots/%s_eff_%s_%s.root" % (self.datatag, self.flavor, stage, etabin), "RECREATE")
        c1c = c1.Clone()
        c1c.Write()
        fout.Close()

        c2 = TCanvas("c2", "", 700, 700)
        leg2 = TLegend(0.4, 0.25, 0.85, 0.4)

        Hdummy.SetYTitle("Data/MC scale factor")
        Hdummy.SetMinimum(minsf)
        Hdummy.SetMaximum(maxsf)
        Hdummy.Draw()

        print plotcount
        if plotcount:
            print plotcount
            SFcntZ = divideEff(effcntZData, effcntZMC)
            SFcntZ.SetMarkerStyle(20)
            SFcntZ.SetMarkerColor(2)
            SFcntZ.SetLineColor(2)
            SFcntZ.Draw("same p")
            leg2.AddEntry(SFcntZ, "Z counting T&P", "lpe")

        SFfitZ = divideEff(efffitZData, efffitZMC)
        SFfitZ.SetMarkerStyle(20)
        SFfitZ.SetMarkerColor(4)
        SFfitZ.SetLineColor(4)
        SFfitZ.Draw("same p")
        leg2.AddEntry(SFfitZ, "Z fit T&P", "lpe")

        leg2.Draw()
        gPad.Update()

        c2.SaveAs("/groups/hephy/cms/fatih.okcu/StopsCompressed/results/%s/finalplots/%s_SF_%s_%s.png" % (self.datatag, self.flavor, stage, etabin))
        c2.SaveAs("%s/%s_SF_%s_%s.png" % (savedir, self.flavor, stage, etabin))
        fout = TFile("/groups/hephy/cms/fatih.okcu/StopsCompressed/results/%s/finalplots/%s_SF_%s_%s.root" % (self.datatag, self.flavor, stage, etabin), "RECREATE")
        c2c = c2.Clone()
        c2c.Write()
        fout.Close()

        flavors = ['ele', 'muon']
        if self.flavor == "ele":
            etabins = ['all', '0p8', '0p8_1p4', '1p4_1p5', '1p5_2p0', '2p0_2p5', 'm0p8', 'm0p8_m1p4', 'm1pm4_m1p5', 'm1p5_m2p0', 'm2p0_m2p5']
            stages = ['Id', 'IpIso', 'IdSpec']
        else:
            etabins = ['all', '0p9', '0p9_1p2', '1p2_2p1', '2p1_2p4']
            stages = ['Id', 'IpIso', 'IpIsoSpec']
            flavors = flavors[::-1]

        time_interval = 4
        unique_times = np.arange(0, len(flavors)*len(stages)*len(etabins)*time_interval, time_interval)
        unique_times_dict = {fl: {st: {et: 0 for et in etabins} for st in stages} for fl in flavors}
        for i, (fl, st, et) in enumerate(product(flavors, stages, etabins)):
            unique_times_dict[fl][st][et] = unique_times[i]
        time.sleep(unique_times_dict[self.flavor][stage][etabin])

        fsfout = TFile("/groups/hephy/cms/fatih.okcu/StopsCompressed/results/%s/finalplots/hephy_scale_factors_%s.root"%(self.datatag,self.flavor),"update")
        H_SFfitZ_name = "{0}_SF_{1}_{2}".format(self.flavor, stage, etabin)
        fsfout.Delete(H_SFfitZ_name + ";*")

        H_SFfitZ = converttohist(SFfitZ, H_SFfitZ_name)

        fsfout.Write()
        fsfout.Close()

        return

    def leptonsf2d(self, inputFileName="hephy_scale_factors", stage="Id", year="2016", vfp="postVFP"):
        if [stage, year, vfp] not in self.check_args:
            print "wrong input"
            print([stage, year, vfp])
            print "not in"
            print(self.check_args)
            sys.exit()

        ROOT.gStyle.SetOptStat(0)  # 1111 adds histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis

        inputFile = "/groups/hephy/cms/fatih.okcu/StopsCompressed/results/%s/finalplots/%s_%s.root"%(self.datatag,inputFileName,self.flavor)
        if not os.path.isfile(inputFile):
            print "input file %s does not exist"%inputFile
            sys.exit()

        suffix = "_%s_%s_%s"%(inputFileName, self.flavor, stage)

        f = ROOT.TFile(inputFile, "update")

        h = {}
        if self.flavor == 'muon':
            for etabin in ['0p9', '0p9_1p2', '1p2_2p1', '2p1_2p4']:
                h[etabin] = f.Get("%s_SF_%s_%s"%(self.flavor,stage,etabin))
        else:
            for etabin in ['0p8', '0p8_1p4', '1p4_1p5', '1p5_2p0','2p0_2p5', 'm0p8', 'm0p8_m1p4', 'm1pm4_m1p5','m1p5_m2p0','m2p0_m2p5']:
                h[etabin] = f.Get("%s_SF_%s_%s"%(self.flavor,stage,etabin))
        for key, value in h.items():
            print(key, value)

        # get binning
        if self.flavor == "muon":
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
        histName = "%s_SF_%s_2D"%(self.flavor,stage)
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

        if self.flavor == "muon":
            SF = ROOT.TH2F(histName, histName, len(etabins)-1, etabins, nx, ptbins)
            SF.SetTitle(histName)
            SF.GetXaxis().SetTitle("p_{T} (GeV)")
            SF.GetYaxis().SetTitle("|#eta|")
            SF.GetZaxis().SetTitle("SF")
            SF.GetXaxis().SetTitleOffset(1.2)
            SF.GetYaxis().SetTitleOffset(1.2)
            SF.GetZaxis().SetTitleOffset(1.2)
            SF.GetZaxis().SetRangeUser(0.5,1)
            SF.SetMarkerSize(0.8)
            for i in range(nx):
                i+=1
                SF.SetBinContent(i, 1, h['0p9'].GetBinContent(i))
                print "value for 1st", h['0p9'].GetBinContent(i)
                SF.SetBinError(i,   1, h['0p9'].GetBinError(i))

                SF.SetBinContent(i, 2, h['0p9_1p2'].GetBinContent(i))
                print "value for 2nd", h['0p9_1p2'].GetBinContent(i)
                SF.SetBinError(i,   2, h['0p9_1p2'].GetBinError(i))

                SF.SetBinContent(i, 3, h['1p2_2p1'].GetBinContent(i))
                print "value for 3rd", h['1p2_2p1'].GetBinContent(i)
                SF.SetBinError(i,   3, h['1p2_2p1'].GetBinError(i))

                SF.SetBinContent(i, 4, h['2p1_2p4'].GetBinContent(i))
                print "value for 4th", h['2p1_2p4'].GetBinContent(i)
                SF.SetBinError(i,   4, h['2p1_2p4'].GetBinError(i))
        else:
            SF = ROOT.TH2F(histName, histName , len(etabins)-1, etabins, nx, ptbins)
            SF.SetTitle(histName)
            SF.GetYaxis().SetTitle("p_{T} (GeV)")
            SF.GetXaxis().SetTitle("|#eta|")
            SF.GetZaxis().SetTitle("SF")
            SF.GetXaxis().SetTitleOffset(1.2)
            SF.GetYaxis().SetTitleOffset(1.2)
            SF.GetZaxis().SetTitleOffset(1.2)
            SF.GetZaxis().SetRangeUser(0.94, 1.06)
            #keeping same z scale for comparison
            #SF.GetZaxis().SetRangeUser(0.75,1.25)
            SF.SetMarkerSize(0.8)

            for i in range(nx):
                i+=1
                SF.SetBinContent(1, i, h['m2p0_m2p5'].GetBinContent(i))
                print "value for 1st", h['m2p0_m2p5'].GetBinContent(i)
                SF.SetBinError(1,   i, h['m2p0_m2p5'].GetBinError(i))

                SF.SetBinContent(2, i, h['m1p5_m2p0'].GetBinContent(i))
                print "value for 2nd", h['m1p5_m2p0'].GetBinContent(i)
                SF.SetBinError(2,   i, h['m1p5_m2p0'].GetBinError(i))

                #SF.SetBinContent(3, i, h['m1pm4_m1p5'].GetBinContent(i))
                #print "value for 3rd", h['m1pm4_m1p5'].GetBinContent(i)
                #SF.SetBinError(3,   i, h['m1pm4_m1p5'].GetBinError(i))

                SF.SetBinContent(3, i, 0)
                print "value for 3rd", 0
                SF.SetBinError(3,   i, 0)

                SF.SetBinContent(4, i, h['m0p8_m1p4'].GetBinContent(i))
                print "value for 4th", h['m0p8_m1p4'].GetBinContent(i)
                SF.SetBinError(4,   i, h['m0p8_m1p4'].GetBinError(i))

                SF.SetBinContent(5, i, h['m0p8'].GetBinContent(i))
                print "value for 5th", h['m0p8'].GetBinContent(i)
                SF.SetBinError(5,   i, h['m0p8'].GetBinError(i))

                SF.SetBinContent(6, i, h['0p8'].GetBinContent(i))
                print "value for 6th", h['0p8'].GetBinContent(i)
                SF.SetBinError(6,   i, h['0p8'].GetBinError(i))

                SF.SetBinContent(7, i, h['0p8_1p4'].GetBinContent(i))
                print "value for 7th", h['0p8_1p4'].GetBinContent(i)
                SF.SetBinError(7,   i, h['0p8_1p4'].GetBinError(i))

                #SF.SetBinContent(8, i, h['1p4_1p5'].GetBinContent(i))
                #print "value for 8th", h['1p4_1p5'].GetBinContent(i)
                #SF.SetBinError(8,   i, h['1p4_1p5'].GetBinError(i))

                SF.SetBinContent(8, i, 0)
                print "value for 8th", 0
                SF.SetBinError(8,   i, 0)

                SF.SetBinContent(9, i, h['1p5_2p0'].GetBinContent(i))
                print "value for 9th", h['1p5_2p0'].GetBinContent(i)
                SF.SetBinError(9,   i, h['1p5_2p0'].GetBinError(i))

                SF.SetBinContent(10, i, h['2p0_2p5'].GetBinContent(i))
                print "value for 10th", h['2p0_2p5'].GetBinContent(i)
                SF.SetBinError(10,   i, h['2p0_2p5'].GetBinError(i))

        #c = ROOT.TCanvas("c", "Canvas", 1800, 1500)
        c = ROOT.TCanvas("c", "Canvas", 1800, 1500)
        ROOT.gStyle.SetPalette(1)
        SF.Draw("COLZ TEXT89E") #CONT1-5 #plots the graph with axes and points

        #if logy: ROOT.gPad.SetLogz()
        ROOT.gPad.SetLogy()
        c.Modified()
        c.Update()

        #Save canvas
        if year == "2016":
            if vfp == 'preVFP':
                savedir = "/groups/hephy/cms/fatih.okcu/www/StopsCompressed/TnP/final/2016_80X_v5_preVFP/2DleptonSF"
            else:
                savedir = "/groups/hephy/cms/fatih.okcu/www/StopsCompressed/TnP/final/2016_80X_v5_postVFP/2DleptonSF"
        elif year == "2017":
            savedir = "/groups/hephy/cms/fatih.okcu/www/StopsCompressed/TnP/final/2017_94X/2DleptonSF"
        elif year == "2018":
            savedir = "/groups/hephy/cms/fatih.okcu/www/StopsCompressed/TnP/final/2018_94_pre3/2DleptonSF"


        # savedir = '/groups/hephy/cms/fatih.okcu/StopsCompressed/results/2017_94X/2DleptonSF'
        #savedir = "/mnt/hephy/cms/priya.hussain/www/StopsCompressed/TnP/final/2017_94X/2DleptonSF"
        #savedir = "/mnt/hephy/cms/priya.hussain/www/StopsCompressed/TnP/final/2018_94_pre3/2DleptonSF/noIso"
        #savedir = "/mnt/hephy/cms/priya.hussain/www/StopsCompressed/TnP/final/2016_80X_v5/2DleptonSF/legacy/comp"
        #savedir = "/mnt/hephy/cms/priya.hussain/www/StopsCompressed/TnP/final/2016_80X_v5/2DleptonSF/mod"

        flavors = ['ele', 'muon']
        if self.flavor == "ele":
            etabins = ['all', '0p8', '0p8_1p4', '1p4_1p5', '1p5_2p0', '2p0_2p5', 'm0p8', 'm0p8_m1p4', 'm1pm4_m1p5', 'm1p5_m2p0', 'm2p0_m2p5']
            stages = ['Id', 'IpIso', 'IdSpec']
        else:
            etabins = ['all', '0p9', '0p9_1p2', '1p2_2p1', '2p1_2p4']
            stages = ['Id', 'IpIso', 'IpIsoSpec']
            flavors = flavors[::-1]

        time_interval = 4
        unique_times = np.arange(0, len(flavors)*len(stages)*len(etabins)*time_interval, time_interval)
        unique_times_dict = {fl: {st: {et: 0 for et in etabins} for st in stages} for fl in flavors}
        for i, (fl, st, et) in enumerate(product(flavors, stages, etabins)):
            unique_times_dict[fl][st][et] = unique_times[i]
        time.sleep(unique_times_dict[self.flavor][stage][etabin])

        makeDir(savedir)
        makeDir(savedir + '/root')
        makeDir(savedir + '/pdf')

        c.SaveAs("%s/2DleptonSF%s.png"      %(savedir, suffix))
        c.SaveAs("%s/pdf/2DleptonSF%s.pdf"  %(savedir, suffix))
        c.SaveAs("%s/root/2DleptonSF%s.root"%(savedir, suffix))

        # adds histogram to original file
        f.Write(histName, ROOT.TObject.kOverwrite)
        f.Close()

        return


if __name__ == "__main__":
    to_run = "fit"
    flavor = "ele"
    arg1 = "Data"
    arg2 = "Id"
    arg3 = "all"
    arg4 = "2016"
    arg5 = "postVFP"
    if len(sys.argv) > 1:
        to_run = sys.argv[1]
    if len(sys.argv) > 2:
        flavor = sys.argv[2]
    if len(sys.argv) > 3:
        arg1 = sys.argv[3]
    if len(sys.argv) > 4:
        arg2 = sys.argv[4]
    if len(sys.argv) > 5:
        arg3 = sys.argv[5]
    if len(sys.argv) > 6:
        arg4 = sys.argv[6]
    if len(sys.argv) > 7:
        arg5 = sys.argv[7]
    ScalingFactor(to_run, flavor, arg1, arg2, arg3, arg4, arg5)
