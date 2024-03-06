import os
import pandas as pd
import matplotlib.pyplot as plt
import ROOT
class csvGenFilter:
	def __init__(self, year):
		self.dataDir = os.path.join(os.environ["CMSSW_BASE"],"src/StopsCompressed/Tools/data/T2XX_filterEffs/UL")
		self.name = "csv_appended_filterEff.csv"
		self.csvFile    = os.path.join(self.dataDir,self.name)

		#self.name = "csv_filter_eff_T2tt_10K_dm40.csv"
		#self.name = "oldGenFilterEff.csv"
		#self.name = "oldGenFilterEffdm40.csv"

	def getfilterEff(self,mStop, mNeu):
		df = pd.read_csv(self.csvFile, usecols= ["m","dm","filterEff"])
		if mStop%5 != 0:
			mStop = mStop-1
		dM = mStop - mNeu
		print "stop value: ", mStop, 
		#if mStop in df['m'].values and dM in df['dm'].values:
		#	filterEff = df.loc[(df.m==mStop) & (df.dm==dM), 'filterEff'].values[0]
		#else:
		#	filterEff = df.loc[df['m'].le(mStop) & df['dm'].le(dM), 'filterEff'].values[0]
		filterEff = df.loc[(df.m==mStop ) & (df.dm==dM ),'filterEff'].values[0]
		print filterEff
		return filterEff

		##Plotting filter efficiency as a function of dm
		#df2= df[df['m'] < 825]
		#print "dataframe is: "
		#print df2
		#print df.to_string()
		#print "uodated dataframe: "
		#mstop=df["m"]
		#dm=df["dm"]
		#z=df["filterEff"]
		##plt.xticks(list(range(250,825,25)))
		#plt.xticks(list(range(250,1100,25)))
		#fig = plt.figure(figsize=(10, 10))
		#plt.xlabel('stop mass (GeV)')
		#plt.ylabel('dM')
		#plt.title('Filter Efficiency per  Stop mass and deltaM')
		##plt.figure(figsize=(20,20))
		#ax=plt.scatter(mstop, dm, c=z, s=100, vmin=0.1320, vmax=0.48)
		#plt.gcf().set_size_inches((20, 10))
		#plt.gcf().set_tight_layout(True)
		#plt.colorbar()
		#plt.savefig("filterEfficiencyMapdm40Updated.png")
		#plt.savefig("filterEfficiencyMapdm40Updated.pdf")
		##plt.savefig("oldFilterEfficiencyMapdM40.png")
		##plt.savefig("oldFilterEfficiencyMapdM40.pdf")
		#plt.show()

print "This is only for debug purposes"
g = csvGenFilter("2016")
print "using dataframes"
g.getfilterEff(550, 540)
g.getfilterEff(626, 615)
g.getfilterEff(926, 885)
