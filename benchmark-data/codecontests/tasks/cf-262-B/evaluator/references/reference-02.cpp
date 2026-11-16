#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, k;
  cin >> n >> k;
  int sum = 0, count_neg = 0;
  vector<int> v;
  int x;
  for (int i = 0; i < n; i++) {
    cin >> x;
    v.push_back(x);
    sum += x;
    if (x < 0) count_neg++;
  }
  for (int i = 0; i < min(count_neg, k); i++) {
    sum += -2 * v[i];
  }
  int ele;
  if (count_neg) {
    ele = min(-v[count_neg - 1], v[count_neg]);
  } else {
    ele = v[count_neg];
  }
  for (int i = 0; i < (k - count_neg); i++) {
    ele = -1 * ele;
    sum += 2 * ele;
  }
  cout << sum;
  return 0;
}
