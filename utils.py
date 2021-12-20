import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import StratifiedKFold, KFold
from sklearn.metrics import accuracy_score,f1_score
from sklearn.neighbors import NearestNeighbors
from scipy.stats import entropy
import scipy as sp
from scipy.stats import gaussian_kde, wasserstein_distance
from scipy.stats import norm
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy.ma as ma
from sklearn.metrics import mean_squared_error
from dython.nominal import associations, numerical_encoding
from sdv.metrics.tabular import CSTest, KSTest
from preprocess import change_dtype, find_cateorical_columns, match_dtypes


def PCD(real,synthetic):
    # print(real.isna().sum())
    # print(synthetic.isna().sum())

    # if(real.isnull().values.any()):
    #     real.fillna("0", inplace=True)

    # if(synthetic.isnull().values.any()):
    #     synthetic.fillna("0", inplace=True)

    # print(real.isna().sum())
    # print(synthetic.isna().sum())

    real = change_dtype(real)
    synthetic = match_dtypes(real,synthetic)
    # for col in synthetic.columns:
    #     print(synthetic[col].value_counts())

    synthetic.to_csv('synthetic.csv',index=False)


    # print(real.isna().sum())
    # print(synthetic.isna().sum())

    # if(real.isnull().values.any()):
    #     real.fillna("0", inplace=True)

    # if(synthetic.isnull().values.any()):
    #     synthetic.fillna("0", inplace=True)
    print(np.linalg.norm((associations(real,nan_strategy='drop_samples',compute_only=True)['corr'] - associations(synthetic,nan_strategy='drop_samples',compute_only=True)['corr']),ord='fro'))
    return np.linalg.norm((associations(real,nan_strategy='drop_samples',compute_only=True)['corr'] - associations(synthetic,nan_strategy='drop_samples',compute_only=True)['corr']),ord='fro')
    # return np.linalg.norm((associations(real,nan_strategy='replace',nan_replace_value='nan',nominal_columns='auto',nom_nom_assoc='cramer', num_num_assoc='pearson',compute_only=True)['corr'] - associations(synthetic,nan_strategy='replace',nan_replace_value='nan',nominal_columns='auto',nom_nom_assoc='cramer', num_num_assoc='pearson',compute_only=True)['corr']),ord='fro')

def stat_test(real,synthetic):
    real = change_dtype(real)
    synthetic = match_dtypes(real,synthetic)
    kstest = KSTest.compute(real, synthetic)
    cstest = CSTest.compute(real, synthetic)
    return kstest, cstest


def wass_distance(real,synthetic):
    real = real.sample(n=real.shape[0]).reset_index(drop = True)
    synthetic = synthetic.sample(n=real.shape[0]).reset_index(drop = True)
    return wasserstein_distance(real,synthetic)

def DCR(real,synthetic):
    neigh = NearestNeighbors(n_neighbors=1,algorithm='ball_tree')
    neigh.fit(synthetic.values)
    total_dist = []
    for ix,row in real.iterrows():
        dist,ix = neigh.kneighbors([row.values],return_distance=True)
        total_dist.append(dist)
    return np.mean(total_dist), np.std(total_dist)

def DCkR(real,synthetic,k=3):
    neigh = NearestNeighbors(n_neighbors=k,algorithm='ball_tree')
    neigh.fit(synthetic.values)
    total_dist = []
    dist_lst = []
    for ix,row in real.iterrows():
        dist,ix = neigh.kneighbors([row.values],return_distance=True)
        dist_lst.append(np.squeeze(dist))
    return np.array(dist_lst).mean(axis=0)

def NNDR(real,synthetic):
    neigh = NearestNeighbors(n_neighbors=2,algorithm='ball_tree')
    neigh.fit(synthetic.values)
    total_dist = []
    for ix,row in real.iterrows():
        dist,ix = neigh.kneighbors([row.values],return_distance=True)
        first = np.squeeze(dist)[0]
        second = np.squeeze(dist)[1]
        if(first == 0 and second ==0):
            ratio = 0
        else:
            ratio = first/second
        assert 0<=ratio<=1
        total_dist.append(ratio)
    return np.mean(total_dist), np.std(total_dist)




def predictive_model(real,synthetic,class_col,mode='TSTR'):
    acc_synth_lst = []
    f1_synth_lst = []

    acc_real_lst = []
    f1_real_lst = []
    if(mode=='TSTR'):
        X_real = real.drop(class_col,axis=1)
        y_real = real[class_col]
        
        X = synthetic.drop(class_col,axis=1)
        y = synthetic[class_col]
        skf = KFold(n_splits=5, shuffle=True, random_state=1)
        for train_index, test_index in skf.split(X, y):
            xtrain, xtest = X.iloc[train_index], X.iloc[test_index]
            ytrain, ytest = y.iloc[train_index], y.iloc[test_index]
            mod = RandomForestClassifier()
            mod.fit(xtrain,ytrain)
            
            synth_test_pred = mod.predict(xtest)
            accuracy_synth,f1_synth = plot_metrics(synth_test_pred, ytest)
            acc_synth_lst.append(accuracy_synth)
            f1_synth_lst.append(f1_synth)

            
            real_test_pred = mod.predict(X_real)
            accuracy_real,f1_real = plot_metrics(real_test_pred, y_real)
            acc_real_lst.append(accuracy_real)
            f1_real_lst.append(f1_real)
            
            return np.mean(acc_real_lst),np.mean(f1_real_lst)
        
    elif(mode=='TRTS'):
        X_real = real.drop(class_col,axis=1)
        y_real = real[class_col]
        
        X = synthetic.drop(class_col,axis=1)
        y = synthetic[class_col]
        skf = KFold(n_splits=5, shuffle=True, random_state=1)
        for train_index, test_index in skf.split(X_real, y_real):
            xtrain, xtest = X_real.iloc[train_index], X_real.iloc[test_index]
            ytrain, ytest = y_real.iloc[train_index], y_real.iloc[test_index]
            mod = RandomForestClassifier()
            mod.fit(xtrain,ytrain)
            real_test_pred = mod.predict(xtest)
            accuracy_real,f1_real = plot_metrics(real_test_pred, ytest)
            acc_real_lst.append(accuracy_real)
            f1_real_lst.append(f1_real)

            
            synth_test_pred = mod.predict(X)
            accuracy_synth,f1_synth = plot_metrics(synth_test_pred, y)
            acc_synth_lst.append(accuracy_synth)
            f1_synth_lst.append(f1_synth)

            return np.mean(acc_synth_lst),np.mean(f1_synth_lst)

def regression_model(real,synthetic,class_col,mode='TSTR'):
    rmse_synth_lst = []
    mape_synth_lst = []

    rmse_real_lst = []
    mape_real_lst = []
    if(mode=='TSTR'):
        X_real = real.drop(class_col,axis=1)
        y_real = real[class_col]
        
        X = synthetic.drop(class_col,axis=1)
        y = synthetic[class_col]
        skf = KFold(n_splits=5, shuffle=True, random_state=1)
        for train_index, test_index in skf.split(X, y):
            xtrain, xtest = X.iloc[train_index], X.iloc[test_index]
            ytrain, ytest = y.iloc[train_index], y.iloc[test_index]
            mod = RandomForestRegressor()
            mod.fit(xtrain,ytrain)
            
            synth_test_pred = mod.predict(xtest)
            rmse_synth = rmse(synth_test_pred, ytest)
            mape_synth = mape(synth_test_pred, ytest)
            rmse_synth_lst.append(rmse_synth)
            mape_synth_lst.append(mape_synth)

            
            real_test_pred = mod.predict(X_real)
            rmse_real = rmse(real_test_pred, y_real)
            mape_real = mape(real_test_pred, y_real)
            rmse_real_lst.append(rmse_real)
            mape_real_lst.append(mape_real)
            
            return np.mean(rmse_real_lst),np.mean(mape_real_lst)
        
    elif(mode=='TRTS'):
        X_real = real.drop(class_col,axis=1)
        y_real = real[class_col]
        
        X = synthetic.drop(class_col,axis=1)
        y = synthetic[class_col]
        skf = KFold(n_splits=5, shuffle=True, random_state=1)
        for train_index, test_index in skf.split(X_real, y_real):
            xtrain, xtest = X_real.iloc[train_index], X_real.iloc[test_index]
            ytrain, ytest = y_real.iloc[train_index], y_real.iloc[test_index]
            mod = RandomForestRegressor()
            mod.fit(xtrain,ytrain)
            real_test_pred = mod.predict(xtest)
            rmse_real = rmse(real_test_pred, ytest)
            mape_real = mape(real_test_pred, ytest)
            rmse_real_lst.append(rmse_real)
            mape_real_lst.append(mape_real)

            
            synth_test_pred = mod.predict(X)
            rmse_synth = rmse(synth_test_pred, y)
            mape_synth = mape(synth_test_pred, y)
            rmse_synth_lst.append(rmse_synth)
            mape_synth_lst.append(mape_synth)

            return np.mean(rmse_synth_lst),np.mean(mape_synth_lst)

def plot_metrics(predictions, labels):
    
    if(len(np.unique(labels)) == 2):
        accuracy = accuracy_score(labels,predictions)
        f1_sco = f1_score(labels,predictions,pos_label=np.unique(labels)[0])
        return accuracy,f1_sco
    else:
        accuracy = accuracy_score(labels,predictions)
        f1_sco = f1_score(labels,predictions,average="micro")
        return accuracy,f1_sco


def mape(actual, pred): 
    actual, pred = np.array(actual), np.array(pred)
    return np.mean(np.abs((actual - pred) / actual)) * 100

def rmse(actual, predict): 
    return(np.sqrt(mean_squared_error(actual, predict)))