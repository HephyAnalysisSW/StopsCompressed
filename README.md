# StopsCompressed

Installaion
```bash
cmsrel CMSSW_10_6_25
cd CMSSW_10_6_25/src
cmsenv

# Download patched version of install_correctionslib.sh
curl -sLO https://gist.githubusercontent.com/dietrichliko/96865aa4c47d7fabc7d746d163fc7cf5/raw/943ebc27101408c14659cc25d935565936da7fc9/install_correctionslib.sh
. ./install_correctionslib.sh
rm install_correctionslib.sh

# clone repositories
git clone git@github.com:HephyAnalysisSW/StopsCompressed -b UltraLegacy
git clone git@github.com:HephyAnalysisSW/Samples.git -b StopsCompressedUL
git clone git@github.com:HephyAnalysisSW/RootTools.git -b StopCompressed
git clone git@github.com:HephyAnalysisSW/Analysis.git -b StopsCompressed
git clone git@github.com:priyasajid/nanoAOD-tools.git PhysicsTools/NanoAODTools

#compile
scram b -j4
```

Install [combine](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/) from HiggsAnalysis

```bash
cd $CMSSW_BASE/src
git clone git@github.com:cms-analysis/HiggsAnalysis-CombinedLimit.git \
    HiggsAnalysis/CombinedLimit -b v8.2.0
cd HiggsAnalysis/CombinedLimit

scramv1 b clean # always make a clean build
scramv1 b -j4 
```

For combine tools

```bash
cd $CMSSW_BASE/src/HiggsAnalysis
bash <(curl -s https://raw.githubusercontent.com/cms-analysis/CombineHarvester/master/CombineTools/scripts/sparse-checkout-ssh.sh)

scram b -j4
```
