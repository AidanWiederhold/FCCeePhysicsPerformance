import os
#repo = os.getenv('PWD')
repo = "/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bd2KstNuNu/analysis"
#repo can be changed, but by default writes locally
class loc : pass
loc.root = repo+'/'
loc.out = loc.root+'output/'
loc.data = loc.root+'data'
loc.csv = loc.data+'/csv'
loc.pkl = loc.data+'/pkl'
loc.root_files = loc.data+'/ROOT'
loc.plots = loc.out+'plots'
loc.tex = loc.out+'tex'
loc.json = loc.out+'json'

#EOS location for files used in analysis
loc.eos = "/eos/experiment/fcc/ee/analyses/case-studies/flavour/Bd2KstNuNu"

#Output BDT model location - used in official sample production to assign MVA weights
loc.bdt = loc.eos+""

#Location of prod_04 tuples used in analysis
loc.prod = f"{loc.eos}/flatNtuples/spring2022/prod_01"

#Samples for first stage BDT training
loc.train = f"{loc.prod}/Batch_Training_4stage1/"

#Samples for second stage training
loc.train_2 = f"{loc.prod}/Training_4stage2/"

#Samples for final analysis
loc.analysis = f"{loc.prod}/Analysis_stage2/"

#First stage BDT including event-level vars
train_vars = ["EVT_ThrustEmin_E",
              "EVT_ThrustEmax_E",
              "EVT_ThrustEmin_Echarged",
              "EVT_ThrustEmax_Echarged",
              "EVT_ThrustEmin_Eneutral",
              "EVT_ThrustEmax_Eneutral",
              "EVT_ThrustEmin_Ncharged",
              "EVT_ThrustEmax_Ncharged",
              "EVT_ThrustEmin_Nneutral",
              "EVT_ThrustEmax_Nneutral"
              ]

#First stage BDT including event-level vars and vertex vars
#This is the default list used in the analysis
train_vars_vtx = [*train_vars, *[
                  "EVT_NtracksPV",
                  "EVT_NVertex",
                  "EVT_NKPi",
                  "EVT_ThrustEmin_NDV",
                  "EVT_ThrustEmax_NDV",
                  "EVT_dPV2DVmin",
                  "EVT_dPV2DVmax",
                  "EVT_dPV2DVave"
                  ]]


#Decay modes used in first stage training and their respective file names
mode_names = {"Bd2KstNuNu": "p8_ee_Zbb_ecm91_EvtGen_Bd2KstNuNu",
              "uds": "p8_ee_Zuds_ecm91",
              "cc": "p8_ee_Zcc_ecm91",
              "bb": "p8_ee_Zbb_ecm91"
              }

#Second stage training variables
train_vars_2 = ["EVT_CandMass",
                "EVT_CandRho1Mass",
                "EVT_CandRho2Mass",
                "EVT_CandN",
                "EVT_CandVtxFD",
                "EVT_CandVtxChi2",
                "EVT_CandPx",
                "EVT_CandPy",
                "EVT_CandPz",
                "EVT_CandP",
                "EVT_CandD0",
                "EVT_CandZ0",
                "EVT_CandAngleThrust",
                "EVT_DVd0_min",
                "EVT_DVd0_max",
                "EVT_DVd0_ave",
                "EVT_DVz0_min",
                "EVT_DVz0_max",
                "EVT_DVz0_ave",
                "EVT_PVmass",
                "EVT_Nominal_B_E"
               ]

#Hemisphere energy difference cut, applied offline prior to MVA2 optimisation
energy_difference_cut = ">10."
