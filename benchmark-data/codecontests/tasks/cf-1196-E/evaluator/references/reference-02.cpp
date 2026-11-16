#include <bits/stdc++.h>
using namespace std;
int main() {
  int n;
  cin >> n;
  for (int i = 1; i <= n; ++i) {
    int b, w, s = 2;
    cin >> b >> w;
    swap(b, w);
    if (b > w) swap(b, w), s = 3;
    if (b * 3 + 1 < w) {
      cout << "NO" << endl;
      continue;
    }
    cout << "YES" << endl;
    for (int i = 1; i <= b; ++i) cout << s << " " << i * 2 << endl;
    for (int i = 1; i <= b; ++i, --w) cout << s << " " << i * 2 - 1 << endl;
    if (w > 0) cout << s << " " << b * 2 + 1 << endl, w--;
    if (w > 0)
      for (int i = 1; i <= b && w > 0; ++i, w--)
        cout << s + 1 << " " << i * 2 << endl;
    if (w > 0)
      for (int i = 1; i <= b && w > 0; ++i, --w)
        cout << s - 1 << " " << i * 2 << endl;
  }
  return 0;
}
