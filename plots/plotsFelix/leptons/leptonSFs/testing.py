import numpy as np
from itertools import product

flavors = ['ele', 'muon']
stages = ['Id', 'IpIso', 'IdSpec']
etabins = ['all', '0p8', '0p8_1p4', '1p4_1p5', '1p5_2p0', '2p0_2p5', 'm0p8', 'm0p8_m1p4', 'm1pm4_m1p5', 'm1p5_m2p0', 'm2p0_m2p5']
time_interval = 4
unique_times = np.arange(0, len(flavors)*len(stages)*len(etabins)*time_interval, time_interval)
unique_times_dict = {fl: {st: {et: 0 for et in etabins} for st in stages} for fl in flavors}
print(product(flavors, stages, etabins))
for i, (fl, st, et) in enumerate(product(flavors, stages, etabins)):
    #print(i, fl, st, et)
    unique_times_dict[fl][st][et] = unique_times[i]

#time.sleep(unique_times_dict[flavor][stage][etabin])