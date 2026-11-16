import os
import sys
import math

def main():
    n,m = [int(i) for i in input().split()]
    centeri, centerj = -1,-1
    starti, startj = -1,-1
    for i in range(n):
        s = input()
        if not 'B' in s:
            continue
        if starti == -1:
            starti = i
            a = [int(pos) for pos,char in enumerate(s) if char=='B']
            centerj = min(a) + (max(a)-min(a))/2
            a = centerj - s.index('B')
            centeri = starti + a

    print('{} {}'.format(int(centeri+1), int(centerj+1)))



if __name__ == '__main__':
    main()
