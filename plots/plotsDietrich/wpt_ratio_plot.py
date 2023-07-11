import ROOT as R
import sys

outname = sys.argv[1]
norm = int(sys.argv[2])

_file = R.TFile("help_all_nISRJets1p-ntau0-lepSel-deltaPhiJets-jet3Veto-met200-ht300.root")

if (outname == "l1_pt") :
    nom_l1pt = _file.Get("l1pt_WJetsToLNu_HT__8506153e_0a34_430e_a160_3c1d52be9c96")   
    up_l1pt = _file.Get( "l1pt_up_WJetsToLNu_HT__aa22ba45_88ab_4289_8626_d30ceefc0a60")  
    up_l1pt.SetLineColor(2) 

if (outname == "W_pt") :
    nom_l1pt = _file.Get("Wpt_WJetsToLNu_HT__a7512a4a_962b_406f_830c_d4487f2d2f52")   
    up_l1pt = _file.Get( "Wpt_up_WJetsToLNu_HT__6d0d1c42_96d9_4c07_b94a_5857ff66f23b")  
    up_l1pt.SetLineColor(2) 


# _file = R.TFile("help_all_lepSel.root")

# if (outname == "l1_pt") :
#     nom_l1pt = _file.Get("l1pt_WJetsToLNu_HT__c34cb623_76d3_45b6_adcf_016432716927")   
#     up_l1pt = _file.Get( "l1pt_up_WJetsToLNu_HT__62c9114e_d11a_464d_bc67_68db21533490")  
#     up_l1pt.SetLineColor(2) 

# if (outname == "W_pt") :
#     nom_l1pt = _file.Get("Wpt_WJetsToLNu_HT__1a3fa76a_f25a_40bb_99d8_298463629f22")   
#     up_l1pt = _file.Get( "Wpt_up_WJetsToLNu_HT__4d2e145e_30f9_4fe0_8c3a_45ecce76d5b0")  
#     up_l1pt.SetLineColor(2) 



if norm :
    print up_l1pt.Integral()
    print nom_l1pt.Integral()
    print up_l1pt.Integral() / nom_l1pt.Integral()
    nom_l1pt.Scale(1./nom_l1pt.Integral())
    up_l1pt.Scale(1./up_l1pt.Integral()) 
    

    outname += "_norm"
nom_l1pt.GetXaxis().SetLabelFont(63)
nom_l1pt.GetXaxis().SetLabelSize(16)
nom_l1pt.GetYaxis().SetLabelFont(63)
nom_l1pt.GetYaxis().SetLabelSize(16)
c1 = R.TCanvas()

pad1 = R.TPad("pad1","pad1",0,0.3,1,1)
pad1.SetBottomMargin(0)
pad1.Draw()
pad1.cd()
nom_l1pt.DrawCopy()
up_l1pt.Draw("same") 
c1.cd()
pad2 = R.TPad("pad2","pad2",0,0,1,0.3)
pad2.SetTopMargin(0)
pad2.Draw()
pad2.cd()
# nom_l1pt.Sumw2()
nom_l1pt.SetStats(0)
nom_l1pt.Divide(up_l1pt)
nom_l1pt.SetMarkerStyle(21)
nom_l1pt.Draw("ep")
# nom_l1pt.GetXaxis().SetTitle("l1 pT")
c1.cd()

c1.SaveAs("{}.png".format(outname))

