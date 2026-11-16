napitki = int(input())
apelsina_v_soke = [int(x) for x in input().split()]
kokteil = sum(apelsina_v_soke) / napitki 
kokteil = format(kokteil, '.12f')
print(kokteil)