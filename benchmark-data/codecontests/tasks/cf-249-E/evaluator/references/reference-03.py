
if __name__ == "__main__":
	T = int(raw_input())
	for step in xrange(T):
		x0, y0, x1, y1 = map(int, raw_input().split(' '))
		ans = 0; mini = min(x1, y1); maxi = max(x0, y0)
		
		if max(x0, y0) <= min(x1, y1):
			ans += (x1 * (x1 + 1) * (x1 * 2 + 1) * (y1 - y0 + 1) - mini * (mini + 1) * (mini * 2 + 1) * y1 + (maxi - 1) * maxi * (maxi * 2 - 1) * (y0 - 1)) / 6
			ans += ((y1 - 1) * y1 * (y1 * 2 - 1) * (x1 - x0 + 1) - (mini - 1) * mini * (mini * 2 - 1) * x1 + (maxi - 2) * (maxi - 1) * (maxi * 2 - 3) * (x0 - 1)) / 6
			ans += (((y0 - 2) * (y0 - 1) * (x1 - maxi + 1) - (y1 - 1) * y1 * (x1 - mini)) + ((y1 - mini) * x1 * (x1 + 1) - (y1 - maxi + 1) * (x0 - 1) * x0)) / 2
			ans += ((mini * mini) * ((mini * mini) + 1) - ((maxi - 1) * (maxi - 1)) * (((maxi - 1) * (maxi - 1)) + 1)) / 2
		else:
			MAX = max(x1, y1)
			if x1 != MAX:
				ans += ((MAX - 1) * MAX * (MAX * 2 - 1) * (x1 - x0 + 1) + (maxi - 2) * (maxi - 1) * (maxi * 2 - 3) * (x0 - 1 - x1)) / 6
				ans += (MAX - maxi + 1) * (x1 * (x1 + 1) - (x0 - 1) * x0) / 2
			else:
				ans += (MAX * (MAX + 1) * (MAX * 2 + 1) * (y1 - y0 + 1) + (maxi - 1) * maxi * (maxi * 2 - 1) * (y0 - 1 - y1)) / 6
				ans += (MAX - maxi + 1) * ((y0 - 2) * (y0 - 1) - (y1 - 1) * y1) / 2
			
		print "..." + str(ans)[-10:] if 10000000000 <= ans else ans
			
			
			
