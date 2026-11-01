import math, itertools, csv, time
def dist(a,b):return math.hypot(a[0]-b[0],a[1]-b[1])
def exhaustive(points):
    best=float("inf");besttour=None;nodes=0
    for p in itertools.permutations(range(1,len(points))):
        tour=(0,)+p;cost=sum(dist(points[tour[i]],points[tour[(i+1)%len(tour)]]) for i in range(len(tour)))
        nodes+=1
        if cost<best:best,besttour=cost,tour
    return best,besttour,nodes
def mst_cost(vertices,points):
    if len(vertices)<2:return 0
    remaining=set(vertices); used={remaining.pop()}; total=0
    while remaining:
        edge=min((dist(points[a],points[b]),a,b) for a in used for b in remaining)
        total+=edge[0];used.add(edge[2]);remaining.remove(edge[2])
    return total
def branch_bound(points):
    n=len(points);best=float("inf");besttour=None;expanded=0;pruned=0
    # A nearest-neighbour tour supplies an initial upper bound.
    tour=[0];unused=set(range(1,n))
    while unused:
        nxt=min(unused,key=lambda x:dist(points[tour[-1]],points[x]));tour.append(nxt);unused.remove(nxt)
    best=sum(dist(points[tour[i]],points[tour[(i+1)%n]]) for i in range(n))
    besttour=tuple(tour)
    def dfs(path,unused,cost):
        nonlocal best,besttour,expanded,pruned
        expanded+=1
        if not unused:
            total=cost+dist(points[path[-1]],points[0])
            if total<best:best,besttour=total,tuple(path)
            return
        # Admissible lower bound: current path + MST of remaining nodes
        # + cheapest connection from current endpoint + cheapest return edge.
        mst=mst_cost(unused,points)
        connect=min(dist(points[path[-1]],points[x]) for x in unused)
        return_edge=min(dist(points[x],points[0]) for x in unused)
        if cost+mst+connect+return_edge>=best:
            pruned+=1;return
        for nxt in sorted(unused):
            dfs(path+[nxt],unused-{nxt},cost+dist(points[path[-1]],points[nxt]))
    dfs([0],set(range(1,n)),0)
    return best,besttour,expanded,pruned
def main():
    rows=[]
    for n in (7,8,9):
        pts=[(float((i*19+7)%37),float((i*i*13+3*i)%41)) for i in range(n)]
        ex,t1,n1=exhaustive(pts);bb,t2,n2,p=branch_bound(pts)
        row={"customers":n,"exhaustive_tours":n1,"branch_bound_nodes":n2,
             "pruned_nodes":p,"exhaustive_cost":round(ex,4),"redesign_cost":round(bb,4),
             "same_optimum":abs(ex-bb)<1e-8}
        rows.append(row);print(row)
    with open("performance.csv","w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
if __name__=="__main__":main()
