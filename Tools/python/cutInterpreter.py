''' Class to interpret string based cuts
'''

import logging
logger = logging.getLogger(__name__)

jetSelection    = "nJetGood"
bJetSelectionM  = "nBTag"
ISRJet          = "nISRJets"
mIsoWP = { "VT":5, "T":4, "M":3 , "L":2 , "VL":1, 0:"None" }

special_cuts = {
    "deltaPhiJetsInverted"  	:  "dphij0j1>=2.5",
    "deltaPhiJets"  	        :  "dphij0j1<2.5",
    "deltaPhiMetJetsInv"	:  "dPhiMetJet<0.5",
    "deltaPhiJetsmod"           :  "dphij0j1<2.5&&dphij0j1>0",
    "lepSel"        	        :  "Sum$(lep_pt>20)<=1&&l1_pt>0",
    "lpt"           	        :  "l1_pt>0",
    "jet3Veto"      	        :  "(nJetGood<=2||Alt$(JetGood_pt[2],0)<60)",
    "jet3VetoInverted"      	:  "(nJetGood>2&&Alt$(JetGood_pt[2],0)>=60)",
    
    "jet3VetoOld"   	:  "(nJetGood<=2||JetGood_pt[2]<60)",
    "jet3Vetobad"   	:  "(nJetGood<=2)",
    "nHardJetsTo2"  	:  "Sum$(JetGood_pt>=60&&abs(Jet_eta)<2.4)<=2",
    "HEMJetVetoWide"	:  "Sum$(JetGood_pt>20&&JetGood_eta<-1.0&&JetGood_eta>-3.2&&JetGood_phi<-0.5&&JetGood_phi>-2.0)==0",
    "HEMElectronVetoWide"	:  "Sum$(Electron_eta<-1.0&&Electron_eta>-3.2&&Electron_phi<-0.5&&Electron_phi>-2.0)==0",
    "HEMElVetoWide"	:  "Sum$(Electron_eta<-1.392&&Electron_eta>-3.00&&Electron_phi<-0.87&&Electron_phi>-1.57)==0",
    "HEMElVetoWidePt"	:  "Sum$(Electron_pt>30&&Electron_eta<-1.392&&Electron_eta>-3.00&&Electron_phi<-0.87&&Electron_phi>-1.57)==0",
    "mu"		:  "abs(l1_pdgId)==13",
    "e"			:  "abs(l1_pdgId)==11",
    "all"		:  "(1)",
    "isPrompt"          :  "l1_isPrompt>0",
    "isFake"            :  "l1_isPrompt==0",
    "isGenMatched"      :  "l1_isGenMatched>0",
    "veryLow"		:  "l1_pt<5",
    "low"		:  "l1_pt>=5&&l1_pt<12",
    "medium"		:  "l1_pt>=12&&l1_pt<30",

  }

continous_variables = [ ("met", "met_pt"), ("mt", "mt"), ("ht", "HT") , ('ISRJets_pt', 'ISRJets_pt'), ("nPV", "PV_npvsGood"), ("lpt","l1_pt") ,("leta","abs(l1_eta)"), ("Cone", "CT1"), ("Ctwo", "CT2"),("dphimetjet","dPhiMetJet"), ("dxy", "abs(l1_dxy)")]
discrete_variables  = [ ("njet", "nJetGood"), ("nbtag", "nBTag") ,("nHardJet", "Sum$(JetGood_pt>=60&&abs(Jet_eta)<2.4)"), ("nSoftJets", "Sum$(JetGood_pt>=30&&JetGood_pt<60&&abs(Jet_eta)<2.4)"), ("nISRJets", "nISRJets"),( "ntau","nGoodTaus"),("nSoftBJets", "nSoftBJets"),("nHardBJets", "nHardBJets"), ("nISR", "nISR"), ("isPrompt","l1_isPrompt")]

class cutInterpreter:
    ''' Translate var100to200-var2p etc.
    '''

    @staticmethod
    def translate_cut_to_string( string ):

        if string.startswith("multiIso"):
            str_ = mIsoWP[ string.replace('multiIso','') ]
            return "l1_mIsoWP>%i&&l2_mIsoWP>%i" % (str_, str_)
        elif string.startswith("relIso"):
           iso = float( string.replace('relIso','') )
           #raise ValueError("We do not want to use relIso for our analysis anymore!")
           return "l1_relIso03<%3.2f&&l2_relIso03<%3.2f"%( iso, iso )
        elif string.startswith("miniIso"):
           iso = float( string.replace('miniIso','') )
           return "l1_miniRelIso<%3.2f&&l2_miniRelIso<%3.2f"%( iso, iso )
        # special cuts
        if string in special_cuts.keys(): return special_cuts[string]
        if string == "":
            return "(1)"

        # continous Variables
        for var, tree_var in continous_variables:
            if string.startswith( var ):
                num_str = string[len( var ):].replace("to","To").split("To")
                upper = None
                lower = None
                if len(num_str)==2:
                    lower, upper = num_str
                    lower = lower.replace("p",".")
                    upper = upper.replace("p",".")
                elif len(num_str)==1:
                    lower = num_str[0]
                    lower = lower.replace("p",".")
                else:
                    raise ValueError( "Can't interpret string %s" % string )
                
               
                res_string = []
                if lower: res_string.append( tree_var+">="+lower )
                if upper: res_string.append( tree_var+"<"+upper )
                return "&&".join( res_string )

        # discrete Variables
        for var, tree_var in discrete_variables:
            logger.debug("Reading discrete cut %s as %s"%(var, tree_var))
            if string.startswith( var ):
                # So far no njet2To5
                if string[len( var ):].replace("to","To").count("To"):
                    raise NotImplementedError( "Can't interpret string with 'to' for discrete variable: %s. You just volunteered." % string )

                num_str = string[len( var ):]
                # logger.debug("Num string is %s"%(num_str))
                # var1p -> tree_var >= 1
                if num_str[-1] == 'p' and len(num_str)==2:
                    # logger.debug("Using cut string %s"%(tree_var+">="+num_str[0]))
                    return tree_var+">="+num_str[0]
                # var123->tree_var==1||tree_var==2||tree_var==3
                else:
                    vls = [ tree_var+"=="+c for c in num_str ]
                    if len(vls)==1:
                      # logger.debug("Using cut string %s"%vls[0])
                      return vls[0]
                    else:
                      # logger.debug("Using cut string %s"%'('+'||'.join(vls)+')')
                      return '('+'||'.join(vls)+')'
        raise ValueError( "Can't interpret string %s. All cuts %s" % (string,  ", ".join( [ c[0] for c in continous_variables + discrete_variables] +  special_cuts.keys() ) ) )

    @staticmethod
    def cutString( cut, select = [""], ignore = [], photonEstimated=False):
        ''' Cutstring syntax: cut1-cut2-cut3
        '''
        cuts = cut.split('-')
        # require selected
        cuts = filter( lambda c: any( sel in c for sel in select ), cuts )
        # ignore
        cuts = filter( lambda c: not any( ign in c for ign in ignore ), cuts )


        cutString = "&&".join( map( cutInterpreter.translate_cut_to_string, cuts ) )
        if cut == "":
          cutString = "(1)"
        return cutString
    
    @staticmethod
    def cutList ( cut, select = [""], ignore = []):
        ''' Cutstring syntax: cut1-cut2-cut3
        '''
        cuts = cut.split('-')
        # require selected
        cuts = filter( lambda c: any( sel in c for sel in select ), cuts )
        # ignore
        cuts = filter( lambda c: not any( ign in c for ign in ignore ), cuts )
        return [ cutInterpreter.translate_cut_to_string(cut) for cut in cuts ] 
        #return  "&&".join( map( cutInterpreter.translate_cut_to_string, cuts ) )

if __name__ == "__main__":
    print cutInterpreter.cutString("lepSel-nISRJets1p-nHardJetsTo2-deltaPhiJets-met300")
    #print cutInterpreter.cutString("")
    #print cutInterpreter.cutList("njet2-btag0p-multiIsoVT-relIso0.12-looseLeptonVeto-mll20-onZ-met80-metSig5-dPhiJet0-dPhiJet1-mt2ll100")
