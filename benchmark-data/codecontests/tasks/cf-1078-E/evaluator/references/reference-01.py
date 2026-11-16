def C(x, y):
        return x + '10' + y + 't' + y

def CBF(x, y):
        return x + '01' + y + 't' + y

Cr = C('r', 'l')
Cl = C('l', 'r')
Cu = C('u', 'd')
Cd = C('d', 'u')

CBFr = CBF('r', 'l')
CBFl = CBF('l', 'r')
CBFu = CBF('u', 'd')
CBFd = CBF('d', 'u')

def CE(x, y):
        return x+x+'0'+x+'1'+y+y+'10'+y+'t'+x+x+'t'+y+x+x+'e'+x+'e'+y+y+y

def MNE(x, y):
        return CE(x, y) + x + C(y, x) + 'e' + y

def MNEall(n):
        return (MNE('d', 'u') + 'l') * n + 'r' * n + 'u' + (MNE('u', 'd') + 'l') * n + 'r' * n + 'd'

def ADD():
        return 'u' + Cu + 'u' + Cu + 'dd' + Cu + 'u' + Cu + 'u' + Cl + '010ltut' + Cd + 'dd'

def ADDc():
        return ADD() + '0ulrtd' + ADD() + 'lltr'

def ADDbit():
        return 'u' + Cu + 'u' + Cl + 'll0l1rrr' + ADDc() + 'dd' + Cu + 'u' + Cu + 'u' + Cl + ADDc() + 'dd'

def full(n):
        return MNEall(n) + 'uuu' + '0l' * (n+1) + 'r' * (n+1) + 'ddd' + (ADDbit() + 'l') * n + 'uuu'

print(full(30))