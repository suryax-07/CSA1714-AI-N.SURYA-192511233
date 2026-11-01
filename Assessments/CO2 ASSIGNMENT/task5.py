import copy, csv
INSTANCES={
 "propagation_solves":({"A":["1"],"B":["1","2"],"C":["2","3"]},
                       {"A":["B"],"B":["A","C"],"C":["B"]}),
 "challenging_cycle":({"A":["1","2","3"],"B":["1","2","3"],"C":["1","2","3"],"D":["1","2","3"]},
                      {"A":["B","D"],"B":["A","C"],"C":["B","D"],"D":["A","C"]})
}
def revise(domains, graph, xi, xj, metrics):
    removed=[]
    for x in list(domains[xi]):
        metrics["checks"]+=1
        if not any(x!=y for y in domains[xj]):
            domains[xi].remove(x); removed.append(x)
    return bool(removed)
def ac3(domains,graph,metrics):
    queue=[(x,y) for x in graph for y in graph[x]]
    while queue:
        xi,xj=queue.pop(0)
        if revise(domains,graph,xi,xj,metrics):
            metrics["revisions"]+=1
            if not domains[xi]: metrics["wipeouts"]+=1; return False
            for xk in graph[xi]:
                if xk!=xj: queue.append((xk,xi))
    return True
def solve(domains,graph,propagate=True):
    metrics={"nodes":0,"backtracks":0,"checks":0,"wipeouts":0,"revisions":0}
    def backtrack(d):
        metrics["nodes"]+=1
        if all(len(v)==1 for v in d.values()): return {k:v[0] for k,v in d.items()}
        var=min((v for v in d if len(d[v])>1),key=lambda x:len(d[x]))
        for val in list(d[var]):
            nd=copy.deepcopy(d); nd[var]=[val]
            if propagate:
                if not ac3(nd,graph,metrics): metrics["backtracks"]+=1; continue
            else:
                # Check assigned neighbours only.
                ok=True
                for nb in graph[var]:
                    metrics["checks"]+=1
                    if len(nd[nb])==1 and nd[nb][0]==val: ok=False
                if not ok: metrics["backtracks"]+=1; continue
            ans=backtrack(nd)
            if ans is not None:return ans
        metrics["backtracks"]+=1
        return None
    if propagate and not ac3(domains,graph,metrics): return None,metrics
    return backtrack(copy.deepcopy(domains)),metrics


def main():
    rows=[]
    for name,(domains,graph) in INSTANCES.items():
        for use in (False,True):
            solution,m=solve(copy.deepcopy(domains),graph,use)
            row={"instance":name,"propagation":use,"solution":solution,
                 **m};rows.append(row);print(row)
    with open("performance.csv","w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
if __name__=="__main__":main()
