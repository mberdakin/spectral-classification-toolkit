import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
import seaborn as sns 


def PlotOverlap_random(df, path_to_res, num=5, filename= None): 
    """Naive aproach to overlap multiple spectra
    for df.
    df: the data frame should only include the spectra"""

    samples = df.sample(num)

    fig,ax = plt.subplots(figsize=(8,6))
    sns.lineplot(data=samples.transpose(), ax=ax)
    ax.set_ylabel("Intensity [a.u]")
    ax.set_xlabel("Wavelenght [nm]")
    if filename!=None:
        plt.savefig(f"{path_to_res}/{filename}.png")
    
    plt.show()


def Plot_zoom(df, path_to_res,
                       random= True, iloc=0, 
                       num=5, filename= None,
                       xmin=200, xmax =550,
                       ymin=-10, ymax= 1e4): 
    """Zoom in, one or randomly selected spectra 
    df: the data frame should only include the spectra"""

    if random == True: 
        samples = df.sample(num)
    else :
        samples = df.iloc[iloc]
        
    fig,ax = plt.subplots(figsize=(8,6))
    sns.lineplot(data=samples.transpose(), ax=ax)
    ax.set_ylabel("Intensity [a.u]")
    ax.set_xlabel("Wavelenght [nm]")
    ax.set_xlim(xmin,xmax)
    ax.set_ylim(ymin,ymax)

    if filename!=None:
        plt.savefig(f"{path_to_res}/{filename}.png")
    
    plt.show()


def Plot_CompareBaseline(df, df_base, path_to_res,
                       iloc=0, level=600, 
                       filename= None,
                       xmin=200, xmax =550,
                       ymin=-10, ymax= 1e4): 
    """Zoom in, one selected spectra with and without baseline 
    df: the data frame should only include the spectra"""

    sample1 = df.iloc[iloc]
    sample2 = df_base.iloc[iloc]

    fig,ax = plt.subplots(figsize=(8,6))
    sns.lineplot(data=sample1.transpose(), ax=ax)
    sns.scatterplot(data=sample2.transpose(), color='orange', ax=ax)

    ax.hlines(level,xmin,xmax)

    ax.set_ylabel("Intensity [a.u]")
    ax.set_xlabel("Wavelenght [nm]")
    ax.set_xlim(xmin,xmax)
    ax.set_ylim(ymin,ymax)

    if filename!=None:
        plt.savefig(f"{path_to_res}/{filename}.png")
    
    plt.show()


def Plot_groupBy_mean(df, path_to_res, alpha=0.5, filename=None):
    """Plot the average spectra of each experiment
    df: Full df, must include 'experiment' and 'file' columns
    """
    gb=df.drop(columns=["file"]).groupby(by=["experiment"]).mean()
    
    fig,ax = plt.subplots(figsize=(8,6))
    sns.lineplot(gb.transpose(),alpha=alpha, ax=ax)

    ax.set_ylabel("Intensity [a.u]")
    ax.set_xlabel("Wavelenght [nm]")

    if filename!=None:
        plt.savefig(f"{path_to_res}/{filename}.png")
    
    plt.show()


def Plot_with_std(df, path_to_res, alpha=0.5, filename=None,
                xmin=200, xmax =550,
                ymin=-10, ymax= 1e4): 
    
    """Plot the average spectra of each experiment with std
    df: Full df, must include 'experiment' and 'file' columns
    use: xmin,xmax,ymin,ymax for zoom and alpha for opacity"""

    print("this may take a bit")
    labels = df["experiment"].unique()
    fig,ax = plt.subplots(1,1, figsize=(8,6))

    for i in range(len(labels)):
        dff = df[df["experiment"]==labels[i]].drop(columns=["file","experiment"])
        sns.lineplot(data=dff.melt(), x="variable", y="value", ax=ax, alpha=0.5)

    ax.set_ylabel("Intensity [a.u]")
    ax.set_xlabel("Wavelenght [nm]")
    ax.set_xlim(xmin,xmax)
    ax.set_ylim(ymin,ymax)

    if filename!=None:
        plt.savefig(f"{path_to_res}/{filename}.png")
    
    plt.show()