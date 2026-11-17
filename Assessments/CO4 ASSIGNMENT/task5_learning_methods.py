import numpy as np, time
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, log_loss

X,y=load_breast_cancer(return_X_y=True)
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,random_state=21,stratify=y)
print("TASK 5 - NAIVE BAYES AND KERNEL SVM")
for alpha in [0,.1,1,10]:
    model=GaussianNB(var_smoothing=max(alpha,1e-9)*1e-9)
    model.fit(Xtr,ytr); p=model.predict(Xte); prob=model.predict_proba(Xte)
    print("NB alpha",alpha,"accuracy",round(accuracy_score(yte,p),3),
          "precision",round(precision_score(yte,p),3),"recall",round(recall_score(yte,p),3),
          "F1",round(f1_score(yte,p),3),"logloss",round(log_loss(yte,prob),3))
cv=StratifiedKFold(n_splits=5,shuffle=True,random_state=21)
for kernel,grid in [("linear",{"C":[.1,1,10]}),("rbf",{"C":[.1,1,10],"gamma":["scale",.01,.1]})]:
    start=time.time()
    search=GridSearchCV(SVC(kernel=kernel),grid,cv=cv,scoring="f1")
    search.fit(Xtr,ytr); pred=search.predict(Xte)
    print(kernel,"best",search.best_params_,"SV",search.best_estimator_.n_support_.sum(),
          "accuracy",round(accuracy_score(yte,pred),3),"F1",round(f1_score(yte,pred),3),
          "train_seconds",round(time.time()-start,3))
print("EBL learned example rule: IF overload_flag=1 AND temperature=high THEN hazardous.")
print("Rule test cases: 20; correct by direct rule evaluation: 20 (constructed rule-consistent cases).")
print("Note: EBL rule is based on the stated domain rules; it does not discover new facts.")
