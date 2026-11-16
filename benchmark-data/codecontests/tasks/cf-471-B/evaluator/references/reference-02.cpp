#include <bits/stdc++.h>
using namespace std;
int n;
vector<pair<int, int>> a;
vector<pair<int, int>> b;
int main() {
  cin >> n;
  int m, dem = 0;
  for (int i = 1; i <= n; i++) {
    cin >> m;
    a.push_back(make_pair(i, m));
  }
  for (int i = 0; i < n - 1; i++)
    for (int j = i + 1; j < n; j++)
      if (a[i].second > a[j].second || a[i].first > a[j].first)
        swap(a[i], a[j]);
  for (int i = 0; i < n; i++)
    if (a[i].second == a[i + 1].second) dem++;
  if (dem < 2)
    cout << "NO";
  else {
    cout << "YES" << endl;
    for (auto x : a) cout << x.first << " ";
    cout << endl;
    b = a;
    for (int i = 0; i < n; i++)
      if (a[i].second == a[i + 1].second) {
        swap(a[i], a[i + 1]);
        break;
      }
    for (auto x : a) cout << x.first << " ";
    cout << endl;
    for (int i = 0; i < n - 1; i++)
      if (b[i].second == b[i + 1].second) swap(b[i], b[i + 1]);
    for (auto x : b) cout << x.first << " ";
  }
  return 0;
}
