party = list(map(int, input().split()))
friends, bottles, ml, limes, lime_slices, salt, friend_ml, friend_salt = party


total_gas = bottles * ml
total_limes = limes * lime_slices

rotation_ml = friend_ml * friends


q_tosts = -1
while all(x >= 0 for x in (salt, total_gas, total_limes)):
    total_gas -= rotation_ml 
    total_limes -= friends
    salt -= friend_salt * friends
    q_tosts += 1
print(q_tosts)