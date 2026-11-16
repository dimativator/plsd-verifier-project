from sys import stdin, stdout


def siftup(ind):
    while ind != 1 and heap[ind] < heap[ind // 2]:
        heap[ind], heap[ind // 2] = heap[ind // 2], heap[ind]
        ind //= 2    
        
        
def siftdown(ind):
    while len(heap) > ind * 2 + 1 and (heap[ind] > heap[ind * 2] or heap[ind] > heap[ind * 2 + 1]):
        if heap[ind * 2 + 1] < heap[ind * 2]:
            heap[ind], heap[ind * 2 + 1] = heap[ind * 2 + 1], heap[ind]
            ind = ind * 2 + 1
        else:
            heap[ind], heap[ind * 2] = heap[ind * 2], heap[ind]
            ind = ind * 2
    if len(heap) > ind * 2 and heap[ind] > heap[ind * 2]:
        heap[ind], heap[ind * 2] = heap[ind * 2], heap[ind]
        ind *= 2


n = int(stdin.readline())
heap = [0]
steps = []
for i in range(n):
    s = stdin.readline().rstrip().split()
    if s.count('insert'):
        heap.append(int(s[-1]))
        siftup(len(heap) - 1)
        steps.append(' '.join(s))
    elif s.count('getMin'):
        while len(heap) != 1 and heap[1] < int(s[-1]):
            steps.append('removeMin')
            if len(heap) == 2:
                heap.pop()
            else:
                heap[1] = heap[-1]
                heap.pop()
                siftdown(1)
        if len(heap) > 1 and heap[1] != int(s[-1]):
            steps.append(' '.join(['insert'] + [s[-1]]))
            heap.append(int(s[-1]))
            siftup(len(heap) - 1)
        elif len(heap) == 1:
            steps.append(' '.join(['insert'] + [s[-1]]))
            heap.append(int(s[-1]))
        steps.append(' '.join(s))
    else:
        if len(heap) > 1:
            steps.append(' '.join(s))
            if len(heap) > 2:
                heap[1] = heap[-1]
                heap.pop()
                siftdown(1)
            else:
                heap.pop()
        else:
            steps.append(' '.join(['insert', '1']))
            steps.append('removeMin')

stdout.write(str(len(steps)) + '\n' + '\n'.join(steps))#!