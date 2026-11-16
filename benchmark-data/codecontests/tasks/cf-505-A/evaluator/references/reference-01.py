# 505A

__author__ = 'artyom'

# SOLUTION

def main():
  s = list(read(0))
  n = len(s)
  m = n // 2
  for i in range(n + 1):
    p = s[:i] + [s[n - i - (i <= m)]] + s[i:n]
    if p == p[::-1]:
      return p
  return 'NA'


# HELPERS


def read(mode=2):
  # 0: String
  # 1: List of strings
  # 2: List of integers
  inputs = input().strip()
  if mode == 0: return inputs
  if mode == 1: return inputs.split()
  if mode == 2: return int(inputs)
  if mode == 3: return list(map(int, inputs.split()))


def write(s="\n"):
  if s is None: s = ''
  if isinstance(s, list): s = ''.join(map(str, s))
  s = str(s)
  print(s, end="")


write(main())