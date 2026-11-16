import sys

#sys.stdin = open('in', 'r')
#sys.stdout = open('out', 'w')

def Out(x):
    sys.stdout.write(str(x) + '\n')

def In():
    return sys.stdin.readline().strip()

def main():
    s = str(input())
    Map = {}
    
    for word in s:
        if word not in Map:
            Map[word] = 1
        else:
            Map[word] += 1
    
    odd = 0
    for key, value in Map.items():
        if value&1 == 1:
            odd +=1
    
    if odd&1 or odd == 0:
        print("First")
    else:
        print("Second")


if __name__ == '__main__':
    main()
