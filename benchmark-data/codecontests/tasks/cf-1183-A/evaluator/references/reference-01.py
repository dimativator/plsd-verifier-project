def fun(x):
      s=0
      org=x      
      while(x):
            s+=x%10
            x=x//10
      temp=s%4
      if temp :
            org+=1
            return fun(org)
      else :
            return org
      
x=int(input())
print(fun(x))