def computeTiling(n):
    if n == 1:
        print("a\na\nf\nf")
        return

    for tiling in generateRowTilings(n):
        print("".join(tiling))
    
def generateRowTilings(n):
    for (rowNum, firstTile, pattern) in generateRowTilingPatterns(n):
        yield makeRowTiling(rowNum, firstTile, pattern, n)

def generateRowTilingPatterns(n):
    rows = (1, 2, 3, 4)
    firstTiles = ('a', 'a', 'd', 'e')
    patterns = ('bbcc', 'ccbb', 'deed', 'edde')
    return zip(rows, firstTiles, patterns)

def makeRowTiling(row, prefix, pattern, n):
    yield prefix
    yield from (pattern[i%4] for i in range(n-2))
    yield pattern[(n-2)%4] if (n%2 != (row-1)//2) else 'f'

if __name__ == '__main__':
    n = int(input())
    computeTiling(n)
