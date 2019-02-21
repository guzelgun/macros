# # # #
# Chi2 test of DATA & BKG, with function chi2test(), and manually.
# It ignores the bins with under 10 events, applies a cut then adds the sum of cut bins as an overflow bin.
# Ceren Guzelgun - 2018
# # # #

from ROOT import *
from utils import *
#from histlib import *
import sys

gStyle.SetOptStat(0)
gStyle.SetFrameBorderMode(0)
gStyle.SetLegendBorderSize(0)
gROOT.ForceStyle()

try: fname = sys.argv[1]
except:
    fname = 'Var_METFB_17_35invfb_mt_SR.root'

f  = TFile(fname)
keys = f.GetListOfKeys()

h  = f.Get("data_obs")
h2 = f.Get("allbkg_METFB_17")

nbins = h.GetSize()
nbins = nbins - 2
nbins_bkg = h2.GetSize()
nbins_bkg = nbins_bkg - 2
if (nbins != nbins_bkg):
    print "Histograms have different binning!!"
else:
    print("Histograms have " +repr(nbins) + " bins.")

B = h.GetSumOfWeights()
A = h2.GetSumOfWeights()

suma = 0
bins = []
for i in range(1, nbins):
        a = h.GetBinContent(i)
        if a < 10:
            suma = suma + a
            bins.append(i)
print "Sum of the events in DATA bins with low statistics is: " + repr(suma)
print "The first bin with low statistics is: " +repr(bins[0])

sumb = 0
for j in range(bins[0],nbins):
        a_bk = h2.GetBinContent(j)
        sumb = sumb + a_bk
print "Sum of the events in BKG bins with low statistics is: " + repr(sumb)

h.SetBinContent(bins[0]-1, suma)
h2.SetBinContent(bins[0]-1,sumb)
h.GetXaxis().SetRange(1,bins[0]-1)
h2.GetXaxis().SetRange(1,bins[0]-1)
h.SetLineColor(kRed)
h.Draw("hist")
h2.Draw("same")

chi2sum=0
for i in range(1,bins[0]-1):
    #try:
    n = h.GetBinContent(i)
    m = h2.GetBinContent(i)
    chi2 = (1/(A*B))*(((A*n-B*m)**2)/(n+m))
    print "for "+repr(i)+"th bin, chi2 is "+repr(chi2)
    chi2sum = chi2sum + chi2
    #except:
    #    verem=1
print "chi2sum is= " + repr(chi2sum)

b = h.Chi2Test(h2,"WW P")
print b

###LEgend
leg = TLegend(0.60,0.60,0.87,0.89)
leg.AddEntry(h,"DATA","l")
leg.AddEntry(h2,"BKG","l")
leg.AddEntry(0,"CHI2/NDF =  %.2f" %b,"")
leg.Draw()
pause()

