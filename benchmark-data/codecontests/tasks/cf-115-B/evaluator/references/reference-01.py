n, m = [int(i) for i in input().split()]

if n == 1 and m == 1:  # nothing to mow
    print(0)
elif n == 1: # 1 row --> move right until last weed
    lawn = input()
    print(lawn.rfind('W'))
elif m == 1: # 1 column --> move down until last weed
    weeds = 0
    for i in range(n):
        lawn = input()
        if lawn == 'W':
            weeds = i
    print(weeds)
else:  # generic solution for n-by-m lawn
    # Get lawn as a list of strings, where each string is a row
    lawn = []
    for i in range(n):
        lawn.append(input())
    
    # Determine the first and last weed in each row
    first_weed = [row.find('W') for row in lawn]
    last_weed = [row.rfind('W') for row in lawn]
    
    if all([i == -1 for i in first_weed]):  # there are not weeds!
        print(0)
    else:  # there must be some weeds to mow
        # Determine the last row that needs to be mowed
        last_row = max(i for i, v in enumerate(first_weed) if v >= 0)
        lawn = lawn[:last_row+1]
        first_weed = first_weed[:last_row+1]
        last_weed = last_weed[:last_row+1]
        n = len(lawn)
        
        # Add down movement
        moves = n-1
        
        # Add left/right movement
        even = True
        col = 0
        for i in range(n):
            if first_weed[i] != -1:
                if even:
                    moves += abs(first_weed[i] - col)
                    col = last_weed[i]
                else:
                    moves += abs(last_weed[i] - col)
                    col = first_weed[i]
                moves += last_weed[i] - first_weed[i]
            even = not even
        print(moves)