#include <bits/stdc++.h>
using namespace std;
map<int, int> a;
int main() {
  int n, ans = 0, k, sc;
  int maxi1 = 0, maxi2 = 0;
  int index = 0, films;
  cin >> n;
  for (int i(1); i <= n; i++) {
    cin >> sc;
    a[sc]++;
  }
  cin >> films;
  int ozv[films + 1], sub[films + 1];
  for (int film(1); film <= films; film++) cin >> ozv[film];
  for (int film(1); film <= films; film++) cin >> sub[film];
  for (int i(1); i <= films; i++) {
    if ((a[ozv[i]] >= maxi1 && a[sub[i]] >= maxi2) ||
        (a[ozv[i]] >= maxi1 && a[sub[i]] == maxi2) ||
        (a[ozv[i]] == maxi1 && a[sub[i]] >= maxi2) || a[ozv[i]] > maxi1) {
      maxi1 = a[ozv[i]];
      maxi2 = a[sub[i]];
      index = i;
    }
  }
  cout << index;
  return 0;
}
