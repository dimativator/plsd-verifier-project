#include <bits/stdc++.h>
using namespace std;
char c[2];
int main() {
  cin >> c;
  int res = 8;
  if (c[0] == 'a' || c[0] == 'h') res -= 3;
  if (c[1] == '1' || c[1] == '8') {
    res -= 3;
    if (c[0] == 'a' || c[0] == 'h') res++;
  }
  cout << res;
}
