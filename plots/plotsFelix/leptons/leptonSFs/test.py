import os
import tkinter as tk
from tkinter import ttk

### VALUE LISTS

values_jobs = ["hist", "fit", "ploteff", "2DleptonSF"]

values_mode = ["Data", "MC"]
values_flavor = ["ele", "muon"]
values_stage = ["Id", "IpIso", "IdSpec (ele)", "IpIsoSpec (muon)"]
values_year = ["2016 (preVFP)", "2016 (postVFP)", "2017", "2018"]

### FUNCTIONS

submit_title = "jobs"

def submit(job, mode, flavor, stage, year):
	if flavor == "ele":
		etabins = ["0p8", "0p8_1p4", "1p4_1p5", "1p5_2p0", "2p0_2p5", "m0p8", "m0p8_m1p4", "m1pm4_m1p5", "m1p5_m2p0", "m2p0_m2p5", "all"]
	elif flavor == "muon":
		etabins = ["0p9", "0p9_1p2", "1p2_2p1", "2p1_2p4"]

	if job == "hist":
		submit_walltime = "72:00:00"
		if flavor == "ele":
			submit_job = "mod_ele_hist.py"
		elif flavor == "muon":
			submit_job = "mod_muon_hist.py"
		for mode_i in mode:
			for stage_i in stage:
				for year_i in year:
					print(submit_job, mode_i, stage_i, year_i)

	if job == "fit":
		if flavor == "ele":
			submit_job = "mod_ele_fit.py"
		elif flavor == "muon":
			submit_job = "mod_muon_fit.py"
		for mode_i in mode:
			for stage_i in stage:
				for year_i in year:
					for eta in etabins:
						print(submit_job, mode_i, stage_i, eta, year_i)

	if job == "ploteff":
		submit_job = "mod_ploteff.py"
		for stage_i in stage:
			for year_i in year:
				for eta in etabins:
					print(submit_job, flavor, stage_i, eta, year_i)

	if job == "2DleptonSF":
		submit_job = "mod_2DleptonSF.py"
		for stage_i in stage:
			for year_i in year:
				print(submit_job, flavor, stage_i, year_i)

def on_press_submit():
	#os.system("submit --title {} {}".format(submit_title, submit_job))
	job = values_jobs[jobmenu.current()]
	mode = [modemenu.get(i) for i in modemenu.curselection()]
	flavor = flavormenu.get(flavormenu.curselection())
	stage = [stagemenu.get(i) for i in stagemenu.curselection()]
	year = [yearmenu.get(i) for i in yearmenu.curselection()]
	submit(job, mode, flavor, stage, year)
	#print(b_flavor.current())


### ROOT WINDOW

width = 850
height = 300

root = tk.Tk()
root.geometry("%ix%i" %(width,height))

### JOBS

jobmenu = ttk.Combobox(root, values = values_jobs)
jobmenu.set("Pick Job")
jobmenu.place(x = 0.01*width,y = 0.2*height)

### MODE

mode_label = tk.Label(root, text = "Pick Mode")
mode_label.place(x = 0.24*width, y = 0.1*height)

modemenu = tk.Listbox(root, selectmode = "multiple", exportselection=False)
for mode in values_mode:
	modemenu.insert("end", mode)
modemenu.place(x = 0.24*width, y = 0.2*height)

### FLAVOR

flavor_label = tk.Label(root, text = "Pick Flavor")
flavor_label.place(x = 0.41*width, y = 0.1*height)

flavormenu = tk.Listbox(root, exportselection=False)
for flavor in values_flavor:
	flavormenu.insert("end", flavor)
flavormenu.place(x = 0.41*width, y = 0.2*height)

### STAGE

stage_label = tk.Label(root, text = "Pick Stage")
stage_label.place(x = 0.58*width, y = 0.1*height)

stagemenu = tk.Listbox(root, selectmode = "multiple", exportselection=False)
for stage in values_stage:
	stagemenu.insert("end", stage)
stagemenu.place(x = 0.58*width, y = 0.2*height)

### YEAR

year_label = tk.Label(root, text = "Pick Year")
year_label.place(x = 0.75*width, y = 0.1*height)

yearmenu = tk.Listbox(root, selectmode = "multiple", exportselection=False)
for year in values_year:
	yearmenu.insert("end", year)
yearmenu.place(x = 0.75*width, y = 0.2*height)

### RUN

b_run = tk.Button(root, text = "Submit", activebackground = "red", bg = "#00C20C", command = on_press_submit)
b_run.place(x = 0.5*width, y = 0.77*height)

### MAINLOOP

root.mainloop()
