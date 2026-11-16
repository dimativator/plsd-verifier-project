def cal(n,ind_list):
    ind1_list = [ind+1 for ind in ind_list]
    red_list =  [n-ind for ind in ind_list]

    pre_sum = [0]
    for ind1 in ind1_list:
        pre_sum.append(pre_sum[-1]+ind1)

    
    res = 0
    
    for i in range(1,len(red_list)):
        res += red_list[i]*pre_sum[i]
    return res

def getResult(n,a_list):
    v_dict = {}
    for i in range(n):
        v = a_list[i]
        if v in v_dict:
            v_dict[v].append(i)
        else:
            v_dict[v] = [i]
    res= 0
    for v in v_dict.keys():
        if len(v_dict[v])>=2:
            res += cal(n,v_dict[v])
    return res


t = int(input())
for _ in range(t):
    n = int(input())
    a_list = [int(k) for k in input().split()]
    print(getResult(n,a_list))