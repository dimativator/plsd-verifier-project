def good_string(string):
	if string[::-1] != string:
		return string
	else:
		string = string[-1] + string[:-1]
		try:
			return good_string(string)
		except:
			return -1

if __name__ == "__main__":
	queries = int(input())
	for _ in range(queries):
		string = input()
		print(good_string(string))

