from ROOT import *
from math import *
import os, sys
import array

#datatag = "2016_80X_v5"

#binning = [5., 10., 20., 30., 45., 60., 100., 200.]
binning = [5., 10., 20., 35., 50., 100., 200., 500]
#etabinning = [0., 0.8, 1.442, 1.566, 2.0, 2.5]

x1 = array.array("d",binning)
nb = len(x1)-1
x2 = -999

mode = "Data"
if len(sys.argv)>1: mode = sys.argv[1]
if mode != "Data" and mode != "MC":
    print "wrong mode"
    sys.exit()

stage = "IpIso"
if len(sys.argv)>2: stage = sys.argv[2]
if stage != "IpIso" and stage != "Id" and stage != "IdSpec":
    print "wrong stage"
    sys.exit()

etabin = 'all'
if len(sys.argv)>3: etabin = sys.argv[3]
if etabin not in ['all', '0p8', '0p8_1p4', '1p4_1p5', '1p5_2p0', '2p0_2p5','m0p8', 'm0p8_m1p4', 'm1pm4_m1p5','m1p5_m2p0','m2p0_m2p5']:
	print "wrong etabin"
	sys.exit()

year = "2016"
if len(sys.argv)>4: year = sys.argv[4]
if year != "2016" and year != "2017" and year != "2018":
    print "wrong year"
    sys.exit()
#etabin = "all"
#if len(sys.argv)>3: etabin = sys.argv[3]
#if etabin != "barrel" and etabin != "endcap" and etabin != "all":
#    print "wrong etabin"
#    sys.exit()
if year == "2016":
	datatag = "2016_80X_v5"
elif year == "2017":
	datatag ="2017_94X"
elif year == "2018":
	datatag ="2018_94_pre3"
def makeDir(path):
    if "." in path[-5:]:
            path = path.replace(os.path.basename(path),"")
            print path
    if os.path.isdir(path):
            return
    else:
            os.makedirs(path)

makeDir("/scratch/priya.hussain/StopsCompressed/results/%s/fits/noIso"%datatag)

pout = ["lowedge","pthigh","mean","sigma","alpha","n","sigma2","gaus1f","a","signal","bkg"]

fpout = open("/scratch/priya.hussain/StopsCompressed/results/%s/fits/noIso/el_%s_%s.params"%(datatag,mode,stage),"w")
sout = "\t".join(pout)
fpout.write(sout+"\n")
#2017&2018 noISo hists location
#fin = TFile("/scratch/priya.hussain/StopsCompressed/results/%s/hists/noIso/ele_histos_%s_%s.root"%(datatag,mode,stage))
#2016 legacy hists location
fin = TFile("/scratch/priya.hussain/StopsCompressed/results/%s/legacy/hists/ele_histos_%s_%s.root"%(datatag,mode,stage))
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
    

fout = TFile("/scratch/priya.hussain/StopsCompressed/results/%s/fits/noIso/ele_result_%s_%s_%s.root"%(datatag,mode,stage,etabin),"recreate")

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
    savedir = "/mnt/hephy/cms/priya.hussain/www/StopsCompressed/TnP/%s/fits/noIso/%s/%s"%(datatag,mode,stage)
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

