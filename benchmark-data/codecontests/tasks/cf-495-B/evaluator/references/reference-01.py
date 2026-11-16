a, b = map(int, input().split())

if a == b:
  print ('infinity')
elif b > a:
  print (0)
else:
  a -= b
  i = 1
  cont = 0

  while (i*i) <= a:
    if (a % i) == 0:
      if i > b:
        cont += 1
      if (a/i) > b and (i*i) != a:
        cont += 1
    i += 1
  print (cont)
	 	 	 			 	       				 		   		