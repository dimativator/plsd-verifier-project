# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 09:55:17 2020

@author: Mridul Garg
"""
#def swap()


n = int(input())
arr = list(map(int, input().split(' ')))

check = [i for i in range(1, n+1)]

last0 = 0
for i in range(n):
    
    if arr[i] != 0:
        check[arr[i]-1] = 0
    else:
        last0 = i+1
        
remain = []
for i in check:
    if i != 0:
        remain.append(i)
        
remain.sort(reverse = True)

#print(remain)
#print(last0)

#print(check)
j = -1
if remain[-1] == last0:
    
    remain[j], remain[j-1] = remain[j-1], remain[j]
#print(remain)
#print(arr)
j = 0
for i in range(n):
    if arr[i] == 0:
        
        if i+1 == remain[j]:
            remain[j], remain[j+1] = remain[j+1], remain[j]
        arr[i] = remain[j]
        j += 1
        
for i in arr:
    print(i, end = " ")
print()    
