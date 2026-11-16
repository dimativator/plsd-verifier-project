#!/usr/bin/python

import sys
from sys import stdin
    
def solve(N, K, S):
    if N % K != 0:
        print(-1)
        return
    cnt_dict = {}
    for s in S:
        cnt_dict[s] = 0
    for s in S:
        cnt_dict[s] += 1
    bea = True
    for k in cnt_dict:
        if cnt_dict[k] % K != 0:
            bea = False
    if bea:
        print(S)
        return
    #string wasnt beautiful but can be made one
    pref = S[:]
    to_add_dict = {}
    for k in cnt_dict:
        to_add_dict[k] = (K - (cnt_dict[k] % K)) % K
    for i in range(1,N+1):
        pref = pref[:-1]
        letter_cur = S[N-i]
        letter_next = chr(ord(letter_cur)+ 1)
        cnt_dict[letter_cur] -= 1
        to_add_dict[letter_cur] += 1
        to_add_dict[letter_cur] %= K
        #check if we can make string beautiful
        my_sum = sum(to_add_dict.values())
        if letter_cur != "z":
            if my_sum < i:
                diff = i - my_sum
                if letter_next in to_add_dict.keys():
                    if to_add_dict[letter_next] == 0:
                        to_add_dict[letter_next] = K
                        diff -= K
                    if 'a' in to_add_dict.keys():
                        to_add_dict['a'] += diff
                    else:
                        to_add_dict['a'] = diff
                    my_suffix = letter_next
                    to_add_dict[letter_next] -= 1
                    for my_key in sorted(to_add_dict):
                        my_suffix += my_key * to_add_dict[my_key]
                else:
                    to_add_dict[letter_next] = K
                    diff -= K
                    if 'a' in to_add_dict.keys():
                        to_add_dict['a'] += diff
                    else:
                        to_add_dict['a'] = diff
                    my_suffix = letter_next
                    to_add_dict[letter_next] -= 1
                    for my_key in sorted(to_add_dict):
                        my_suffix += my_key * to_add_dict[my_key]
                print(pref + my_suffix)
                return
            elif my_sum == i:
                good = False
                for my_key in sorted(to_add_dict):
                    if my_key > letter_cur and to_add_dict[my_key] > 0:
                        my_suffix = my_key
                        to_add_dict[my_key] -= 1
                        good = True
                        break
                if good:
                    for my_key in sorted(to_add_dict):
                        my_suffix += my_key * to_add_dict[my_key]
                    print(pref + my_suffix)
                    return
    return
     
    
    
def run():
    out = ""    
    T = int(input())
    for i in range(T):
        N, K = [int(x) for x in stdin.readline().split()]
        S = stdin.readline().strip()
        solve(N, K, S)

run()

