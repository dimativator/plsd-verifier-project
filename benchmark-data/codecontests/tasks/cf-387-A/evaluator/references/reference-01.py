def tmins():
  sh, sm = map(int, input().split(':'))
  return 60 * sh + sm

t = tmins() - tmins()
if t < 0:
  t += 60*24

print('%02d:%02d' % (t//60, t%60))
