#include <bits/stdc++.h>
using namespace std;
int a[5005];
int main() {
  int n, m;
  cin >> n >> m;
  for (int i = 0; i < n; i++) cin >> a[i];
  sort(a, a + n);
  int num = 0;
  for (int i = 0; i < n; i++) {
    if (a[i] != a[(i + (n / 2)) % n]) num++;
  }
  cout << num << endl;
  for (int i = 0; i < n; i++) {
    cout << a[i] << " " << a[(i + (n / 2)) % n] << endl;
  }
  return 0;
}
