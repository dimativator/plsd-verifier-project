class Ball:
    def __init__(self, x, v, m):
        self.v = v
        self.x = x
        self.m = m

    def move(self, time):
        self.x += self.v * time

    def collisionTime(self, other):
        if self.v == other.v:
            return float("inf")

        t = - (self.x - other.x) / (self.v - other.v)

        if t < 1e-9:
            return float("inf")
        return t 
        
    def __str__(self):
        return "Ball(x={:.2f} v={:.2f} m={:.2f})".format(self.x, self.v, self.m)


def findFirst():
    global nBalls, balls

    minTime = float("inf")
    minPairs = []

    for i in range(nBalls):
        for j in range(i + 1, nBalls):
            time = balls[i].collisionTime(balls[j])
            if time < minTime:
                minTime = time
                minPairs = [(i, j)]
            elif abs(time - minTime) < 1e-9:
                minPairs.append((i, j))
                
    return minTime, minPairs


def collidePair(i, j):
    global balls

    v1 = balls[i].v
    v2 = balls[j].v

    m1 = balls[i].m
    m2 = balls[j].m

    balls[i].v = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
    balls[j].v = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)



nBalls, maxTime = map(int, input().split())

balls = []
for i in range(nBalls):
    x, v, m = map(int, input().split())
    balls.append(Ball(x, v, m))

while True:
    time, pairs = findFirst()
    if time > maxTime:
        break
    
    for i in range(nBalls):
        balls[i].move(time)

    # print(time, maxTime)
    for i, j in pairs:
        collidePair(i, j)
        # print(i, balls[i], j, balls[j])
    # print()

    maxTime -= time
   

for ball in balls:
    ball.move(maxTime)
    print("{:.6f}".format(ball.x))
