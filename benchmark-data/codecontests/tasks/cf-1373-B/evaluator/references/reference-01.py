from sys import stdin,stdout
t=int(stdin.readline().strip())
for _ in range(t):
    s=stdin.readline().strip()
    stdout.write(("NET","DA")[min(s.count('0'),s.count('1')) % 2]+"\n")
