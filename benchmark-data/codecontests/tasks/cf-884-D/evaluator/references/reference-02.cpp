#include <bits/stdc++.h>
using namespace std;
int n;
long long x, y, z, ans, tmp;
priority_queue<long long, vector<long long>, greater<long long> > pq;
int main() {
  scanf("%d", &n);
  for (int i = 0; i < n; i++) {
    scanf("%I64d", &tmp);
    pq.push(tmp);
  }
  if (n % 2 == 0) {
    x = pq.top();
    pq.pop();
    y = pq.top();
    pq.pop();
    pq.push(x + y);
    ans += (x + y);
  }
  while (pq.size() > 1) {
    x = pq.top();
    pq.pop();
    y = pq.top();
    pq.pop();
    z = pq.top();
    pq.pop();
    pq.push(x + y + z);
    ans += (x + y + z);
  }
  printf("%I64d\n", ans);
}
