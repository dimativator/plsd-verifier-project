number_of_testcases = 1 #int(input())
 
for _ in range(number_of_testcases):
    number_of_digits = int(input())
    ticket_number = input()
    ticket_number = list(ticket_number)
    first_half = ticket_number[:number_of_digits]
    second_half = ticket_number[number_of_digits:]
    #print(first_half)
    first_half.sort()
    second_half.sort()
    flag = 1
    if first_half[0] > second_half[0]:
        for i in range(number_of_digits):
            if first_half[i] <= second_half[i]:
                flag = 0
                #print("NO")
               
                
    else:
        for i in range(number_of_digits):
            if first_half[i] >= second_half[i]:
                flag = 0
                #print("NO")
               
                
    if flag==1:
        print("YES")
        
    else:
        print("NO")

