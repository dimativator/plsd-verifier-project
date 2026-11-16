#include <bits/stdc++.h>
using namespace std;
int arr[310];
int main() {
  int n, sum = 0, i, sum2 = 0;
  cin >> n;
  bool exit = true;
  for (i = 0; i < n; i++) {
    cin >> arr[i];
    sum += arr[i];
  }
  sum2 = sum;
  while (exit) {
    for (i = 0; i < n; i++) {
      if (sum != sum2 && i == 0) continue;
      if (arr[i] > 0) {
        cout << "P";
        arr[i]--;
        sum--;
      }
      if (sum == 0) break;
      if (i + 1 < n) cout << "R";
    }
    if (sum != 0) {
      cout << "L";
    } else
      break;
    for (i = n - 2; i >= 0; i--) {
      if (arr[i] > 0) {
        cout << "P";
        arr[i]--;
        sum--;
      }
      if (sum == 0) break;
      if (i - 1 >= 0) cout << "L";
    }
    if (sum == 0)
      exit = false;
    else
      cout << "R";
  }
  cout << endl;
  return 0;
}
