# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 14:16:45 2020

@author: Anes
"""

import pandas as pd


dataset = pd.read_excel("AirQualityUCI.xlsx")


"""
Based On : https://www.breeze-technologies.de/ Use Case
    
Our air quality index is calculated based on averages of all pollutant concentrations 
measured in a full hour, a full 8 hours, or a full day. To calculate an hourly air 
quality index, we average at least 90 measured data points of pollution
Concentration from a full hour (e.g. between 09:00 AM and 10:00 AM)

"""

dataset = dataset.groupby("Date").mean()


"""
to keep :
    
['CO(GT)','C6H6(GT)',"Nonmethane Hydrocarbon"]
"""

"""
to delete : 

['PT08.S1(CO)','PT08.S3(NOx)','PT08.S4(NO2)','PT08.S2(NMHC)','RH']
"""

dataset = dataset.drop(columns=['PT08.S1(CO)','PT08.S3(NOx)','PT08.S4(NO2)','PT08.S2(NMHC)','RH'])

dataset["AirQuality"] = (dataset['CO(GT)'] + dataset['C6H6(GT)'] + dataset["NMHC(GT)"]) / 3

dataset = dataset.drop(columns=['CO(GT)','C6H6(GT)',"NMHC(GT)"])

#Modèle Prévision : Sans utiliser aucun capteur le Jour J en se basant sur les 7 jours précédents.
period = 14
for i in range(1,period+1):
    dataset["AirQuality -"+str(i)] = dataset["AirQuality"].shift(periods=i)

for i in dataset.columns:
    if "AirQuality" not in i:
        dataset = dataset.drop(columns=i)

dataset = dataset.dropna()

del(i,period)

corr = dataset.corr()

columns = dataset.columns[1:].tolist()
columns.append("AirQuality")
dataset = dataset[columns]

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV


X_train, X_test, y_train, y_test = train_test_split(
    dataset.iloc[:,:-1], dataset.iloc[:,-1], test_size=0.20, random_state=0)

#GridSearchCV on RandomForestRegrossor

parameters = {'n_estimators': [120,140,160],
               'max_features': ['auto'],
               'max_depth': [5,6,7],
               'min_samples_split': [10,12,14],
               'min_samples_leaf': [4,6,8],
               'bootstrap': [True, False]}

rf = RandomForestRegressor(random_state=0)

reg = GridSearchCV(estimator = rf, param_grid = parameters, 
                          cv = 5,n_jobs=-1)


reg.fit(X_train, y_train)


#score on train
reg.score(X_train, y_train)

#score on test
reg.score(X_test, y_test)

#94% on train, 40% on test


rf = RandomForestRegressor(random_state=0,max_depth=5,min_samples_leaf=8,
                           min_samples_split=10)

rf.fit(X_train,y_train)

#score on train
rf.score(X_train, y_train)

#score on test
rf.score(X_test, y_test)

#94% on train, 40% on test


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor


for i in dataset.columns:
    if "AirQuality" not in i:
        dataset = dataset.drop(columns=i)

jours = []
train_score = []
test_score = []
period = 15
for i in range(1,period+1):
    dataset["AirQuality -"+str(i)] = dataset["AirQuality"].shift(periods=i)
    dataset = dataset.dropna()
    X_train, X_test, y_train, y_test = train_test_split(
        dataset.iloc[:,1:], dataset.iloc[:,0], test_size=0.20, random_state=0)
    rf = RandomForestRegressor(random_state=0,max_depth=5,min_samples_leaf=8,
                           min_samples_split=10)
    rf.fit(X_train,y_train)
    jours.append(i)
    train_score.append(rf.score(X_train, y_train))
    test_score.append(rf.score(X_test, y_test))
    

import matplotlib.pyplot as plt

plt.figure()
plt.plot(jours,train_score,label="Accuracy on training set")
plt.plot(jours,test_score,label="Accuracy on test set")
plt.title("Courbe d'apprentissage")
plt.xlabel("Jours")
plt.ylabel("Précision")
plt.legend()
plt.show()



dataset = dataset.dropna()





