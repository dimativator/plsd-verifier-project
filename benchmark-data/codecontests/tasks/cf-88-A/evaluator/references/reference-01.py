# Problem: 88A
# Time Created: August 10(Monday) 2020 || 11:37:58

#>-------------------------<#
import sys

input = sys.stdin.readline
#>-------------------------<#
from itertools import permutations


# Helper Functions. -> Don't cluster your code.
def check_chord(tup):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'B', 'H']
    notes += notes 
    x, y, z = tup

    x_y = 0
    y_z = 0


    for i in range(notes.index(x), len(notes)):
        if notes[i] == y: break
        else: x_y += 1
    for i in range(notes.index(y), len(notes)):
        if notes[i] == z: break
        else: y_z += 1


    if x_y == 4 and y_z == 3: return "major"
    elif x_y == 3 and y_z == 4: return "minor"
    else: return "strange"


# IO Functions. -> Input output
def io():
    x, y, z = map(str, input().split())
    perms = permutations([x,y,z])
    return list(perms)


# Main functions. -> Write the main solution here
def solve():
    perms = io()

    ans = 'strange'

    for perm in perms:
        chord = check_chord(perm)
        if chord != 'strange':
            ans = chord
            break
    print(ans)



# Multiple test cases. -> When you have T test cases.
solve()

