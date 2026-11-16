n, q = map(int, raw_input().split(' '))
p_arr = map(lambda x:int(x) - 1, raw_input().split(' '))
p_arr = [-1] + p_arr
for i in p_arr[1:]:
  i += 1
pe_arr = [0 for i in xrange(n)]
s_arr = [1 for i in xrange(n)]
mx_arr = [-1 for i in xrange(n)]
z_arr = [i for i in xrange(n)]
for i in p_arr:
  if i > 0:
    pe_arr[i] += 1

arr = [i for i in xrange(n) if pe_arr[i] == 0]
while arr:
  i = arr.pop()
  while z_arr[i] != i and (s_arr[i] - s_arr[z_arr[i]]) * 2 > s_arr[i]:
    z_arr[i] = p_arr[z_arr[i]]
  if i == 0:
    continue
  fa = p_arr[i]
  s_arr[fa] += s_arr[i]
  if mx_arr[fa] < s_arr[i]:
    mx_arr[fa] = s_arr[i]
    z_arr[fa] = z_arr[i]
  pe_arr[fa] -= 1
  if pe_arr[fa] == 0:
    arr.append(fa)
q_arr = [int(raw_input()) - 1 for i in xrange(q)]
for i in q_arr:
  print z_arr[i] + 1
