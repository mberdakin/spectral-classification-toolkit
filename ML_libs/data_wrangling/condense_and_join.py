#!/usr/bin/env python

import os as os
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 
import pandas as pd 
import warnings



def get_experiemnts(path_to_raw, show=False):
    """Get the list of experiment in a path 
    path_to_raw= Path to files 
    show = print list of experiments 
    """
    list_of_experiments= os.listdir(path_to_raw)
    if show == True:
        print (list_of_experiments)

    return list_of_experiments


def get_idx(experiment, seg, path_to_raw):
    """ get indexes of files with the desired part of the spectrum
        for a single experiment.
        experiment = path to experiment folder
        seg = segment of spectrum : Merge0 or name of spectrometer
        return list of index and name of files in experiment """

    listOffile = os.listdir(os.path.join(path_to_raw, experiment))
    # get indexes of files with the desired part of the spectrum.:
    idx =[]
    idx = [i for i, file in enumerate(listOffile) if seg in file]
    return idx,listOffile


def condense(dat_to_con, path_to_raw, seg, test=False):
    """ This function takes a list of experiments and condense all
    the spectra of that experiment in a single csv.
    This csv is stored in a experiment/condense.
    data_to_con= list of experiments
    seg = segment of the spectrum or Merge0
    test = Flag to return the last csv as DataFram
    """
    for experiment in dat_to_con:
        idx, listOffile = get_idx(experiment, seg, path_to_raw)
        exp_dir = os.path.join(path_to_raw, experiment)
        print(exp_dir)
        for i,index in enumerate(idx):
            data = pd.read_csv(os.path.join(exp_dir, listOffile[index]), delimiter=";", skiprows=2, header=None)
            data.replace(',', '.', regex=True, inplace=True)
            data = data.astype(float)
            ## Drop duplicated wavelenght, if there are:
            data.drop_duplicates(subset=0, keep="first", inplace=True)

            if i==0 : # Add wavelenght as column names :
                condense_data = pd.DataFrame(columns=data.iloc[:,0])

            condense_data.loc[i]= np.asanyarray(data.iloc[:,1])

        files = [listOffile[j] for j in idx]
        condense_data["file"] = files
        condense_data["experiment"] = experiment

        condensate_dir = os.path.join(exp_dir, "condensate")
        os.makedirs(condensate_dir, exist_ok=True)
        condense_data.to_csv(os.path.join(condensate_dir, f"{experiment}_{seg}_condense.csv"))

    if test == True:
        return data, condense_data


def join_data(path_to_raw, dat_to_con, seg):
    """Join the condensed data form multiple experiments
    path_to_raw= Path to files
    seg = segment of the spectrum or Merge0
    data_to_con= list of experiments needed for the model,
    tipically, 2 different experiments
    return join df
    """

    dfs = {}
    for i, experiment in enumerate(dat_to_con,1):
        dfs[f'df{i}'] = pd.read_csv(os.path.join(path_to_raw, experiment, "condensate", f"{experiment}_{seg}_condense.csv"))

    df_final = pd.concat(dfs.values(), ignore_index=True)
    df_final.drop(columns="Unnamed: 0", inplace=True)

    #Change column names to float (ugly approach):
    columns_to_keep_as_strings = ['file', 'experiment']

    # Create a new dictionary for renaming columns
    new_column_names = {}
    for col in df_final.columns:
        if col not in columns_to_keep_as_strings:
            # Convert column name to float if it's not in the keep list
            new_column_names[col]= float(col)
        else:
            # Keep the original name for specified columns
            new_column_names[col]= col

    # Rename the columns in the DataFrame
    df_final.rename(columns=new_column_names, inplace=True)

    return df_final


def normalize_dataframe(df):
    """Normalizes all spectra of a DataFrame
    to a range between 0 and 1.
    
    parameters:
    df (pd.DataFrame): The DataFrame to normalize.
    Returns:
    pd.DataFrame: A new DataFrame with normalized values.
    """

    df_raw = df.drop(columns=["file", "experiment"])
      # Calculate the min and max for each row
    row_min = df_raw.min(axis=1)
    row_max = df_raw.max(axis=1)
    
    # Normalize using the formula (x - min) / (max - min)
    normalized_df = (df_raw.sub(row_min, axis=0)).div(row_max - row_min, axis=0)
    normalized_df[["file", "experiment"]] = df[["file", "experiment"]]

    return normalized_df


def normalize_dataframe_to(df, peak, w):
    """Normalizes all spectra of a DataFrame
    to a single line, between 0 and 1.
    
    parameters:
    df (pd.DataFrame): The DataFrame to normalize.
    peak : line to normilize to 
    w: width of the line to select max intensity
    Returns:
    pd.DataFrame: A new DataFrame with normalized values.
    """

    df_raw = df.drop(columns=["file", "experiment"])
    
    #columns with peak :
    columns_in_range = df_raw.columns[(df_raw.columns >= peak - w) & (df_raw.columns <= peak + w)]
       
    #if there are nono, print a warning:
    if columns_in_range.empty:
        warnings.warn(f"No se encontró ningún máximo en el rango de {peak - w} a {peak + w} para el pico en {peak}.")
        
    # get the idx with the max position:        
    max_col = df_raw[columns_in_range].mean(axis=0).idxmax()
      
    # Normalize using the formula (x ) / (max at selected peak)
    normalized_df = (df_raw).div(df_raw[max_col] , axis=0)
    
    normalized_df[["file", "experiment"]] = df[["file", "experiment"]]

    return normalized_df


def filtter_noise_spec(df, peak, w, sigma):
    """Filtter noisy spect. Compute the mean intensity
    at peak frequency. Erase spectra that meet:
    peak(int)> Av_peak(int)+sigma
    peak(int)< Av_peak(int)-sigma
     
    
    parameters:
    df (pd.DataFrame): The DataFrame to normalize.
    peak : line to normilize to 
    w: width of the line to select max intensity
    sigma : percentage to filtter
    Returns:
    pd.DataFrame: A new DataFrame with normalized values.
    """

    df_raw = df.drop(columns=["file", "experiment"])
    
    #columns with peak :
    columns_in_range = df_raw.columns[(df_raw.columns >= peak - w) & (df_raw.columns <= peak + w)]
       
    #if there are nono, print a warning:
    if columns_in_range.empty:
        warnings.warn(f"No se encontró ningún máximo en el rango de {peak - w} a {peak + w} para el pico en {peak}.")
        
    # get the idx with the max position:        
    max_col = df_raw[columns_in_range].mean(axis=0).idxmax()

    peak_av = df_raw[max_col].mean()
    
    lim_max = peak_av+peak_av*sigma
    lim_min = peak_av-peak_av*sigma

    print(f"average:{peak_av.round(2)}, min:{lim_min.round(2)}, max:{lim_max.round(2)}")

#    to_filtter =  (df_raw[max_col] < lim_max) & (df_raw[max_col] > lim_min)
    to_filtter =  (df_raw[max_col] > lim_min)

    print(f"you are getting {sum(to_filtter)} from {len(to_filtter)} spects")

    filtter_df= df[to_filtter].copy()
    filtter_df[["file", "experiment"]] = df[["file", "experiment"]]

    return filtter_df


def remove_baseline(df, type="constant", level=1000):
    """Remove baseline from spectra
    type: "constant", "poly"
    """

    df_raw = df.drop(columns=["file", "experiment"])

    if type=="constant":
        df_mask = df_raw[df_raw>level].dropna(axis=1)

    ## TODO: type=poly
         
    df_mask[["file", "experiment"]] = df[["file", "experiment"]]

    return df_mask


def select_region(df, xmin=250, xmax=550):
    """Select a range of wavelenght.
   
     parameters:
    df (pd.DataFrame): The DataFrame to select.
    Returns:
    pd.DataFrame: A new DataFrame with the selected wavelenghts.
    """
   
    df_raw = df.drop(columns=["file", "experiment"])
    selected = [i for i in df_raw.columns if ((i>xmin) and (i<xmax))]
    selected = selected+["file", "experiment"]      
     
    return df[selected]


def select_peaks(df, peaks_centers, w): 
    
    selected_columns = []
    df_raw= df.drop(columns=["file", "experiment"])
    for peak_center in peaks_centers:
        # Encuentra las columnas dentro del rango del pico
        columns_in_range = df_raw.columns[(df_raw.columns >= peak_center - w) & (df_raw.columns <= peak_center + w)]
       
        if columns_in_range.empty:
            warnings.warn(f"No se encontró ningún máximo en el rango de {peak_center - w} a {peak_center + w} para el pico en {peak_center}.")
            continue
            
        max_col = df_raw[columns_in_range].mean(axis=0).idxmax()
        selected_columns.append(max_col)
    
    # Filtrar el DataFrame con las columnas seleccionadas
    return df[selected_columns+["file", "experiment"]]
    


