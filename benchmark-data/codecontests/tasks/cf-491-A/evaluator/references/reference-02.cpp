#include <bits/stdc++.h>
using namespace std;
int main() {
  int a, b;
  cin >> a >> b;
  int t = 1;
  int f = 1;
  for (int i = 0; i < a + b + 1; i++) {
    if (i == a) {
      cout << a + b + 1 << " ";
      t = a + b;
      f = -f;
      continue;
    }
    cout << t << " ";
    t += f;
  }
}
