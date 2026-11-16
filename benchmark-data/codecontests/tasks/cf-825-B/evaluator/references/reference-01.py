mat=[]
n=10 
m=10 
for i in range(n):
    s=input()
    s=list(s)
    mat.append(s)
f=0 
def check(mat): 
    for i in range(10):
        for j in range(10):
            #horizontal
            for k in range(5): 
                if (i+k)>=10 or mat[i+k][j]!='X':
                    break 
            else:
                return 1 
            #vertical 
            for k in range(5):
                if (j+k)>=10 or mat[i][j+k]!='X':
                    break 
            else :
                return 1 
            #diag 
            for k in range(5):
                if (i+k)>=10 or (j+k)>=10 or mat[i+k][j+k]!='X':
                    break 
            else :
                return 1 
            for k in range(5):
                if (i+k)>=10 or (j-k)<0 or mat[i+k][j-k]!='X':
                    break 
            else :
                return 1 
    return 0 
            
for i in range(n):
    for j in range(m):
        if mat[i][j]=='.':
            mat[i][j]='X'
            if check(mat):
                f=1 
                print('YES')
                exit() 
            else:
                mat[i][j]='.'
print('NO')