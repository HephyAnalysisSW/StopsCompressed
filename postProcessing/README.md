# Signal Production

nanoAOD samples need to be in the respective python file in Samples repository. In order to obtain normalization of each sample, run `getWeightForSignals.py` , e.g.,
```
python getWeightsForSignals.py --year UL2016 --sample SMS_T2tt_LL_mStop_300_mLSP_290
```
Remaining samples for UL can be found in `getWeightsForSignals_UL.sh`.

After this, you can post-process the signal samples without each job having to obtain the normalizations again.
Post-processing is run e.g.,
```
python nanoPostProcessing.py  --skim Met --year UL2018  --processingEra compstops_UL18v9_nano_v10 --susySignal  --sample SMS_T2tt_mStop_500_mLSP_420
```
For the grids add `--fastSim` for proper propagation of L1PrefireWeghts, which are not stired in susy fast sim grids unlike susy signal points.
```
python nanoPostProcessing.py  --skim Met --year UL2016  --processingEra compstops_UL16v9_nano_v10  --susySignal --sample SMS_T2tt_mStop_250to1100_dM_10to30
```
The samples can always be submitted in multiple (N) jobs, with the use of #SPLITN at the end of the command before submitting it.
# Signal Splitting
The last step of processing is to split the sample into seperate files for each mass-point.
```
python nanoSignalSplitting.py --year UL2016 --T2tt --processingEra compstops_UL16v9_nano_v10 --inputDir /groups/hephy/cms/priya.hussain/StopsCompressed/nanoTuples/  --targetDir /scratch-cbe/users/priya.hussain/StopsCompressed/nanoTuples/  --skim Met --samples SMS_T2tt_mStop_250to1100_dM_10to30
```
More examples can be found in `nanoSignalSplitting.sh`. For now the splitting works for prompt grid, some changes need to be implemented for long lived grid according to the ctau and BR for each point.
