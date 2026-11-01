import random, csv

def minimax(values):
    visited=0
    def rec(level,index):
        nonlocal visited
        visited+=1
        if level==3: return values[index]
        a=rec(level+1,index*2); b=rec(level+1,index*2+1)
        return max(a,b) if level%2==0 else min(a,b)
    return rec(0,0),visited

def alphabeta(values):
    visited=cutoffs=0
    def rec(level,index,alpha,beta):
        nonlocal visited,cutoffs
        visited+=1
        if level==3: return values[index]
        if level%2==0:
            value=float("-inf")
            for child in (index*2,index*2+1):
                value=max(value,rec(level+1,child,alpha,beta)); alpha=max(alpha,value)
                if alpha>=beta: cutoffs+=1; break
            return value
        value=float("inf")
        for child in (index*2,index*2+1):
            value=min(value,rec(level+1,child,alpha,beta)); beta=min(beta,value)
            if beta<=alpha: cutoffs+=1; break
        return value
    value=rec(0,0,float("-inf"),float("inf"))
    return value,visited,cutoffs

def main():
    # Four leaves per MIN subtree are arranged to help or hinder early cutoffs.
    cases={
      "good_order":[8,9,8,8,1,2,7,8],
      "poor_order":[1,2,0,1,8,9,7,8],
      "equal_values":[5,5,5,5,5,5,5,5]
    }
    rows=[]
    for name,leaves in cases.items():
        mm,nm=minimax(leaves); ab,na,cut=alphabeta(leaves)
        row={"tree":name,"minimax_value":mm,"minimax_nodes":nm,
             "alphabeta_value":ab,"alphabeta_nodes":na,"cutoffs":cut}
        rows.append(row); print(row)
    with open("performance.csv","w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
if __name__=="__main__":main()
