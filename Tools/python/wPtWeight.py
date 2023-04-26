
class wPtWeight:
	def __init__(self, year):
		if year == 'UL2016_preVFP':
			self.norm = 1.046
		elif year == 'UL2016':
			self.norm = 1.048
		elif year == 'UL2017':
			self.norm = 1.042
		elif year == 'UL2018':
			self.norm = 1.043
		else:
			self.norm = 1
		#Parameters for 2016 data
		self.params    = { 
				#'norm' : 0.94,
				'a0'   : 1.00,
				'a1'   : 1.052,
				'a2'   : 1.179, #greater than 1
				'a3'   : 1.150, #greater than 1
				'a4'   : 1.057,
				'a5'   : 1.000,
				'a6'   : 0.912,
				'a7'   : 0.783,
				}
	def wPtWeight(self,wpt, sigma=0):
		#norm = self.params['norm']
		wPt = wpt
		#wPt = r.leptons[0]['wPt']
		#print "Wpt :", wPt
		if wPt < 50:
			a = 'a0'
		elif wPt >= 50 and wPt < 100:
			a = 'a1'
		elif wPt >= 100 and wPt < 150:
			a = 'a2'
		elif wPt >= 150 and wPt < 200:
			a = 'a3'
		elif wPt >= 200 and wPt < 300:
			a = 'a4'
		elif wPt >= 300 and wPt < 400:
			a = 'a5'
		elif wPt >= 400 and wPt < 600:
			a = 'a6'
		elif wPt >= 600:
			a = 'a7'
		else:
			print "Error: Issue with computing wPt weight"
		corr_fact = self.params[a]
		#print "weights: wPt %s , correction factor: %s"%(wPt,corr_fact)
		#w = (norm*corr_fact)+(self.sys*sigma)

		if sigma==0:
			#print (norm*corr_fact)
			return (self.norm*corr_fact)
		elif sigma <0:
			#print ((norm*corr_fact)**2)
			return ((self.norm*corr_fact)**2)
		elif sigma>0:
			#print 1
			return 1
		##up=no weight, nom=weighted, down= (reweight)^2
		#print "weight calculated in function: ", w 
		#return (norm*corr_fact)+(sys_fact*sigma) 
		#return	()	
