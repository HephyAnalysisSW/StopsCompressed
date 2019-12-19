''' Object selection for StopsCompressed Analysis
'''

# StopsCompressed
from StopsCompressed.Tools.helpers import getVarValue, getObjDict, deltaR

# standard imports 
from math import *
import numbers
import textwrap  # needed for CutBased Ele ID
import operator

jetVars = ['eta','pt','phi','btagDeepB', 'btagCSVV2', 'jetId', 'area', 'rawFactor', 'corr_JER']

def getJets(c, jetVars=jetVars, jetColl="Jet"):
    return [getObjDict(c, jetColl+'_', jetVars, i) for i in range(int(getVarValue(c, 'n'+jetColl)))]

def jetId(j, ptCut=30, absEtaCut=2.4, ptVar='pt', idVar='jetId', corrFactor=None):
  j_pt = j[ptVar] if not corrFactor else j[ptVar]*j[corrFactor]
  return j_pt>ptCut and abs(j['eta'])<absEtaCut and ( j[idVar] > 0 if idVar is not None else True )

def getGoodJets(c, ptCut=30, absEtaCut=2.4, jetVars=jetVars, jetColl="Jet", ptVar='pt'):
    return filter(lambda j:jetId(j, ptCut=ptCut, absEtaCut=absEtaCut, ptVar='pt'), getJets(c, jetVars, jetColl=jetColl))

def getAllJets(c, leptons, ptCut=30, absEtaCut=2.4, jetVars=jetVars, jetCollections=[ "Jet"], idVar='jetId'):

    jets = sum( [ filter(lambda j:jetId(j, ptCut=ptCut, absEtaCut=absEtaCut, idVar=idVar), getJets(c, jetVars, jetColl=coll)) for coll in jetCollections], [] )
    res  = []

    for jet in jets:
        clean = True
        for lepton in leptons:
            if deltaR(lepton, jet) < 0.4:
                clean = False
                break
        if clean:
            res.append(jet)

    res.sort( key = lambda j:-j['pt'] )

    return res


def isBJet(j, tagger = 'DeepCSV', year = 2016):
    if tagger == 'CSVv2':
        if year == 2016:
            # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80XReReco
            return j['btagCSVV2'] > 0.8484 
        elif year == 2017 or year == 2018:
            # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
            return j['btagCSVV2'] > 0.8838 
        else:
            raise (NotImplementedError, "Don't know what cut to use for year %s"%year)
    elif tagger == 'DeepCSV':
        if year == 2016:
            # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80XReReco
            return j['btagDeepB'] > 0.6321
        elif year == 2017:
            # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
            return j['btagDeepB'] > 0.4941
        elif year == 2018:
            # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation102X
            return j['btagDeepB'] > 0.4184
        else:
            raise (NotImplementedError, "Don't know what cut to use for year %s"%year)

def getGenLeps(c):
    return [getObjDict(c, 'genLep_', ['eta','pt','phi','charge', 'pdgId', 'sourceId'], i) for i in range(int(getVarValue(c, 'ngenLep')))]

def getGenParts(c):
    return [getObjDict(c, 'GenPart_', ['eta','pt','phi','charge', 'pdgId', 'motherId', 'grandmotherId'], i) for i in range(int(getVarValue(c, 'nGenPart')))]

genVars = ['eta','pt','phi','mass','charge', 'status', 'pdgId', 'genPartIdxMother', 'statusFlags','index'] 
def getGenPartsAll(c, genVars=genVars):
    return [getObjDict(c, 'GenPart_', genVars, i) for i in range(int(getVarValue(c, 'nGenPart')))]

def genLepFromZ( genParts ):
    ''' get all gen leptons (e,m,tau) from Z
    '''
    try:
        leptons = list( filter( lambda l: abs(l['pdgId']) in [11,13,15] and abs(genParts[l['genPartIdxMother']]['pdgId']) == 23, genParts ) )
    except:
        print "Found no generated leptons"
        leptons = []
    return leptons

def get_index_str( index ):
    if isinstance(index, int):
        index_str = "["+str(index)+"]"
    elif type(index)==type(""):
        if index.startswith('[') and index.endswith(']'):
            index_str = index
        else:
            index_str = '['+index+']'
    elif index is None:
        index_str=""
    else:
        raise ValueError( "Don't know what to do with index %r" % index )
    return index_str

def alwaysTrue(*args, **kwargs):
  return True
def alwaysFalse(*args, **kwargs):
  return False

def mergeCollections( a, b ):
    allKeys = []
    for coll in [a[0], b[0]]:
        keys = coll.keys()
        for k in keys:
            if k not in allKeys: allKeys += [k]

    merged = a + b
    for m in merged:
        for key in allKeys:
            if not m.has_key(key):
                m[key] = float('nan')

    return merged

## MUONS ##
#def muonSelector( lepton_selection, year, ptCut = 10):
def muonSelector( lepton_selection, year):
    # tigher isolation applied on analysis level
    if lepton_selection == 'hybridIso':
        def func(l):
            if l["pt"] <= 25 and l["pt"] >3.5:
                return \
                    abs(l["eta"])       < 2.4 \
                    and (l['pfRelIso03_all']*l['pt']) < 5.0 \
                    and abs(l["dxy"])       < 0.02 \
                    and abs(l["dz"])        < 0.1 \
                    and l["looseId"] 
            elif l["pt"] > 25:
                return \
                    abs(l["eta"])       < 2.4 \
                    and l['pfRelIso03_all'] < 0.2 \
                    and abs(l["dxy"])       < 0.02 \
                    and abs(l["dz"])        < 0.1 \
                    and l["looseId"] 
                    
    elif lepton_selection == 'looseHybridIso':
        def func(l):
            if l["pt"] <= 25 and l["pt"] >3.5:
                return \
                    abs(l["eta"])       < 2.4 \
                    and (l['pfRelIso03_all']*l['pt']) < 20.0 \
                    and abs(l["dxy"])       < 0.1 \
                    and abs(l["dz"])        < 0.5 \
                    and l["looseId"] 
            elif l["pt"] > 25:
                return \
                    abs(l["eta"])       < 2.4 \
                    and l['pfRelIso03_all'] < 0.8 \
                    and abs(l["dxy"])       < 0.1 \
                    and abs(l["dz"])        < 0.5 \
                    and l["looseId"] 
    return func

def muonSelectorString(relIso03 = 0.2, ptCut = 20, absEtaCut = 2.4, dxy = 0.05, dz = 0.1, index = "Sum"):
    idx = None if (index is None) or (type(index)==type("") and index.lower()=="sum") else index
    index_str = get_index_str( index  = idx)
    string = [\
                "Muon_pt"+index_str+">=%s"%ptCut ,
                "abs(Muon_eta"+index_str+")<%s" % absEtaCut ,
                "Muon_looseId"+index_str+">=1" ,
                "abs(Muon_dxy"+index_str+")<%s" % dxy ,
                "abs(Muon_dz"+index_str+")<%s" % dz ,
                "Muon_pfRelIso03_all"+index_str+"<%s" % relIso03 ,
             ]
    if type(index)==type("") and index.lower()=='sum':
        return 'Sum$('+'&&'.join(string)+')'
    else:
        return '&&'.join(string)

## ELECTRONS ##

# Electron bitmap
# or  https://cms-nanoaod-integration.web.cern.ch/integration/master-102X/mc102X_doc.html
# Attention: only for nanoAOD v94x or higher (in 80x, only 2 bits are used)
vidNestedWPBitMapNamingList = \
    ['GsfEleMissingHitsCut',
     'GsfEleConversionVetoCut',
     'GsfEleRelPFIsoScaledCut',
     'GsfEleEInverseMinusPInverseCut',
     'GsfEleHadronicOverEMEnergyScaledCut',
     'GsfEleFull5x5SigmaIEtaIEtaCut',
     'GsfEleDPhiInCut',
     'GsfEleDEtaInSeedCut',
     'GsfEleSCEtaMultiRangeCut',
     'MinPtCut']
vidNestedWPBitMap           = { 'fail':0, 'veto':1, 'loose':2, 'medium':3, 'tight':4 }  # Bitwise (Electron vidNestedWPBitMap ID flags (3 bits per cut), '000'=0 is fail, '001'=1 is veto, '010'=2 is loose, '011'=3 is medium, '100'=4 is tight)

def cutBasedEleBitmap( integer ):
    return [int( x, 2 ) for x in textwrap.wrap("{0:030b}".format(integer),3) ]

def cbEleSelector( quality, removeCuts = [] ):
    if quality not in vidNestedWPBitMap.keys():
        raise Exception( "Don't know about quality %r" % quality )
    if type( removeCuts ) == str:
        removeCuts = [removeCuts]

    # construct a list of thresholds the electron has to satisfy 
    thresholds = []
    for cut in removeCuts:
        if cut not in vidNestedWPBitMapNamingList:
            raise Exception( "Don't know about ele cut %r" % cut )
    for cut in vidNestedWPBitMapNamingList:
        if cut not in removeCuts: 
            thresholds.append( vidNestedWPBitMap[quality] )
        else:
            thresholds.append( 0 )

    # construct the selector
    def _selector( integer ):
        return all(map( lambda x: operator.ge(*x), zip( cutBasedEleBitmap(integer), thresholds ) ))
    return _selector

#def eleSelector( lepton_selection, year, ptCut = 10):
def eleSelector( lepton_selection, year):
    # tighter isolation applied on analysis level. cutBased corresponds to Fall17V2 ID for all 2016-2018.  # (cut-based ID Fall17 V2 (0:fail, 1:veto, 2:loose, 3:medium, 4:tight))
    if lepton_selection == 'hybridIso':
        def func(l):
            if l["pt"] <= 25 and l["pt"] >5:
                return \
                    abs(l["eta"])       < 2.5 \
                    and l["convVeto"] \
                    and l['cutBased']       >= 1 \
                    and (l['pfRelIso03_all']*l['pt']) < 5.0 \
                    and abs(l["dxy"])       < 0.02 \
                    and abs(l["dz"])        < 0.1 
            elif l["pt"] > 25:
                
                return \
                    abs(l["eta"])       < 2.5 \
                    and l["convVeto"] \
                    and l['cutBased']       >= 1 \
                    and l['pfRelIso03_all'] < 0.2 \
                    and abs(l["dxy"])       < 0.02 \
                    and abs(l["dz"])        < 0.1 

    elif lepton_selection == 'looseHybridIso':
        def func(l):
            if l["pt"] <= 25 and l["pt"] >5:
                return \
                    abs(l["eta"])       < 2.5 \
                    and l["convVeto"] \
                    and l['cutBased']       >= 1 \
                    and (l['pfRelIso03_all']*l['pt']) < 20.0 \
                    and abs(l["dxy"])       < 0.1 \
                    and abs(l["dz"])        < 0.5 
            elif l["pt"] > 25:
                return \
                    abs(l["eta"])       < 2.5 \
                    and l["convVeto"] \
                    and l['cutBased']       >= 1 \
                    and l['pfRelIso03_all'] < 0.8 \
                    and abs(l["dxy"])       < 0.1 \
                    and abs(l["dz"])        < 0.5 
    return func

def eleSelectorString(relIso03 = 0.2, eleId = 1, ptCut = 20, absEtaCut = 2.5, dxy = 0.05, dz = 0.1, index = "Sum", noMissingHits=True):
    idx = None if (index is None) or (type(index)==type("") and index.lower()=="sum") else index
    index_str = get_index_str( index  = idx)
    string = [\
                "Electron_pt"+index_str+">=%s" % ptCut ,
                "abs(Electron_eta"+index_str+")<%s" % absEtaCut ,
                "Electron_convVeto"+index_str+"",
                "Electron_lostHits"+index_str+"==0" if noMissingHits else "(1)",
                "Electron_sip3d"+index_str+"<4.0" ,
                "abs(Electron_dxy"+index_str+")<%s" % dxy ,
                "abs(Electron_dz"+index_str+")<%s" % dz ,
                "Electron_pfRelIso03_all"+index_str+"<%s" % relIso03 ,
                "Electron_cutBased"+index_str+">=%s"%eleId , # Fall17V2 ID
             ]

    if type(index)==type("") and index.lower()=='sum':
        return 'Sum$('+'&&'.join(string)+')'
    else:
        return '&&'.join(string)

leptonVars_data = ['eta','etaSc', 'pt','phi','dxy', 'dz','tightId', 'pdgId', 'mediumMuonId', 'miniRelIso', 'relIso03', 'sip3d', 'mvaIdSpring15', 'convVeto', 'lostHits', 'jetPtRelv2', 'jetPtRatiov2', 'eleCutId_Spring2016_25ns_v1_ConvVetoDxyDz']
leptonVars = leptonVars_data + ['mcMatchId','mcMatchAny']

electronVars_data = ['pt','eta','phi','pdgId','cutBased','miniPFRelIso_all','pfRelIso03_all','sip3d','lostHits','convVeto','dxy','dz','charge','deltaEtaSC','mvaFall17V2noIso_WP80', 'vidNestedWPBitmap']
electronVars = electronVars_data + []

muonVars_data = ['pt','eta','phi','pdgId','mediumId','looseId','miniPFRelIso_all','pfRelIso03_all','sip3d','dxy','dz','charge']
muonVars = muonVars_data + []

def getLeptons(c, collVars=leptonVars):
    return [getObjDict(c, 'LepGood_', collVars, i) for i in range(int(getVarValue(c, 'nLepGood')))]

def getMuons(c, collVars=muonVars):
    return [getObjDict(c, 'Muon_', collVars, i) for i in range(int(getVarValue(c, 'nMuon')))]
def getElectrons(c, collVars=electronVars):
    return [getObjDict(c, 'Electron_', collVars, i) for i in range(int(getVarValue(c, 'nElectron')))]

def getGoodMuons(c, collVars=muonVars, mu_selector = alwaysFalse):
    return [l for l in getMuons(c, collVars) if mu_selector(l)]

def getGoodElectrons(c, collVars=electronVars, ele_selector = alwaysFalse):
    return [l for l in getElectrons(c, collVars) if ele_selector(l)]

idCutBased={'loose':0 ,'medium':1, 'tight':2}
photonVars=['eta','pt','phi','mass','cutBased']
photonVarsMC = photonVars + ['mcPt']

def getPhotons(c, collVars=None, idLevel='loose', year=2016):
    if collVars is None:
        collVars = ['eta','pt','phi','mass','cutBased'] if (not (year == 2017 or year == 2018)) else ['eta','pt','phi','mass','cutBasedBitmap']
    return [getObjDict(c, 'Photon_', collVars, i) for i in range(int(getVarValue(c, 'nPhoton')))]

def getGoodPhotons(c, ptCut=50, idLevel="loose", isData=True, collVars=None, year=2016):
    idVar = "cutBased" if (not (year == 2017 or year == 2018)) else "cutBasedBitmap"
    #if collVars is None: collVars = photonVars if isData else photonVarsMC
    collVars = ['eta','pt','phi','mass','cutBased'] if (not (year == 2017 or year == 2018)) else ['eta','pt','phi','mass','cutBasedBitmap']
    return [p for p in getPhotons(c, collVars) if p[idVar] > idCutBased[idLevel] and p['pt'] > ptCut ] # > 2 is tight for 2016, 2017 and 2018

