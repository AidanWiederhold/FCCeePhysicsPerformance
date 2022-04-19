import sys, os, argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xgboost as xgb
import joblib

#Local code
from userConfig import loc, train_vars, train_vars_vtx
import plotting
import utils as ut

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Roman']})
rc('text', usetex=True)

def run(vars):
    # Load trained model
    bdt = joblib.load(f"{loc.BDT}/xgb_bdt_{vars}.joblib")

    #Bd -> Kst nu nu signal
    if(vars=="normal"):
        vars_list = train_vars
    elif(vars=="vtx"):
        vars_list = train_vars_vtx

    #Load samples

    #Bd -> Kst nu nu signal
    path = f"{loc.PKL}"
    df_sig = pd.read_pickle(f"{path}/Bd2KstNuNu.pkl")
    df_sig = df_sig[vars_list]
    df_sig["BDT"] = bdt.predict_proba(df_sig).tolist()
    df_sig["BDT"] = df_sig["BDT"].apply(lambda x: x[1])

    #Z -> qq inclusive
    df_bkg = {}
    x_bkg = {}
    y_bkg = {}
    bkgs = {"uds": ["#d1e5f0","q\\bar{q}"],
            "cc": ["#92c5de","c\\bar{c}"],
            "bb": ["#2166ac","b\\bar{b}"]
            }
    for q in bkgs:
        df_bkg[q] = pd.read_pickle(f"{path}/{q}.pkl")
        df_bkg[q] = df_bkg[q].sample(n=200000,random_state=100)
        df_bkg[q] = df_bkg[q][vars_list]
        df_bkg[q]["BDT"] = bdt.predict_proba(df_bkg[q]).tolist()
        df_bkg[q]["BDT"] = df_bkg[q]["BDT"].apply(lambda x: x[1])

    fig, ax = plt.subplots(figsize=(12,8))
    xmin = 0
    xmax = 1
    bins_bkg = int(np.sqrt(len(df_bkg["cc"])))
    bins_sig = int(np.sqrt(len(df_sig)))
    plt.hist(df_sig["BDT"],bins=bins_sig,range=(xmin,xmax),density=True,color="#b2182b",histtype='step',linewidth=1.5)
    plt.hist(df_sig["BDT"],bins=bins_sig,range=(xmin,xmax),density=True,color="#b2182b",histtype='stepfilled',alpha=0.3,linewidth=1.5,label="$B^0 \\to K^{*0} \\nu \\bar \\nu$")
    for q in bkgs:
        plt.hist(df_bkg[q]["BDT"],bins=bins_bkg,range=(xmin,xmax),density=True,color=bkgs[q][0],histtype='step',linewidth=1.5,label="Inc. $Z^0 \\to %s$" % bkgs[q][1])
    ax.tick_params(axis='both', which='major', labelsize=25)
    plt.xlim(xmin,xmax)
    plt.xlabel("BDT1 score",fontsize=30)
    plt.ylabel("Normalised counts",fontsize=30)
    plt.yscale('log')
    ymin,ymax = plt.ylim()
    plt.ylim(ymin,50*ymax)
    plt.legend(fontsize=25, loc="upper left")
    plt.tight_layout()
    fname = f"{loc.PLOTS}/Bd2KstNuNu_vs_inclusive_Z_uds_cc_bb_BDT_{vars}.pdf"
    fig.savefig(fname)
    print("Saved plot:", fname)

    #Plot efficiency as a function of BDT cut in each sample
    BDT_cuts = np.linspace(0,999,999)
    N_sig = len(df_sig)
    N_Zuds = len(df_bkg["uds"])
    N_Zcc = len(df_bkg["cc"])
    N_Zbb = len(df_bkg["bb"])
    eff_sig = []
    eff_bkg = {}
    N_bkg = {}
    for q in bkgs:
        eff_bkg[q] = []
        N_bkg[q] = len(df_bkg[q])
    cut_vals = []
    for x in BDT_cuts:
        cut_val = float(x)/100
        cut_vals.append(cut_val)
        eff_sig.append(float(len(df_sig.query("BDT > %s" % cut_val))) / N_sig)
        for q in bkgs:
            eff_bkg[q].append(float(len(df_bkg[q].query("BDT > %s" % cut_val))) / N_bkg[q])

    fig, ax = plt.subplots(figsize=(12,8))

    plt.plot(cut_vals, eff_sig, color="#b2182b",label="$B^0 \\to K^{*0} \\nu \\bar \\nu$")
    for q in bkgs:
        plt.plot(cut_vals, eff_bkg[q], color=bkgs[q][0],label="Inc. $Z^0 \\to %s$" % bkgs[q][1])

    ax.tick_params(axis='both', which='major', labelsize=25)
    plt.xlim(xmin,xmax)
    plt.xlabel("BDT1 score",fontsize=30)
    plt.ylabel("Efficiency",fontsize=30)
    plt.yscale('log')
    ymin,ymax = plt.ylim()
    plt.ylim(ymin,2)
    plt.legend(fontsize=25, loc="lower left")
    plt.grid(alpha=0.4,which="both")
    plt.tight_layout()
    fig.savefig(f"{loc.PLOTS}/Bd2KstNuNu_vs_inclusive_Z_uds_cc_bb_BDT_eff_{vars}.pdf")


def main():
    parser = argparse.ArgumentParser(description='Plot xgb model for Bd -> Kst nu nu vs. Z -> qq, cc, bb')
    parser.add_argument("--Vars", choices=["normal","vtx"],required=False,help="Event-level vars (normal) or added vertex vars (vtx)",default="vtx")
    args = parser.parse_args()

    run(args.Vars)

if __name__ == '__main__':
    main()
