#include <bits/stdc++.h>
using namespace std;
int a, b, c;
pair<bool, pair<int, pair<int, int> > > poss(int k, int rem) {
  int j = max(1, (int)ceil((b - rem) * 1.0 / k));
  while (abs(k * j - b) <= rem) {
    int r = 1, cur = rem - abs(k * j - b), teb = k * j;
    r = max(1, (int)ceil((c - cur) * 1.0 / teb));
    while (abs(teb * r - c) <= cur) return {true, {k, {teb, teb * r}}};
    j++;
  }
  return {false, {0, {0, 0}}};
}
pair<bool, pair<int, pair<int, int> > > can(int ans) {
  if (abs(b - a) + abs(c - a) <= ans) return {true, {a, {a, a}}};
  if (abs(c - b) + abs(c - a) <= ans) return {true, {c, {c, c}}};
  if (abs(c - b) + abs(a - b) <= ans) return {true, {b, {b, b}}};
  for (int i = 0; i <= ans; i++) {
    pair<bool, pair<int, pair<int, int> > > val = poss(a + i, ans - i);
    if (val.first) return val;
    val = poss(a - i, ans - i);
    if (a - i > 0 && val.first) return val;
  }
  return {false, {0, {0, 0}}};
}
int main(int argc, char **argv) {
  ios_base::sync_with_stdio(0);
  cin.tie(0);
  cout.tie(0);
  int t;
  cin >> t;
  while (t--) {
    cin >> a >> b >> c;
    int ans = 1 << 15;
    pair<bool, pair<int, pair<int, int> > > num, anss;
    for (int i = 14; i >= 0; i--) {
      pair<bool, pair<int, pair<int, int> > > num = can(ans - (1 << i));
      if (num.first) anss = num, ans -= 1 << i;
    }
    num = can(0);
    if (num.first) ans = 0, anss = num;
    cout << ans << endl;
    cout << anss.second.first << " " << anss.second.second.first << " "
         << anss.second.second.second << endl;
  }
}
