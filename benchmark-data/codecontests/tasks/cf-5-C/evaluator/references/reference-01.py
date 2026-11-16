string = input()
n = len(string)

stack = []
mapping = [0]*n

# First we create an array where the array called mapping where the index of array
# gives the index of start of opening bracket in string and the value at that index 
# gives the index of closing bracket for corresponding opening bracket.

for idx, char in enumerate(string):

	if char == '(':
		# We add idx of ( to stack which will be used as idx in mapping
		stack.append(idx)

	# Map only those ')' which have an opening brace, empty stack signifies
	# closing brace has no opening brace.
	elif char == ')' and stack:
		mapping[stack.pop()] = idx 


# Once we have generated the mapping we scan the array the difference between the index and its 
# value gives us the len of current regular expression. Now we take the value at that index and 
# icrement it to see if there is some non zero value at that location signifing that the regular 
# expression can be expanded. We continue this till no more expansion or we have some current length
# more than previous expansions.


i = 0
mx = 0
cnt = 1
tmp_max = 0
prev_join_idx = 0

while i < n:
	# If value present at mapping
	if mapping[i]:
		curr_len = mapping[i] - i + 1

		# if we have some previous regx 
		if i == prev_join_idx + 1:
			tmp_max += curr_len
		else:
			tmp_max = curr_len 

		# We have found new regx whose len is more than all prev scanned regx
		if tmp_max > mx:
			mx = tmp_max 
			cnt = 1
		elif tmp_max == mx:
			cnt += 1

		prev_join_idx = mapping[i]
		i = mapping[i] + 1

	else:
		i +=1

print(mx, cnt)