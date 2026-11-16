n = int(input())

sumo = n
while n>=10:
    sumo = 0
    while n!=0:
        sumo+=n%10
        n//=10
    n = sumo
print(sumo)