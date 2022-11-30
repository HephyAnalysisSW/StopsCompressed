import ROOT

print('hey')
print('hey2')
f = ROOT.TF1("f1", "sin(x)/x", 0., 10.)
f.Draw()
print('hey3')