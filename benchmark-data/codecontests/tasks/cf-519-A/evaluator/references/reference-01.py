# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 10:34:19 2018

@author: Quaint Sun
"""

line=[]
t=0
while t<8:
    line=line+list(input())
    t=t+1
    
white=line.count('Q')*9+line.count('R')*5+line.count('B')*3+line.count('N')*3+line.count('P')
black=line.count('q')*9+line.count('r')*5+line.count('b')*3+line.count('n')*3+line.count('p')

if white>black:
    print('White')
elif white<black:
    print('Black')
else:
    print('Draw')







