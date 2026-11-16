from sys import stdin, stdout, stderr, setrecursionlimit
setrecursionlimit(100000)

def debug (*e):
    if not __debug__:
        print(*e, file=stderr)

def dd(*vals):
    import inspect, re
    frame = inspect.getframeinfo(inspect.stack()[1][0])
    vs = re.search("dd\((.+)\)", frame.code_context[0]).group(1).split(",")
    if vs:
        debug(",".join("{0} = {1}".format(vs[i], v) for i,v in enumerate(vals)))

def trace(f):
    def traced(*args, **kw):
        debug("calling {} with args {}, {}".format(f.__name__, args, kw))
        return f(*args, **kw)
    return traced
#@trace
#def f(x):

def read():
    return stdin.readline().rstrip()

def readarr(sep=None, maxsplit=-1):
    return read().split(sep, maxsplit)

def readint():
    return int(read())

def readia(sep=None, maxsplit=-1):
    return [int(a) for a in readarr(sep, maxsplit)]

#write(1, 2, 3, sep="-", end="!")
def write(*args, **kwargs):
    sep = kwargs.get('sep', ' ')
    end = kwargs.get('end', '\n')
    stdout.write(sep.join(str(a) for a in args) + end)

#writea([1, 2, 3], sep="-", end="!")
def writea(arr, sep=' ', end='\n'):
    stdout.write(sep.join(str(a) for a in arr) + end)

n = readint()
xs = readia()

while True:
    xs.sort()
    xs.reverse()
    for i in range(1, n):
        if xs[i-1] > xs[i]:
            xs[i-1] -= xs[i]
            break
    else:
        write(sum(xs))
        break
