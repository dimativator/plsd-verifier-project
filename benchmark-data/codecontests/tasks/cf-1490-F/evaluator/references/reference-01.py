def find():
    n = int(input())
    mas = tuple(map(int, input().split()))

    count_numbers = {}
    for j in mas:
        count_numbers[j] = count_numbers.get(j, 0) + 1

    count_set_numb = {}
    for j in count_numbers:
        count_set_numb[count_numbers[j]] = count_set_numb.get(count_numbers[j], 0) + 1

    res = n
    last = 0
    all_next = n
    uniq_next = len(count_numbers)
    for j in sorted(count_set_numb):
        res = min(res, last + all_next - uniq_next * j)
        last += j * count_set_numb[j]
        all_next -= j * count_set_numb[j]
        uniq_next -= count_set_numb[j]
       
    print(res)


for i in range(int(input())):
    find()
