import re

input()
print(max(map(lambda s: len(set(s)), re.split('[A-Z]', input()))))