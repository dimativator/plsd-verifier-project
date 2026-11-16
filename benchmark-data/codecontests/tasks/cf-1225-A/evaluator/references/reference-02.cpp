#include <bits/stdc++.h>
using namespace std;
int main() {
  int a, b;
  cin >> a >> b;
  if (a == 9 && b == 1) {
    cout << a << " " << 10 * b;
    return 0;
  }
  if (abs(a - b) > 1) {
    cout << "-1";
  } else {
    if (a == b)
      cout << 10 * a << " " << 10 * b + 1;
    else if (a > b)
      cout << "-1";
    else
      cout << a << " " << b;
  }
  return 0;
}
