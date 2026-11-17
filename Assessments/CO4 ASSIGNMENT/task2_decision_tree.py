import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def entropy(y):
    if len(y) == 0: return 0.0
    _, counts = np.unique(y, return_counts=True)
    p = counts / counts.sum()
    return float(-np.sum(p * np.log2(p)))

def best_split(X, y):
    parent = entropy(y)
    best_gain, best_feature, best_threshold = -1, None, None
    for j in range(X.shape[1]):
        for threshold in np.unique(X[:, j])[:-1]:
            left = X[:, j] <= threshold
            right = ~left
            if left.sum() == 0 or right.sum() == 0: continue
            child = (left.mean()*entropy(y[left]) + right.mean()*entropy(y[right]))
            gain = parent - child
            if gain > best_gain:
                best_gain, best_feature, best_threshold = gain, j, threshold
    return best_feature, best_threshold, best_gain

class SimpleTree:
    def __init__(self, max_depth=3): self.max_depth=max_depth
    def fit(self, X, y): self.root=self._build(X,y,0); return self
    def _build(self,X,y,depth):
        labels, counts=np.unique(y,return_counts=True)
        node={"class":labels[np.argmax(counts)]}
        if len(labels)==1 or depth>=self.max_depth or X.shape[1]==0: return node
        f,t,g=best_split(X,y)
        if f is None or g<=0: return node
        mask=X[:,f]<=t
        if mask.all() or (~mask).all(): return node
        node.update({"feature":f,"threshold":float(t),
                     "left":self._build(X[mask],y[mask],depth+1),
                     "right":self._build(X[~mask],y[~mask],depth+1)})
        return node
    def _one(self,x,node):
        if "feature" not in node: return node["class"]
        branch="left" if x[node["feature"]]<=node["threshold"] else "right"
        return self._one(x,node[branch])
    def predict(self,X): return np.array([self._one(x,self.root) for x in X])

X,y=load_iris(return_X_y=True)
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,random_state=7,stratify=y)
custom=SimpleTree(max_depth=3).fit(Xtr,ytr)
pred=custom.predict(Xte)
sk=DecisionTreeClassifier(criterion="entropy",max_depth=3,random_state=7).fit(Xtr,ytr)
skpred=sk.predict(Xte)
print("TASK 2 - DECISION TREE")
print("Custom tree accuracy :",round(accuracy_score(yte,pred),3))
print("sklearn accuracy     :",round(accuracy_score(yte,skpred),3))
print("Precision / Recall / F1 (macro):",
      round(precision_score(yte,pred,average="macro"),3),
      round(recall_score(yte,pred,average="macro"),3),
      round(f1_score(yte,pred,average="macro"),3))
print("Confusion matrix:\n",confusion_matrix(yte,pred))
print("Root split feature index, threshold, gain:",
      best_split(Xtr,ytr))
for depth in [None,2]:
    m=DecisionTreeClassifier(max_depth=depth,random_state=7).fit(Xtr,ytr)
    print("depth",m.get_depth(),"leaves",m.get_n_leaves(),
          "train",round(m.score(Xtr,ytr),3),"test",round(m.score(Xte,yte),3))
