#! /usr/bin/env python

from ROOT import *
import sys
from DataFormats.FWLite import Events, Handle
from glob import glob


# Make VarParsing object 
# https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideAboutPythonConfigFile#VarParsing_Example
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')
options.parseArguments()

def main():


    inputFiles = options.inputFiles
    if inputFiles == []:
        print 'running on the EDM file AODSIM'
        inputFiles = ['/nfs/dust/cms/user/guezelgc/disappearingTracks/CMSSW_8_0_21/src/AODSIM/AODSIM100CM/pMSSM12_MCMC1_27_969542_cff_c177_100cm_9nFiles1.root']


    events = Events(inputFiles)

# create handle and labels of loop

    handle_genparticles  = Handle ("vector<reco::GenParticle>") #strings to use here are learned from AODSIM by edmdumpeventcontent
    label_genparticles = ('genParticlePlusGeant')

    handle_jets = Handle ("vector<reco::PFJet>")
    label_jets = ('ak4PFJetsCHS')

    handle_muons = Handle ("vector<reco::Muon>")
    label_muons = ('muons')

    handle_pfmet = Handle ("vector<reco::PFMET>")
    label_pfmet = ('pfMet')

    handle_tracks  = Handle ("vector<reco::Track>")
    label_tracks = ('generalTracks')

# Create histograms, etc.
    gROOT.SetBatch()        # don't pop up canvases
    gROOT.SetStyle('Plain') # white background 

#define histograms
    hJet1   = TH1F("hJet1", "p_{T} of the 1^{st} Hardest Jet", 80, 0, 2200) # fill min Delta R of charginos
    hJet2   = TH1F("hJet2", "p_{T} of the 2^{nd} Hardest Jet", 80, 0, 2200)
    hJet3   = TH1F("hJet3", "p_{T} of the 3^{rd} Hardest Jet", 40, 0, 1100)
    hJets   = TH1F("hJets", "number of jets", 10,0,30) 
    hchipt  = TH1F("hchipt","gen #chi^{#pm} p_{T}",80,0,2000)
    hneutpt = TH1F("hneutpt","gen #chi^{0} p_{T}",80,0,2000) 

    for event in events:

        event.getByLabel (label_jets, handle_jets)
        event.getByLabel(label_genparticles, handle_genparticles)
    # get the product 

        jets = handle_jets.product()
        genparticles = handle_genparticles.product()
#loop over the gen particles, can also loop over muons, electrons jets etc
        for gp in genparticles:
	    if abs(gp.pdgId()) == 1000022:
                hneutpt.Fill(gp.pt())
            if abs(gp.pdgId()) == 1000024 and gp.status() == 1:
                hchipt.Fill(gp.pt())
       
	ptmax = 0
        for ijet, jet in enumerate(jets):
            if jet.pt() > 0:
                ptMax = jet.pt()
                jet_id = ijet
                  
	hJet1.Fill(jets[0].pt())
        hJet2.Fill(jets[1].pt())
        hJet3.Fill(jets[2].pt())
	nJets = getJET(jets)
        hJets.Fill(nJets)
        
    identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('_step2','').replace('_AODSIM','').replace('_*','').replace('*','')
    identifier+='nFiles'+str(len(inputFiles))
    fnew = TFile('comparison_'+identifier+'.root','recreate')
    #fnew = TFile('sample_DENEME.root','recreate') # save hists in a root file
    hJets.Write()
    hJet1.Write()
    hJet2.Write()
    hJet3.Write()
    hchipt.Write()
    hneutpt.Write()

def DPtRel(track, genp):
    dptrel = abs((track.pt()-genp.pt())/genp.pt())
    return dptrel

def getHT(jetlist = [], *args):
    ht =0
    for jet in jetlist:
        if jet.pt()< 25:continue
        ht = ht + jet.pt()
    return ht

def getJET(jetlist = [], *args):
    j =0
    for jet in jetlist:
        if jet.pt() < 20:continue    
        looseID= 1
        if abs(jet.eta()) < 2.4: looseID = jet.neutralEmEnergyFraction() < .99 and jet.neutralHadronEnergyFraction() < .99 and jet.numberOfDaughters() > 1 and jet.chargedEmEnergyFraction() < .99 and jet.chargedHadronEnergyFraction() > 0 and  jet.chargedMultiplicity() > 0
        if abs(jet.eta()) >= 2.4: looseID = jet.neutralEmEnergyFraction() < .99 and jet.neutralHadronEnergyFraction() < .99 and jet.numberOfDaughters() > 1
        if looseID == 0:continue
        j = j + 1    
    return j

main()



