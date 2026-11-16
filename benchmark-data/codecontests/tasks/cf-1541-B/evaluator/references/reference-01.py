# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 21:55:30 2021

@author: sukbhatt
"""
for _ in " "*int(input()):
    n = int(input())
    result = 0
    arr = list(map(int, input().split()))
    for i in range(n):
            for j in range(arr[i]-i-2,n,arr[i]):
                if j>i and arr[j]*arr[i] == i+j+2:
                    result += 1
    print(result)
            
        
            
