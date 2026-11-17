import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

def sigmoid(z): return 1/(1+np.exp(-np.clip(z,-40,40)))
def forward(x,W1,b1,W2,b2):
    a1=sigmoid(x@W1+b1); a2=sigmoid(a1@W2+b2)
    return a1,a2
def loss(x,y,W1,b1,W2,b2):
    _,p=forward(x,W1,b1,W2,b2)
    return .5*np.sum((p-y)**2)
def gradients(x,y,W1,b1,W2,b2):
    a1,a2=forward(x,W1,b1,W2,b2)
    d2=(a2-y)*a2*(1-a2)
    d1=(d2@W2.T)*a1*(1-a1)
    return a1.T@d2, d2.sum(axis=0), x.T@d1, d1.sum(axis=0)
def numeric_grad(x,y,W1,b1,W2,b2):
    eps=1e-5; g=np.zeros_like(W1)
    for i in range(W1.shape[0]):
        for j in range(W1.shape[1]):
            plus=W1.copy(); minus=W1.copy()
            plus[i,j]+=eps; minus[i,j]-=eps
            g[i,j]=(loss(x,y,plus,b1,W2,b2)-loss(x,y,minus,b1,W2,b2))/(2*eps)
    return g

x=np.array([[1.,0.]])
y=np.array([[1.]])
W1=np.array([[.5,-.4],[.3,.8]])
b1=np.zeros(2); W2=np.array([[.6],[-.2]]); b2=np.zeros(1)
a1,a2=forward(x,W1,b1,W2,b2)
gW2,gb2,gW1,gb1=gradients(x,y,W1,b1,W2,b2)
ng=numeric_grad(x,y,W1,b1,W2,b2)
print("TASK 4 - NEURAL NETWORK")
print("Hidden activation:",np.round(a1,4))
print("Output:",np.round(a2,4),"Loss:",round(loss(x,y,W1,b1,W2,b2),6))
print("Maximum gradient difference:",round(np.max(np.abs(gW1-ng)),8))
lr=.5
W1n=W1-lr*gW1; W2n=W2-lr*gW2
print("Updated W1:\n",np.round(W1n,4))
print("Updated W2:\n",np.round(W2n,4))
# XOR: one hidden layer network
X=np.array([[0,0],[0,1],[1,0],[1,1]],dtype=float)
Y=np.array([0,1,1,0])
net=MLPClassifier(hidden_layer_sizes=(8,),activation="tanh",solver="lbfgs",random_state=3,max_iter=3000)
net.fit(X,Y)
print("Neural network XOR predictions:",net.predict(X).tolist())
