n = int(input())
if 1 <= n <= 100:
    for i in range(n):
        word = input()
        if len(word) > 10:
            numWord = str(len(word[1:-1]))
            print(word[0] + numWord + word[-1])
        else:
            print(word)
        
        
