#!/usr/bin/env python3 

tree = input().strip()

def get_answer(tree, start_index = 0, prev = []):
  colon_index = tree.find(':', start_index)
  period_index = tree.find('.', start_index)
  name_end_index = colon_index if ((colon_index != -1) and (colon_index < period_index)) else period_index
  name = tree[start_index:name_end_index]
  answer = prev.count(name)
  if ((colon_index == -1) or (period_index < colon_index)):
    return (answer, period_index+1)
  else:
    # Recurse
    prev_names = prev + [name]
    next_start = colon_index
    while tree[next_start] != '.':
      (sub_answer, next_start) = get_answer(tree, next_start+1, prev_names)
      answer += sub_answer
    return (answer, next_start+1)

print(get_answer(tree)[0])