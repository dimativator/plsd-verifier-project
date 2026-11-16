def answer():

    ans,count,j=0,0,0

    d=dict()
    

    for i in range(n):

        while(j==0 or d[a[j-1]] < k):
            if(j==n):
                j+=1
                break

            try:d[a[j]]+=1
            except:d[a[j]]=1

            count += 1

            m=n-count+1

            j+=1

        if(j > n):break

        ans+=m

        d[a[i]] -= 1

    return ans


n,k=map(int,input().split())
a=list(map(int,input().split()))


print(answer())

			 	   		   		    	 				   		