from collections import deque
import csv

MAZES = {
    "near_target": (["S...","....","...G"], (0,0)),
    "far_target": (["S....","###..","....G"], (0,0)),
    "unreachable": (["S#G","###","..."], (0,0))
}
DIRECTIONS = [(-1,0),(0,1),(1,0),(0,-1)]

def shortest_path(grid, start, goal):
    q=deque([(start,0)]); seen={start}
    while q:
        p,d=q.popleft()
        if p==goal: return d
        for dr,dc in DIRECTIONS:
            n=(p[0]+dr,p[1]+dc)
            if 0<=n[0]<len(grid) and 0<=n[1]<len(grid[0]) and grid[n[0]][n[1]]!="#" and n not in seen:
                seen.add(n); q.append((n,d+1))
    return None

def online_dfs(grid, start, goal):
    # The agent sees only adjacent cells; the full grid is used by this simulator
    # to provide the local sensor reading at the current cell.
    visited={start}; moves=0; revisits=0; found=False
    parent={start:None}; stack=[(start,0)]
    while stack:
        pos, idx=stack[-1]
        if pos==goal: found=True; break
        if idx==len(DIRECTIONS):
            stack.pop()
            if stack:
                moves+=1; revisits+=1
            continue
        stack[-1]=(pos,idx+1)
        dr,dc=DIRECTIONS[idx]; nxt=(pos[0]+dr,pos[1]+dc)
        if not (0<=nxt[0]<len(grid) and 0<=nxt[1]<len(grid[0])) or grid[nxt[0]][nxt[1]]=="#":
            continue
        if nxt not in visited:
            visited.add(nxt); parent[nxt]=pos; moves+=1; stack.append((nxt,0))
    optimal=shortest_path(grid,start,goal)
    return {"found":found,"moves":moves,"revisited_cells":revisits,
            "visited_cells":len(visited),"optimal_cost":optimal,
            "competitive_ratio":round(moves/optimal,3) if optimal else "undefined (unreachable)"}

def main():
    rows=[]
    for name,(grid,start) in MAZES.items():
        goal=next((r,c) for r,row in enumerate(grid) for c,x in enumerate(row) if x=="G")
        result=online_dfs(grid,start,goal)
        row={"maze":name,**result}; rows.append(row); print(row)
    with open("performance.csv","w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
if __name__=="__main__": main()
