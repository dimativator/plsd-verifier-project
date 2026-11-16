#include <bits/stdc++.h>
using namespace std;
const int MOD = 1e9 + 7;
void solve() {
  long long q;
  cin >> q;
  double ans = 0;
  queue<int> qu;
  long long last = -1, sum = 0, cnt = 1, num = 0;
  while (q--) {
    int a;
    cin >> a;
    if (a == 1) {
      long long b;
      cin >> b;
      num++;
      qu.push(b);
      last = b;
    } else {
      if (num == 1)
        cout << 0 << "\n";
      else {
        while (1) {
          if (qu.front() < (double)(last + sum) / cnt) {
            sum += qu.front();
            cnt++;
            qu.pop();
          } else
            break;
        }
        cout << setprecision(10) << last - ((double)(last + sum)) / cnt << "\n";
      }
    }
  }
}
int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);
  cout.tie(NULL);
  ;
  solve();
}
