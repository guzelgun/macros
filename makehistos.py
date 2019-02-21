# # # #
# This code goes to 4 different data files, obtains required information
# and fills the histograms in order to compare certain properties of different signal samples.
# python makehistos.py fname1 fname2 fname3 fname4
# Ceren Guzelgun - 2018
# # # #


from ROOT import *
from utils import *
from histlib import *
import sys


gStyle.SetOptStat(0)
gStyle.SetFrameBorderMode(0)
gStyle.SetLegendBorderSize(0)
#gStyle.SetLegendTextSize(0.026)

try:fname =sys.argv[1]
except:
    fname = '/nfs/dust/cms/user/guezelgc/disappearingTracks/CMSSW_8_0_20/src/NTupleanalyzer/bkgHists/bkgHists_WJetsToLNu__TuneCUETP8M1_13TeV-madgraphMLM-pythia8_83_nFiles1.root'
    print 'files not specified, will run on 4 default files:'
    print 'catau: 55 cm'
try:fname2 = sys.argv[2]
except:
    fname2 = '/nfs/dust/cms/user/guezelgc/disappearingTracks/CMSSW_8_0_20/src/NTupleanalyzer/bkgHists/bkgHists_WJetsToLNu__TuneCUETP8M1_13TeV-madgraphMLM-pythia8_84_nFiles1.root'
    print 'catau: 90 cm'
try:fname3 = sys.argv[3]
except:
    fname3 = '/nfs/dust/cms/user/guezelgc/disappearingTracks/CMSSW_8_0_20/src/NTupleanalyzer/bkgHists/bkgHists_WJetsToLNu__TuneCUETP8M1_13TeV-madgraphMLM-pythia8_8_nFiles1.root'
    print 'catau: 3 cm'
try:fname4 = sys.argv[4]
except:
    fname4 = '/nfs/dust/cms/user/guezelgc/disappearingTracks/CMSSW_8_0_20/src/NTupleanalyzer/bkgHists/bkgHists_WJetsToLNu__TuneCUETP8M1_13TeV-madgraphMLM-pythia8_52_nFiles1.root'
    print 'catau: 22 cm'
#try:fname5 = sys.argv[5]
#except:
#    fname5 = 'hists_bkg.root'
#    print 'background: WJets2LNu'

#histolib = {}
#histolib['iso'] = 'relIso'


f  = TFile(fname)
f2 = TFile(fname2)
f3 = TFile(fname3)
f4 = TFile(fname4)
#f5 = TFile(fname5)
keys = f.GetListOfKeys()
#f.ls()
#*=*=*=*=*=for makinghist from a flat tuple
#t1 = f1.Get('Analysis')
#t2 = f2.Get('Analysis')
#t1.Show(0)

#for histkey in histolib:
#    t1.Draw(histolib[histkey])
#    t2.Draw(histolib[histkey],'same')
    
#    c1.Update()
#    pause()

c1 = mkcanvas('c1')
histlist = []

for key in keys:
    c1.SetLogy()
    hist = key.GetName()
    print hist
    histlist.append(hist[1:])
    h     = f.Get(hist)
    h2    = f2.Get(hist)
    h3    = f3.Get(hist)
    h4    = f4.Get(hist)
#    h5    = f5.Get(hist)
    overflow(h)
    overflow(h2)
    overflow(h3)
    overflow(h4)
#    overflow(h5)
    
######Normlise Hists
    n = 1
    if h.Integral() > 0 and h2.Integral() > 0 and h3.Integral() > 0 and h4.Integral() > 0: 
        s1= n/(h.Integral())
        h.Scale(s1)
        s2= n/(h2.Integral())
        h2.Scale(s2)
        s3= n/(h3.Integral())
        h3.Scale(s3)
        s4= n/(h4.Integral())
        h4.Scale(s4)
#    s5= n/(h5.Integral()) 
#    h5.Scale(s5)    

    #leg = TLegend(0.66,0.67,0.87,0.89)
    leg = TLegend(0.60,0.60,0.87,0.89)
    leg.SetHeader("Signal point (ctau,mass)")
    #histoStyler(h,1)
    h.SetLineWidth(2)
    h2.SetLineWidth(2)
    h3.SetLineWidth(2)
    h4.SetLineWidth(2)

    h.SetLineColor(kCyan);
    h2.SetLineColor(kRed);
    h3.SetLineColor(kBlue);
    h4.SetLineColor(kBlue); 
       
   # h.SetFillColor(kCyan)
   # h.SetFillStyle(3001)
   # h2.SetFillColor(kRed)
   # h2.SetFillStyle(3001)
   # h3.SetFillColor(kGreen+1)
   # h3.SetFillStyle(3001)
   # h4.SetFillColor(kBlue)
   # h4.SetFillStyle(3001)

    h.SetLineStyle(1);
    h2.SetLineStyle(1);
    h3.SetLineStyle(1);
    h4.SetLineStyle(1); 

    #h.SetFillColor(kCyan);
    #h2.SetFillColor(kRed-3);
    #h3.SetFillColor(kGreen-2);
    #h4.SetFillColor(kBlue-3);

    

    #h.SetLineStyle(2)
    h2.GetXaxis().SetTitle("")
    h2.GetXaxis().SetLabelSize(0.03)
    h2.GetYaxis().SetRangeUser(0.0001,4*max(h4.GetMaximum(),(max(h.GetMaximum(),h2.GetMaximum()))))
    h2.GetYaxis().SetTitle('Events norm to unity')
    h2.GetYaxis().SetTitleOffset(1.4)
    h2.SetTitle(histlib[hist[1:]])
    h2.Draw('hist')
    leg.SetTextSize(0.03)    
    leg.AddEntry(h,"10 cm, 177 GeV ","l")
    leg.AddEntry(h2,"100 cm, 177 GeV","l")
    leg.AddEntry(h3,"1000 cm, 177 GeV ","l")
    #leg.AddEntry(h4,"10000 cm, 177 GeV","l")


    h.Draw('histsame')
    h3.Draw('histsame')
    h4.Draw('histsame')

    leg.SetFillStyle(0)
    leg.Draw()
    c1.Update()

    pause()
    c1.Print(hist+'.pdf')

print 'histlib= {}'
for hist in histlist:
    print 'histlib["' + hist + '"] = "' + hist +'"'
