import ROOT
import math
#dx_file 	= ROOT.TFile("/groups/hephy/cms/priya.hussain/www/StopsCompressed/analysisPlots/HInoDxyDz/v_UL03_Central/Run2016postVFP/alllog/nISRJets1p-ntau0-lepSel-deltaPhiJets-jet3Veto-met200-ht300/l1_abs_dxy_full_nodxydz.root")
#dz_file 	= ROOT.TFile("/groups/hephy/cms/priya.hussain/www/StopsCompressed/analysisPlots/HInoDxyDz/v_UL03_Central/Run2016postVFP/alllog/nISRJets1p-ntau0-lepSel-deltaPhiJets-jet3Veto-met200-ht300/l1_abs_dz_nodxydz.root")
dz_file 	= ROOT.TFile("/groups/hephy/cms/priya.hussain/www/StopsCompressed/analysisPlots/HInoDxyDz/v_UL05_Central/Run2016postVFP/alllog/nISRJets1p-ntau0-lepSel-deltaPhiJets-jet3Veto-met200-ht300/stop1_Lxy.root")

#dx_PromptFile 	= ROOT.TFile("/groups/hephy/cms/priya.hussain/www/StopsCompressed/analysisPlots/HInoDxyDz/v_UL04_Central/Run2016postVFP/alllog/nISRJets1p-ntau0-lepSel-deltaPhiJets-jet3Veto-met200-ht300-isFake/l1_abs_dxy_full_nodxydz.root")
#dz_PromptFile 	= ROOT.TFile("/groups/hephy/cms/priya.hussain/www/StopsCompressed/analysisPlots/HInoDxyDz/v_UL04_Central/Run2016postVFP/alllog/nISRJets1p-ntau0-lepSel-deltaPhiJets-jet3Veto-met200-ht300-isFake//l1_abs_dz_nodxydz.root")
dz_PromptFile 	= ROOT.TFile("/groups/hephy/cms/priya.hussain/www/StopsCompressed/analysisPlots/HInoDxyDz/v_UL05_Central/Run2016postVFP/alllog/nISRJets1p-ntau0-lepSel-deltaPhiJets-jet3Veto-met200-ht300-isFake/stop1_Lxy.root")

#dx_canvas	= dx_file.Get("46772e75_f1da_41a3_93e4_196ead034184")
#dz_canvas	= dz_file.Get("c1ad8c45_2d12_4795_a1cd_86cc88b782b9")
#LXY changes: 
dz_canvas	= dz_file.Get("ce1ce54c_f462_443f_85f7_dda23dc9ae76")
dz_PromptCanvas	= dz_PromptFile.Get("4b7182a2_f771_4c05_987f_07d6900231d1")

#dx_PromptCanvas	= dx_PromptFile.Get("57804ff7_fe0f_4cfc_8398_e0e1856a7aa9")
#dz_PromptCanvas	= dz_PromptFile.Get("18c01fcf_3386_42bf_8efa_ce44a94cc6d6")

LL_dm_20       = (dz_canvas.FindObject("ce1ce54c_f462_443f_85f7_dda23dc9ae76_1")).GetPrimitive("stop1_Lxy_T2tt_LL_400_380_a1db6025_cd66_4039_9d81_d1cc900e7a8a")
LL_dm_15       = (dz_canvas.FindObject("ce1ce54c_f462_443f_85f7_dda23dc9ae76_1")).GetPrimitive("stop1_Lxy_T2tt_LL_350_335_da63ec94_cc8c_46f4_87f5_873881da025c")
LL_dm_10       = (dz_canvas.FindObject("ce1ce54c_f462_443f_85f7_dda23dc9ae76_1")).GetPrimitive("stop1_Lxy_T2tt_LL_300_290_ad4983ad_88a3_4cf2_ada1_7fed2f44a234")
dm_30	       = (dz_canvas.FindObject("ce1ce54c_f462_443f_85f7_dda23dc9ae76_1")).GetPrimitive("stop1_Lxy_T2tt_500_470_af37446a_43ad_4713_9a91_4d04d3e1cdbd")


LL_Prompt_dm_20       = (dz_PromptCanvas.FindObject("4b7182a2_f771_4c05_987f_07d6900231d1_1")).GetPrimitive("stop1_Lxy_T2tt_LL_400_380_41a67059_5e2e_4f2d_87d2_46fd4122f497")
LL_Prompt_dm_15       = (dz_PromptCanvas.FindObject("4b7182a2_f771_4c05_987f_07d6900231d1_1")).GetPrimitive("stop1_Lxy_T2tt_LL_350_335_9dd6951a_be35_488c_94ae_75626e51f084")
LL_Prompt_dm_10       = (dz_PromptCanvas.FindObject("4b7182a2_f771_4c05_987f_07d6900231d1_1")).GetPrimitive("stop1_Lxy_T2tt_LL_300_290_7b31ecb1_f06a_4ff9_ab36_5d4afa9c759d")
Prompt_dm_30	      = (dz_PromptCanvas.FindObject("4b7182a2_f771_4c05_987f_07d6900231d1_1")).GetPrimitive("stop1_Lxy_T2tt_500_470_894273cc_7be5_4016_9041_101d0dcf0e98")

#LL_Prompt_dm_20       = (dx_PromptCanvas.FindObject("c9d68bc1_ff8f_4c00_bb93_4aa58e5eb7b0_1")).GetPrimitive("")
#LL_Prompt_dm_15       = (dx_PromptCanvas.FindObject("c9d68bc1_ff8f_4c00_bb93_4aa58e5eb7b0_1")).GetPrimitive("")
#LL_Prompt_dm_10       = (dx_PromptCanvas.FindObject("c9d68bc1_ff8f_4c00_bb93_4aa58e5eb7b0_1")).GetPrimitive("")
#Prompt_dm_30	      = (dx_PromptCanvas.FindObject("c9d68bc1_ff8f_4c00_bb93_4aa58e5eb7b0_1")).GetPrimitive("")

LL_dm20_ratio = LL_Prompt_dm_20.Clone("Ratio LL ctau 0p3")
LL_dm20_ratio.Divide(LL_dm_20)

LL_dm15_ratio = LL_Prompt_dm_15.Clone("Ratio LL ctau 15p7")
LL_dm15_ratio.Divide(LL_dm_15)

LL_dm10_ratio = LL_Prompt_dm_10.Clone("Ratio LL ctau 7892p9")
LL_dm10_ratio.Divide(LL_dm_10)

dm30_ratio = Prompt_dm_30.Clone("Ratio T2tt 500 470")
dm30_ratio.Divide(dm_30)

ROOT.gStyle.SetErrorX(0)
ROOT.gStyle.SetOptStat(0)
c = ROOT.TCanvas('c', '', 1400, 1000)
leg1 = ROOT.TLegend(0.7, 0.84, 0.9, 0.94)

signal = [LL_dm20_ratio, LL_dm15_ratio, LL_dm10_ratio, dm30_ratio ]

for i, sig in enumerate(signal):
	print "name of histo: ", sig.GetName()
	leg1.AddEntry(signal[i], sig.GetName() ,"l")
	signal[i].SetLineColor(i+1)
	signal[i].SetLineWidth(2)
	if i==0:
		signal[i].SetTitle("Ratio Fake leptons to all leptons HI& no dxy, dz")
		signal[i].GetYaxis().SetTitle("#frac{Fake}{all HI & no dxy,dz}")
		#signal[i].SetTitle("Ratio HI to no HI dxy")
		#signal[i].GetYaxis().SetTitle("#frac{HI}{noHI}")
		signal[i].GetYaxis().SetRangeUser(0,1.1)
		signal[i].Draw('hist')
	else:
		signal[i].Draw('histsame')
leg1.Draw('same')
c.Update()
c.SaveAs("Ratio_isFake_wHI_allLeptons_signal_lxy.pdf")
c.SaveAs("Ratio_isFake_wHI_allLeptons_signal_lxy.png")
#c.SaveAs("Ratio_isFake_wHI_allLeptons_signal_dz.pdf")
#c.SaveAs("Ratio_isFake_wHI_allLeptons_signal_dz.png")
#c.SaveAs("Ratio_isPrompt_wHI_isPrompt_looseHI_dxy_dz_signal.pdf")
#c.SaveAs("Ratio_isPrompt_wHI_isPrompt_looseHI_dxy_dz_signal.png")
#c.SaveAs("Ratio_isPrompt_wHI_all_signal.png")
#c.SaveAs("Ratio_isIso_all_signal.pdf")
#c.SaveAs("Ratio_isIso_all_signal.png")
#c.SaveAs("Ratio_isIso_all_signal.root")
