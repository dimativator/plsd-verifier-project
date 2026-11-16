I = lambda: int(input())
IL = lambda: list(map(int, input().split()))

L = [input()[0] for i in '123']
gt = {'r': 'rp', 'p': 'ps', 's': 'sr'}

print('F' if L[1] not in gt[L[0]] and L[2] not in gt[L[0]] else
      'M' if L[0] not in gt[L[1]] and L[2] not in gt[L[1]] else
      'S' if L[0] not in gt[L[2]] and L[1] not in gt[L[2]] else
      '?')