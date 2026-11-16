#include <bits/stdc++.h>
using namespace std;
int main() {
  ios::sync_with_stdio(0);
  cin.tie(0);
  int t;
  cin >> t;
  string s = "ROYGBIV";
  int i = 0;
  while (t--) {
    cout << s[i++];
    if (i == 7) i = 3;
  }
  return 0;
}
