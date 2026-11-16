gh=set()
def rep(n,four,seven):
    global gh
    if n>10000000000 :return
    if (four==seven):gh|={n}
    rep(n*10+4,four+1,seven)
    rep(n*10+7,four,seven+1)
rep(0,0,0)
gh=sorted(gh)
def bin_s(a):
    lo=0;hi=len(gh);ans=0
    while lo<=hi:
        mid=(lo+hi)//2
        if gh[mid]>=a:ans=gh[mid];hi=mid-1
        else:lo=mid+1
    return ans
print(bin_s(int(input())))