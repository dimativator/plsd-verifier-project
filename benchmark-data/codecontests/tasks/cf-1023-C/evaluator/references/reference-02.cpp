#include <bits/stdc++.h>
using namespace std;
const int maxn = 2e5 + 7;
char stk[maxn];
int dp[maxn], sid[maxn], fl[maxn];
string s;
int main() {
  std::ios::sync_with_stdio(false);
  int n, k, top = 0;
  cin >> n >> k;
  cin >> s;
  for (int i = 0; i < s.size(); ++i) {
    stk[top] = s[i];
    sid[top++] = i;
    while (top > 1 && stk[top - 1] == ')' && stk[top - 2] == '(') {
      dp[sid[top - 2]] = sid[top - 1];
      top -= 2;
    }
  }
  memset(fl, 0, sizeof(fl));
  int l = 0;
  for (int i = 0; i < n - k; i += 2) {
    while (fl[l]) ++l;
    fl[l] = 1;
    fl[dp[l]] = 1;
  }
  for (int i = 0; i < s.size(); ++i)
    if (!fl[i]) cout << s[i];
  cout << endl;
  return 0;
}
