# -*- coding: utf-8 -*-
import sqlite3
import numpy as np 
import matplotlib.pyplot as plt 
from sklearn import preprocessing,svm
from sklearn.svm import LinearSVC 
from sklearn.multiclass import OneVsOneClassifier 
from sklearn import model_selection

Xy=[]

#####入力データ｜記入例→[['騎手名','馬齢','性別'],['騎手名','馬齢','性別'],・・・・・・]
input_data = np.array([['横山和','3','牡']]) 


#データベースに接続
con = sqlite3.connect('database.sqlite3')
cur = con.cursor()

cur.execute('SELECT rank,jockey,age,fm FROM data')

for data in cur:
    Xy.append(data)


Xy = np.array(Xy)


#3着以内を1、それ以外を2とする
for i,d in enumerate(Xy[:,0]):
    if int(d)<=3:
        Xy[i,0]=1
    else:
        Xy[i,0]=0

label_encoder = [] 
Xy_encoded = np.empty(Xy.shape) 
for i,item in enumerate(Xy[0]): 
    if item.isdigit(): 
        Xy_encoded[:, i] = Xy[:, i]
    else: 
        encoder = preprocessing.LabelEncoder()
        Xy_encoded[:, i] = encoder.fit_transform(Xy[:, i])
        label_encoder.append(encoder) 

X = Xy_encoded[:,1:4].astype(int)
y = Xy_encoded[:,0].astype(int)

#print(X[0])
#X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2, random_state=5) 
classifier = svm.LinearSVC(max_iter=30000,random_state=0) 
classifier.fit(X, y)
#y_test_pred = classifier.predict(X_test) 
f1 = model_selection.cross_val_score(classifier, X, y, scoring='f1_weighted', cv=3) 
print("F1 score: " + str(round(100*f1.mean(), 2)) + "%")                       

input_data_encoded = np.zeros(input_data.shape) 
count = 0 
for i,item in enumerate(input_data[0]):
    if item.isdigit(): 
        input_data_encoded[:,i] = input_data[:,i] 
    else: 
        input_data_encoded[:,i] = label_encoder[count].transform(input_data[:,i]) 
        count += 1 

V=input_data_encoded.astype(int)

ppp=classifier.predict(V)
print(ppp)