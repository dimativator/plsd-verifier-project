hist = [0]*1000005

def solve(n,s):
    cnt = 0 
    tot = 0 
    i = 0 
    while i < n:
        if s[i] == '0':
            tot += cnt 
        else:
            l = i 
            r = i  
            while r+1 < n and s[r+1] == '1':
                r+=1 
            #print(r)
            for x in range(r-l+1):
                cnt += (l+x+1)-hist[x]
                tot += cnt 
                hist[x] = r-x+1
            i = r 
        i+=1 
    return tot
    


n = int(input())
s = input()
print(solve(n,s))