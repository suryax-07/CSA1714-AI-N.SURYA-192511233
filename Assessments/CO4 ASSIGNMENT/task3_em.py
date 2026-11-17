import numpy as np
import matplotlib.pyplot as plt

def normal(x, mu, var):
    return np.exp(-0.5*(x-mu)**2/var)/np.sqrt(2*np.pi*var)

def em(data, faulty=False, seed=0, iterations=30):
    rng=np.random.default_rng(seed)
    n=len(data); k=2
    weights=np.array([.5,.5]); means=np.array([-1.0,1.0]); variances=np.array([1.0,1.0])
    history=[]
    for _ in range(iterations):
        weighted=np.array([weights[j]*normal(data,means[j],variances[j]) for j in range(k)]).T
        if faulty:
            resp=weighted.copy()                 # DEFECT: not normalized per data point
        else:
            denom=weighted.sum(axis=1,keepdims=True)
            resp=weighted/np.maximum(denom,1e-300)
        Nk=resp.sum(axis=0)
        means=(resp*data[:,None]).sum(axis=0)/np.maximum(Nk,1e-12)
        variances=(resp*(data[:,None]-means)**2).sum(axis=0)/np.maximum(Nk,1e-12)
        variances=np.maximum(variances,1e-6)
        weights=Nk/n
        if not faulty:
            weights=weights/weights.sum()
        ll=np.sum(np.log(np.maximum(
            sum(weights[j]*normal(data,means[j],variances[j]) for j in range(k)),1e-300)))
        history.append((ll,weights.sum()))
    return np.array(history),weights,means,variances

rng=np.random.default_rng(11)
x=np.r_[rng.normal(-2,.45,100),rng.normal(2,.55,100)]
bad,wb,mb,vb=em(x,True)
good,wg,mg,vg=em(x,False)
print("TASK 3 - GAUSSIAN MIXTURE EM")
print("Faulty final sum of weights :",round(wb.sum(),4))
print("Repaired final sum weights  :",round(wg.sum(),4))
print("Faulty final log likelihood :",round(bad[-1,0],3))
print("Repaired final log likelihood:",round(good[-1,0],3))
print("Repaired likelihood decreases:",bool(np.any(np.diff(good[:,0]) < -1e-7)))
print("Repaired means:",np.round(mg,3))
plt.plot(bad[:,0],label="Faulty")
plt.plot(good[:,0],label="Repaired")
plt.xlabel("Iteration"); plt.ylabel("Log-likelihood"); plt.legend()
plt.tight_layout(); plt.savefig("task3_em_likelihood.png",dpi=140)
