n = int(input(""))
cards=list(map(int,input().split()))

sereja = 0
dima = 0
temp = 0
turn = 1


while cards != []:
    nMax=max(cards[0],cards[-1])
    
    if turn==1:
        temp = sereja + nMax
        sereja+=nMax
        turn=2
    else:
        temp = dima + nMax
        dima+=nMax
        turn=1
    cards.remove(nMax)

print("{} {}".format(sereja, dima))