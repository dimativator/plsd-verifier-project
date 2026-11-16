def f(grid):
  for i in range(9):
    for j in range(9):
      if grid[i][j] == '1':
        grid[i][j] = '2'

def main():
  t = int(input())
  for _ in range(t):
    grid = [[x for x in input()] for __ in range(9)]
    f(grid)
    for row in grid:
      print(''.join(row))
main()