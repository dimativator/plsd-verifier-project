a,b = map(int,input().split())
if(b == a+1):
    print(str(a)+"9 "+str(b)+"0")
elif(b == a):
    print(str(a)+"0 "+str(a)+"1")
elif(b == 1 and a == 9):
    print("99 100")
else:
    print(-1)
