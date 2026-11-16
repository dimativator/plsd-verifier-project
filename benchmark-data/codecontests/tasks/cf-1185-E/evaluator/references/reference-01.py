
def naiveSolve():
    
    
    
    return

from collections import defaultdict
def charToInt(c): #'a'->0
    if c=='.':
        return -1
    return ord(c)-ord('a')

def main():
    
    t=int(input())
    allans=[]
    for _ in range(t):
        n,m=readIntArr()
        grid=[] # convert all chars to int
        for __ in range(n):
            row=list(input())
            grid.append([charToInt(c) for c in row])
        
        start=[None]*26
        end=[None]*26
        for i in range(n):
            for j in range(m):
                if grid[i][j]!=-1:
                    if start[grid[i][j]]==None:
                        start[grid[i][j]]=[i,j]
                    end[grid[i][j]]=[i,j]
        while start and start[-1]==None:
            start.pop()
            end.pop()
        if len(start)==0:
            allans.append(['YES'])
            allans.append([0])
            continue
        
        ok=True
        N=len(start)
        dr,dc=end[N-1] # dummy row and cols for unused chars
        ans=[[dr,dc,dr,dc] for __ in range(N)]
        for i in range(N):
            if start[i]==None: # unused char
                continue
            if start[i][0]!=end[i][0] and start[i][1]!=end[i][1]:
                ok=False
                break
            ans[i]=[*start[i],*end[i]]
        
        if ok==False:
            allans.append(['NO'])
            continue
        
        reconstruct=[[-1 for _z in range(m)] for __ in range(n)]
        for i in range(N):
            r1,c1,r2,c2=ans[i]
            if r1==r2:
                for col in range(c1,c2+1):
                    reconstruct[r1][col]=i
            else:
                assert c1==c2
                for row in range(r1,r2+1):
                    reconstruct[row][c1]=i
        
        # check
        for i in range(n):
            for j in range(m):
                if grid[i][j]!=reconstruct[i][j]:
                    ok=False
        
        if ok==False:
            allans.append(['NO'])
            continue
        
        allans.append(['YES'])
        allans.append([N])
        for a in ans:
            for j in range(4):
                a[j]+=1 # 1-index
        allans.extend(ans)
        
    multiLineArrayOfArraysPrint(allans)
    
    return



import sys
# input=sys.stdin.buffer.readline #FOR READING PURE INTEGER INPUTS (space separation ok)
input=lambda: sys.stdin.readline().rstrip("\r\n") #FOR READING STRING/TEXT INPUTS.

def oneLineArrayPrint(arr):
    print(' '.join([str(x) for x in arr]))
def multiLineArrayPrint(arr):
    print('\n'.join([str(x) for x in arr]))
def multiLineArrayOfArraysPrint(arr):
    print('\n'.join([' '.join([str(x) for x in y]) for y in arr]))
 
def readIntArr():
    return [int(x) for x in input().split()]
# def readFloatArr():
#     return [float(x) for x in input().split()]
 
def makeArr(defaultValFactory,dimensionArr): # eg. makeArr(lambda:0,[n,m])
    dv=defaultValFactory;da=dimensionArr
    if len(da)==1:return [dv() for _ in range(da[0])]
    else:return [makeArr(dv,da[1:]) for _ in range(da[0])]
 
def queryInteractive(l,r):
    print('? {} {}'.format(l,r))
    sys.stdout.flush()
    return int(input())
 
def answerInteractive(x):
    print('! {}'.format(x))
    sys.stdout.flush()
 
inf=float('inf')
# MOD=10**9+7
MOD=998244353

from math import gcd,floor,ceil
# from math import floor,ceil # for Python2
 
for _abc in range(1):
    main()