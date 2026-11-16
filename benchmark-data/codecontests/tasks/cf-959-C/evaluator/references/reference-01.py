n = int(input())
if n <= 5:
    print(-1)
else:
    print('1 2', '1 3', '1 4', '2 5', sep = '\n')
    for i in range(6, n + 1):
        print('2 {0:d}'.format(i))
for i in range(2, n + 1):
    print('1 {0:d}'.format(i))
 	 		 		 		 	 	 	  	 			    	 	