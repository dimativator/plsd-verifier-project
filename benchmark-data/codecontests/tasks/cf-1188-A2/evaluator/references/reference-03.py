from sys import*
class solution():
    def dfs(self, x, par, adj_arr):
        for adj in adj_arr[x]:
            if adj != par:
                return self.dfs(adj, x, adj_arr)
        return x
    def get_two_child(self, x, y, adj_arr):
        if len(adj_arr[x]) == 1:
            return x + 1, x + 1
        child1 = adj_arr[x][0]
        child2 = adj_arr[x][1]
        if child1 == y:
            child1 = child2
            child2 = adj_arr[x][2]
        if child2 == y:
            child2 = adj_arr[x][2]
        return self.dfs(child1, x, adj_arr) + 1, self.dfs(child2, x, adj_arr) + 1
    def main(self):
        n = int(stdin.readline())
        a = [[] for _ in range(n)]
        edges = []
        for i in range(n - 1):
            x, y, w = [int(val) for val in stdin.readline().split(" ")]
            x -= 1
            y -= 1
            a[x].append(y)
            a[y].append(x)
            edges.append((x, y, w))
        for val in a:
            if len(val) == 2:
                print "NO"
                return
        print "YES"
        result = []
        for x, y, w in edges:
            if w == 0:
                continue
            l1, l2 = self.get_two_child(x, y, a)
            r1, r2 = self.get_two_child(y, x, a)
            result.append((l1, r1, w / 2))
            result.append((l2, r2, w / 2))
            if l1 != l2:
                result.append((l1, l2, -(w / 2)))
            if r1 != r2:
                result.append((r1, r2, -(w / 2)))
        print len(result)
        for x in result:
            print " ".join([str(y) for y in x])
x = solution()
x.main()