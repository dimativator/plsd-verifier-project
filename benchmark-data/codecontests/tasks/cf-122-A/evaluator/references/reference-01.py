lucky_numbers = [4, 7, 44, 77, 47, 74, 444, 447, 474, 744, 777, 774, 747, 477]
n = input()
lucky = True
for i in range(0, len(n)):
    if n[i] != '4' and n[i] != '7' :
        lucky = False
        break

if lucky:
    print("YES")
else:
    lucky = False
    for i in lucky_numbers:
        if int(n) % i == 0:
            lucky = True
            break
    if lucky:
        print("YES")
    else:
        print("NO")
        