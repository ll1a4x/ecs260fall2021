# File name: hlp.py
# =============================================================
# ECS 260 Project, Fall 2021
# Team 16, Project 9
# Author: Lynden Lin
# =============================================================
# Description: 
# This file has helper functions for the quantitative data analysis
# of the project.
#

import os
import json
import copy

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

import seaborn as sns
import statsmodels.api as sm

#
# Function: loadRawData
# -------------------------------------------------------------
# Input:  json data file directory path
# Output: data dictionary
#
def loadRawData(filePath):
    data = None
    with open(filePath) as f:
        data = json.load(f)
    return data

#
# Function: getDataAll
# -------------------------------------------------------------
# Input:  directory of folder that contains json data files
# Output: data dictionary
#
def getDataAll(dataPath):
    dataAll = {}
    dataJsonList = os.listdir(dataPath)
    counter = 0
    for file in dataJsonList:
        if file.find('json') == -1:
            continue
        dataNew = loadRawData(dataPath + file)
        dataUpdate = {}
        for project, value in dataNew.items():
            if dataNew[project] == None or "total_fork_count" not in value.keys():
                continue
            dataUpdate[project] = dataNew[project]
            dataAll.update(dataUpdate)
        counter += len(list(dataUpdate.keys()))
    print(counter)
    return dataAll

#
# Function: getFeatAndFork
# -------------------------------------------------------------
# Input:  projects feature list AND projects data dict
# Output: project-to-projectsFeature dict 
#         AND project-to-forksWithFeature dict
#
def getFeatAndFork(proFeat, dataAll):
    dataProFeat = {}     
    dataProFork = copy.deepcopy(dataAll) 
    for project, forks in dataAll.items():
        for feature in proFeat:
            if project not in dataProFeat.keys():
                dataProFeat[project] = {}
            if feature in forks.keys():
                dataProFeat[project][feature] = forks[feature]
                del dataProFork[project][feature]
    return dataProFeat, dataProFork

#
# Function: getAggForks
# -------------------------------------------------------------
# Input:  project-to-forksWithFeature dict AND projects feature list
# Output: project-to-featuresSumForks dict
#
def getAggForks(dataProFork, forkFeat):
    dataProForksFeat = {}
    for project, forks in dataProFork.items():
        if forks == {}:
            continue
        if project not in dataProForksFeat.keys():
            dataProForksFeat[project] = {}
        for fork, forkData in forks.items():
            if list(forkData.keys()) != forkFeat:
                continue
            for feat in forkFeat:
                # Remove incomplte data (missing some features)
                if feat not in dataProForksFeat[project].keys():
                    dataProForksFeat[project][feat] = 0
                else:
                    dataProForksFeat[project][feat] += forkData[feat]
    return dataProForksFeat

#
# Function: logreg_uniVar
# -------------------------------------------------------------
# Input:  feature, X_train, y_train, X_test, and y_test
# Output: print out precision/recall/accuracy, 
#         logit regression results, 
#         logit graph, 
#         and confusion matrix
#         
def logreg_uniVar(feat, X_train, y_train, X_test, y_test):
    
    # Logistic regression on the feature
    X_tr = X_train[feat].values.reshape(-1,1)
    y_tr = np.ravel(y_train.values.reshape(-1,1).astype(int))
    logreg_ = LogisticRegression()
    logreg_.fit(X_tr, y_tr)
    y_pr = logreg_.predict(X_test[feat].values.reshape(-1,1))

    #plt.scatter(X_graph, y_graph)
    plt.xlabel(feat)
    plt.ylabel("Probability of Graduated")
    y_pr_prob = logreg_.predict_proba(X_tr)[:,1]
    plt.scatter(X_tr, y_pr_prob)

    # Confusion metrics and its results
    y_ts = np.ravel(y_test.astype(int))
    cnf_matrix = metrics.confusion_matrix(y_ts, y_pr)
    # Precision = TP / (TP + FP)
    print("Precision:",metrics.precision_score(y_ts, y_pr))
    # Recall = TP / (TP + FN)
    print("Recall:",metrics.recall_score(y_ts, y_pr) )
    # Accuracy = (TP + TN) / (TP + TN + FP + FN)
    print("Accuracy:",metrics.accuracy_score(y_ts, y_pr))

    # Graph of confusion matrix
    class_names=[0, 1] # name  of classes
    fig, ax = plt.subplots()
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names)
    plt.yticks(tick_marks, class_names)
    # create heatmap
    sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="RdGy" ,fmt='g')
    ax.xaxis.set_label_position("top")
    plt.tight_layout()
    plt.title('Confusion matrix', y=1.1)
    plt.ylabel('Actual label')
    plt.xlabel('Predicted label')
    
    # Logit Regression Results
    logit_model_ = sm.Logit(y_tr,X_tr)
    print(logit_model_.fit().summary())