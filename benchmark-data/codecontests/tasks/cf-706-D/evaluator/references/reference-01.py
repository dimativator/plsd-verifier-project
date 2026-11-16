# ------------------- fast io --------------------
import os
import sys
from io import BytesIO, IOBase

BUFSIZE = 8192


class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None

    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)


class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")


sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
input = lambda: sys.stdin.readline().rstrip("\r\n")

# ------------------- fast io --------------------

class Trie:
    class Node:
        def __init__(self, char: bool = False):
            self.char = char
            self.children = []
            self.words = 0

    def __init__(self):
        self.root = Trie.Node()

    def add(self, word):
        node = self.root
        for char in word:
            found_in_child = False
            for child in node.children:
                if child.char == char:
                    node = child
                    found_in_child = True
                    break
            if not found_in_child:
                new_node = Trie.Node(char)
                node.children.append(new_node)
                node = new_node
        node.words += 1

    def remove(self, word):
        node = self.root
        nodelist = [node]
        for char in word:
            for child in node.children:
                if child.char == char:
                    node = child
                    nodelist.append(node)
                    break
        node.words -= 1
        if not node.children and not node.words:
            for i in range(len(nodelist)-2, -1, -1):
                nodelist[i].children.remove(nodelist[i+1])
                if nodelist[i].children or nodelist[i].words:
                    break

    def query(self, prefix, root=None):
        if not root: root = self.root
        node = root
        if not root.children:
            return 0
        prefix = [prefix]
        for char in prefix:
            char_not_found = True
            for child in node.children:
                if child.char == char:
                    char_not_found = False
                    node = child
                    break
            if char_not_found:
                return 0
        return node

di = {}
tr = Trie()
tr.add([False]*32)

for _ in range(int(input())):
    a, b = input().split()
    b = int(b)
    x = bin(b)[2:]
    x = "0"*(32 - len(x)) + x
    x = [False if k == '0' else True for k in x]
    if a == '+':
        tr.add(x)
    elif a == '-':
        tr.remove(x)
    else:
        ans = 0
        node = tr.root
        cnt = 32
        for i in x:
            cnt -= 1
            req = not i
            next = tr.query(req, node)
            if not next:
                node = tr.query(not req, node)
            else:
                node = next
                ans += 2**cnt
        print(ans)