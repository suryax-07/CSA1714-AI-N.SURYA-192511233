import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

model = DecisionTreeClassifier(random_state=42)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(model, X_train, y_train, cv=cv)
model.fit(X_train, y_train)

train_acc = accuracy_score(y_train, model.predict(X_train))
test_pred = model.predict(X_test)
test_acc = accuracy_score(y_test, test_pred)

baseline = DummyClassifier(strategy="most_frequent")
baseline.fit(X_train, y_train)
base_acc = accuracy_score(y_test, baseline.predict(X_test))

print("TASK 1 - TRAIN/TEST PROTOCOL")
print(f"Training accuracy       : {train_acc:.3f}")
print(f"5-fold CV mean accuracy : {cv_scores.mean():.3f}")
print(f"Held-out test accuracy  : {test_acc:.3f}")
print(f"Majority baseline       : {base_acc:.3f}")
print(f"Train - test gap        : {train_acc-test_acc:.3f}")
print(f"Test precision/recall/F1: {precision_score(y_test,test_pred):.3f} / {recall_score(y_test,test_pred):.3f} / {f1_score(y_test,test_pred):.3f}")
