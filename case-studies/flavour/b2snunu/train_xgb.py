import sys,os, argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.metrics import roc_curve, auc
#from root_pandas import read_root
import uproot
import ROOT
import joblib
import glob

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)

#Local code
from userConfig import loc, train_vars, train_vars_vtx, mode_names
import plotting
import utils as ut

def run(vars, signal, bbbar, ccbar, qqbar):

    #Bd -> Kst nu nu signal
    if(vars=="normal"):
        vars_list = train_vars
    elif(vars=="vtx"):
        vars_list = train_vars_vtx
    print("TRAINING VARS")
    print(vars_list)

    df_sig = pd.read_pickle(signal[0])
    for input_file in signal[1:]:
        df_sig = df_sig.append(pd.read_pickle(input_file))
    df_sig = df_sig[vars_list]
    print(f"Number of signal events: {len(df_sig)}")

    n_tot_bkg = 1e6

    #Efficiency of the pre-selection equirements on each bkg
    #eff = {}
    #Number of generated events for each background type
    #N = {}

    #bkgs = ["uds","cc","bb"]

    #Loop over all background files and calculate total number of generated events
    bkg_files = [*bbbar, *ccbar, *qqbar]
    df_bkg = pd.read_pickle(bkg_files[0])
    for input_file in bkg_files[1:]:
        df_bkg = df_bkg.append(pd.read_pickle(input_file))
    #for q in bkgs:
    #    N[q] = 0
    #    for f in files:
    #        tree = uproot.open(f)["metadata"]
    #        df_gen = tree.arrays(library="pd")
    #        #df_gen = read_root(f,"metadata")
    #        N[q] = N[q] + df_gen.iloc[0]["eventsProcessed"]

    #df_bkg = {}
    #for q in bkgs:
    #    df_bkg[q] = pd.read_pickle(f"{path}/{q}.pkl")#,usecols=vars_list)
    #    df_bkg[q] = df_bkg[q][vars_list]
    #    print(f"Total size of {q} sample: {len(df_bkg[q])}")
    #    eff[q] = float(len(df_bkg[q]))/N[q]
    #    print(f"Efficiency of pre-selection on {q} sample: {eff[q]}")
    #BF_tot = eff["uds"]*BF["uds"] + eff["cc"]*BF["cc"] + eff["bb"]*BF["bb"]
    #for q in bkgs:
    #    df_bkg[q] = df_bkg[q].sample(n=int(n_tot_bkg*(eff[q]*BF[q]/BF_tot)),random_state=10)
    #    print(f"Size of {q} in combined sample: {len(df_bkg[q])}")

    #Make a combined background sample according to BFs
    #df_bkg_tot = df_bkg["uds"].append(df_bkg["cc"])
    #df_bkg_tot = df_bkg_tot.append(df_bkg["bb"])
    #Shuffle the background so it is an even mixture of the modes
    #df_bkg_tot = df_bkg_tot.sample(frac=1)
    print(f"total bkg events {len(df_bkg)}")
"""
    #Signal and background labels
    df_sig["label"] = 1
    df_bkg["label"] = 0

    #Combine the datasets
    df_tot = df_sig.append(df_bkg)

    #Split into class label (y) and training vars (x)
    y = df_tot["label"]
    x = df_tot[vars_list]

    y = y.to_numpy()
    x = x.to_numpy()

    #Sample weights to balance the classes
    weights = compute_sample_weight(class_weight='balanced', y=y)

    #BDT
    config_dict = {
            "n_estimators": 400,
            "learning_rate": 0.3,
            "max_depth": 3,
            }

    bdt = xgb.XGBClassifier(n_estimators=config_dict["n_estimators"],
                            max_depth=config_dict["max_depth"],
                            learning_rate=config_dict["learning_rate"],
                            )

    #Fit the model
    print("Training model")
    bdt.fit(x, y, sample_weight=weights)

    feature_importances = pd.DataFrame(bdt.feature_importances_,
                                     index = vars_list,
                                     columns=['importance']).sort_values('importance',ascending=False)

    print("Feature importances")
    print(feature_importances)

    #Create ROC curves
    decisions = bdt.predict_proba(x)[:,1]

    # Compute ROC curves and area under the curve
    fpr, tpr, thresholds = roc_curve(y, decisions)
    roc_auc = auc(fpr, tpr)

    fig, ax = plt.subplots(figsize=(8,8))
    plt.plot(tpr, 1-fpr, lw=1.5, color="k", label='ROC (area = %0.3f)'%(roc_auc))
    plt.plot([0.45, 1.], [0.45, 1.], linestyle="--", color="k", label='50/50')
    plt.xlim(0.45,1.)
    plt.ylim(0.45,1.)
    plt.ylabel('Background rejection',fontsize=30)
    plt.xlabel('Signal efficiency',fontsize=30)
    ax.tick_params(axis='both', which='major', labelsize=25)
    plt.legend(loc="upper left",fontsize=20)
    plt.grid()
    plt.tight_layout()
    fname = f"{loc.PLOTS}/Bd2KstNuNu_vs_inclusive_Z_uds_cc_bb_ROC_{vars}.pdf"
    os.system("mkdir -p "+os.path.dirname(fname))
    print('Plotted ROC curve to', fname)
    fig.savefig(fname)

    #Write the model to a ROOT file on EOS, for application elsewhere in FCCAnalyses
    out = f"{loc.BDT}"
    print("Writing xgboost model to ROOT file")
    os.system(f"mkdir -p {out}") 
    ROOT.TMVA.Experimental.SaveXGBoost(bdt, "Bd2KstNuNu_BDT", f"{out}/xgb_bdt_{vars}.root", num_inputs=len(vars_list))

    #Write model to joblib file
    joblib.dump(bdt, f"{out}/xgb_bdt_{vars}.joblib")
"""
def main():
    parser = argparse.ArgumentParser(description='Train xgb model for Bc -> tau nu vs. Z -> qq, cc, bb')
    parser.add_argument("--vars", choices=["normal","vtx"], required=True, help="Event-level vars (normal) or added vertex vars (vtx)")
    parser.add_argument("--signal", nargs="+", required=True, help="signal ntuples")
    parser.add_argument("--inclusive_bbbar", nargs="+", required=True, help="bkg Z -> bb ntuples")
    parser.add_argument("--inclusive_ccbar", nargs="+", required=True, help="bkg Z -> cc ntuples")
    parser.add_argument("--inclusive_qqbar", nargs="+", required=True, help="bkg Z -> qq ntuples")
    args = parser.parse_args()

    run(args.vars, args.signal, args.inclusive_bbbar, args.inclusive_ccbar, args.inclusive_qqbar)

if __name__ == '__main__':
    main()