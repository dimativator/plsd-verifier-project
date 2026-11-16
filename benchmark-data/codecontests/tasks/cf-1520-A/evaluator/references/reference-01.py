def solve(task):
    unique = set(task)
    segments = 0
    prev = ' '
    for letter in task:
        if letter != prev:
            segments+=1
        prev = letter
    return "YES" if len(unique) == segments else "NO"
if __name__ == '__main__':
    T = int(input().strip())
    
    for _ in range(T):
        days = int(input().strip())
        tasks = input().strip()
        print(solve(tasks))