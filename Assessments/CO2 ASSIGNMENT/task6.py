import itertools, math, random, time, csv

def distance(a,b): return math.hypot(a[0]-b[0],a[1]-b[1])
def tour_cost(tour,points):
    return sum(distance(points[tour[i]],points[tour[(i+1)%len(tour)]]) for i in range(len(tour)))

def exhaustive(points):
    n=len(points); best=float("inf"); best_tour=None; candidates=0
    for perm in itertools.permutations(range(1,n)):
        tour=(0,)+perm; cost=tour_cost(tour,points);candidates+=1
        if cost<best:best,best_tour=cost,tour
    return best,best_tour,candidates

def two_opt(points,seed):
    rng=random.Random(seed); n=len(points); tour=list(range(n));rng.shuffle(tour)
    if tour[0]!=0:
        k=tour.index(0);tour[0],tour[k]=tour[k],tour[0]
    improved=True;checks=0
    while improved:
        improved=False
        for i in range(1,n-1):
            for j in range(i+1,n):
                checks+=1
                candidate=tour[:i]+tour[i:j+1][::-1]+tour[j+1:]
                if tour_cost(candidate,points)+1e-9<tour_cost(tour,points):
                    tour=candidate;improved=True
    return tour_cost(tour,points),checks

def main():
    rows=[]
    for n in (5,7,8,9):
        points=[(float((i*19+7)%37),float((i*i*13+3*i)%41)) for i in range(n)]
        t=time.perf_counter();opt,tour,candidates=exhaustive(points);exact_ms=(time.perf_counter()-t)*1000
        local=[];checks=[]
        for seed in range(20):
            t=time.perf_counter();cost,c=two_opt(points,seed);local.append((cost,(time.perf_counter()-t)*1000));checks.append(c)
        avg=sum(x[0] for x in local)/20
        row={"customers":n,"candidate_tours":candidates,"optimum":round(opt,4),
             "local_avg":round(avg,4),"gap_percent":round((avg-opt)/opt*100,2),
             "local_best":round(min(x[0] for x in local),4),
             "local_worst":round(max(x[0] for x in local),4),
             "avg_local_ms":round(sum(x[1] for x in local)/20,4),
             "exact_ms":round(exact_ms,4),"avg_2opt_checks":round(sum(checks)/20,1)}
        rows.append(row);print(row)
    with open("performance.csv","w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
if __name__=="__main__":main()
