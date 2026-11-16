import math

def Solve(x):
    if x == 0:
        return 0
    stage = int(math.floor(math.log(x,2)))
    odd = math.ceil(stage/2)
    even = math.floor(stage/2)
    even_terms = 2*(pow(4,even)-1)//3
    odd_terms = (pow(4,odd)-1)//3
    total = even_terms+odd_terms
    
    if (stage+1)%2 == 0:
        even_terms += x-total
    else:
        odd_terms += x-total

    sum_even_terms = even_terms*(1+even_terms)
    sum_odd_terms = odd_terms*(odd_terms)

    return (sum_even_terms%1000000007+sum_odd_terms%1000000007)%1000000007
    

def main():
    l,r = map(int,input().split())
    print((Solve(r)-Solve(l-1))%1000000007)

main()
