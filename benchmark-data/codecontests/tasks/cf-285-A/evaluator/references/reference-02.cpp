#include <bits/stdc++.h>
using namespace std;
int encode(const string &s, int dig) {
  int x = 0, k = dig;
  for (int i = 0; i < dig; i++) {
    x = k * x;
    for (int j = i + 1; j < dig; j++)
      if (s[j] < s[i]) x++;
    k--;
  }
  return x;
}
int main() {
  int n, k;
  scanf("%d", &n);
  ;
  scanf("%d", &k);
  ;
  for (int i = (1); i < (n - k); i++) cout << i << " ";
  for (int i = n; i >= n - k; i--) cout << i << " ";
  return 0;
}
