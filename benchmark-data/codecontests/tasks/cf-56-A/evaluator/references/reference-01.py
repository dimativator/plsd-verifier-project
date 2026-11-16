a=['ABSINTH','BEER','BRANDY','CHAMPAGNE', 'GIN', 'RUM', 'SAKE', 'TEQUILA', 'VODKA', 'WHISKEY', 'WINE']
l=0
for i in range(int(input())):
    x=input()
    try:
        if(int(x)<18):
            l+=1
    except:
        if(x in a):
            l+=1
print(l)