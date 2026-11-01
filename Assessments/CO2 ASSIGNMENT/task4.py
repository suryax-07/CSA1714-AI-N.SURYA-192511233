import time, csv

def build_tree(depth, branching=3):
    # Deterministic terminal values make repeated experiments reproducible.
    def value_at(index):
        return ((index*17+11)%101)-50
    return [value_at(i) for i in range(branching**depth)]

def minimax(depth, branching=3):
    leaves=build_tree(depth,branching); calls=0; nodes=0
    def rec(level,index):
        nonlocal calls,nodes
        nodes+=1
        if level==depth:
            calls+=1; return leaves[index]
        vals=[rec(level+1,index*branching+j) for j in range(branching)]
        return max(vals) if level%2==0 else min(vals)
    t=time.perf_counter(); score=rec(0,0); ms=(time.perf_counter()-t)*1000
    return score,nodes,calls,ms

def main():
    rows=[]
    for d in (2,3,4,5):
        score,nodes,calls,ms=minimax(d)
        theoretical=sum(3**i for i in range(d+1))
        row={"branching":3,"depth":d,"theoretical_nodes":theoretical,
             "actual_nodes":nodes,"evaluation_calls":calls,"best_score":score,"time_ms":round(ms,4)}
        rows.append(row);print(row)
    with open("performance.csv","w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
if __name__=="__main__":main()
