import sys,functools,collections,bisect,math,heapq
input = sys.stdin.readline
#print = sys.stdout.write

mirror = {0:0,1:1,2:5,5:2,8:8}

@functools.lru_cache(None)
def fun(i):
    ones = i%10
    i //= 10
    tens = i%10
    if ones in mirror:
        newten = mirror[ones]
    else:
        return None
    if tens in mirror:
        newone = mirror[tens]
    else:
        return None
    return str(newten)+str(newone)

t = int(input())
for _ in range(t):
    h,m = map(int,input().strip().split())
    hour,minute = map(int,input().strip().split(':'))
    while True:
        #print(hour,minute)
        currhour = fun(minute)
        currminute = fun(hour)
        #print(currhour,currminute)
        if currhour and currminute and int(currhour) < h and int(currminute) < m:
            print(str(hour).zfill(2)+':'+str(minute).zfill(2))
            break
        
        minute += 1
        if minute >= m:
            minute = 0
            hour += 1
            
        if hour >= h:
            hour = 0
            minute = 0