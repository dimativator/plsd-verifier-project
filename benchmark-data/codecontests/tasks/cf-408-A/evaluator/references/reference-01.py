num_cashiers = int(input())
queue_sizes = list(map(lambda x: int(x) * 15, input().split()))

items = []

for i in range(num_cashiers):
    items_list = sum(map(lambda x: int(x) * 5, input().split()))
    items.append(items_list)

min_time = min(change + groceries for change, groceries in zip(queue_sizes, items))
print(min_time)
