import numpy as np

ACTIONS=["Off","Low","High"]
def environment(state,action,price):
    occupancy,temp=state
    cooling={"Off":0,"Low":1,"High":2}[action]
    next_temp=max(18,min(34,temp+ (1 if temp>=24 else 0)-cooling))
    comfort_violation=int(occupancy==1 and next_temp>25)
    energy={"Off":0.0,"Low":.5,"High":1.2}[action]
    reward=-(energy*price+5*comfort_violation)
    next_occupancy=1 if next_temp%2==0 else 0
    return (next_occupancy,next_temp),reward,energy,comfort_violation

states=[(o,t) for o in [0,1] for t in range(18,35)]
index={s:i for i,s in enumerate(states)}
def train(seed=0,episodes=300):
    rng=np.random.default_rng(seed); q=np.zeros((len(states),3))
    rewards=[]; energies=[]; violations=[]
    for ep in range(episodes):
        s=(0,24); total=energy_total=bad=0
        for step in range(24):
            eps=max(.05,.3*(1-ep/episodes))
            if rng.random()<eps: a=rng.integers(3)
            else: a=int(np.argmax(q[index[s]]))
            price=[.7,1.0,1.4][step%3]
            ns,r,e,v=environment(s,ACTIONS[a],price)
            future=max(q[index[ns]])
            q[index[s],a]+=0.15*(r+0.9*future-q[index[s],a])
            s=ns; total+=r; energy_total+=e; bad+=v
        rewards.append(total); energies.append(energy_total); violations.append(bad)
    return q,np.mean(rewards[-30:]),np.mean(energies[-30:]),np.mean(violations[-30:])

q,r,e,v=train()
print("TASK 6 - Q-LEARNING SMART AC")
print("Mean reward over last 30 episodes:",round(r,3))
print("Mean energy units over last 30 episodes:",round(e,3))
print("Mean comfort violations:",round(v,3))
print("Learned action in state (occupied, 29C):",ACTIONS[int(np.argmax(q[index[(1,29)]]))])
print("Baseline: fixed Low action; energy per step 0.5 units.")
print("Toy update: Q(s,a) <- Q(s,a) + 0.15[r + 0.9 max Q(s',a') - Q(s,a)].")
