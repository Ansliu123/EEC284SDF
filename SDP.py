from math import gcd
from fractions import Fraction

#This algorithm is based on the paper "JOINT MINIMIZATION OF CODE AND DATA FOR SYNCHRONOUS DATAFLOW PROGRAMS" by Murthy et al.
# Use the Periodic static schedule to calculate the GCD of production and consuption rates for each chain to be used to calculating the cost of splitting schedules

ACTORS = ['A', 'B', 'C', 'D', 'E']
EDGES  = [(3,4), (5,3), (6,5), (2,3)]  # (produced, consumed)
#Edge A->B, Edge B->C, Edge C->D, Edge D-> E

PSS = [4, 3, 5, 6, 4]  #Periodic Static Schedule from part a)
n = len(ACTORS)

# GCD table
GCD = [[0 for _ in range(n)] for _ in range(n)]
for i in range(n):
    GCD[i][i] = PSS[i]
    for j in range(i+1, n):
        GCD[i][j] = gcd(GCD[i][j-1], PSS[j])

# DP tables
INF  = float('inf')
cost = [[0 for _ in range(n)] for _ in range(n)]   # cost[i][j] = min buffer for subchain [i..j]
split = [[-1 for _ in range(n)] for _ in range(n)]  # best split offset

for size in range(2, n+1):
    for Right in range(size-1, n):
        Left = Right - size + 1
        cost[Left][Right] = INF
        for k in range(0, size-1):                        # try each split offset
            a = Left + k                                  # split after actor a
            c = (PSS[a] * EDGES[a][0]) // GCD[Left][Right]       # eq. (4): c[l,r][a]
            t = c + cost[Left][a] + cost[a+1][Right]
            if t < cost[Left][Right]:
                cost[Left][Right], split[Left][Right] = t, k

# Reconstruct scheduling
def ConvertSplit(Left, Right):
    if Left == Right: 
        return ACTORS[Left] 
    else:
        a  = Left + split[Left][Right]
        iL = GCD[Left][a]   // GCD[Left][Right]
        iR = GCD[a+1][Right] // GCD[Left][Right]

        L_string  = f"({iL}*{ConvertSplit(Left,a)})"   if iL > 1 else f"({ConvertSplit(Left,a)})"
        R_string  = f"({iR}*{ConvertSplit(a+1,Right)})" if iR > 1 else f"({ConvertSplit(a+1,Right)})"
        return L_string + R_string

print("PSS =", dict(zip(ACTORS, PSS)))
print(f"Min buffer = {cost[0][n-1]}")
print(f"Schedule   = ({ConvertSplit(0, n-1)})")  