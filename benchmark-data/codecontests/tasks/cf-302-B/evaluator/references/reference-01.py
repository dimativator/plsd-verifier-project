# Getting input
song = list()
n,m=map(int,input().split())

song.append(0)
for i in range(n):
   note, times = map(int,input().split())
   total_time = song[i] +note*times                                                     
   song.append(total_time)


eugeny_moments = list(map(int, input().split()))
# computing result
counter = 0
for i in range(m):

    while(True):
        check = eugeny_moments[i] - song[counter]
        if check > 0:
           counter += 1
        else:
            break
    print(counter)
  		  			 			 	   	 	  	  			 	