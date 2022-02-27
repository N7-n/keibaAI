# -*- coding: utf-8 -*-
import sqlite3
import numpy as np 
import matplotlib.pyplot as plt 
from sklearn import preprocessing 
from sklearn.svm import LinearSVC 
from sklearn.multiclass import OneVsOneClassifier 
from sklearn import model_selection

Xy=[]

#データベースに接続
con = sqlite3.connect('database.sqlite3')
cur = con.cursor()

cur.execute('SELECT * FROM data')

for data in cur:
    Xy.append(data)


Xy = np.array(Xy)

label_encoder = [] 
Xy_encoded = np.empty(Xy.shape) 
for i,item in enumerate(Xy[0]): 
    if item.isdigit(): 
        Xy_encoded[:, i] = Xy[:, i]
    else: 
        encoder = preprocessing.LabelEncoder()
        Xy_encoded[:, i] = encoder.fit_transform(Xy[:, i])
        label_encoder.append(encoder) 

X = Xy_encoded[:,:0].astype(int)
y = Xy_encoded[:,0].astype(int)

#3着以内を1、それ以外を2とする
for i,d in enumerate(y):
    if d<=3:
        y[i]=1
    else:
        y[i]=2

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2, random_state=5) 

classifier = LinearSVC(max_iter=20,random_state=0) 
classifier.fit(X_train, y_train) 