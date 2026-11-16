#include <bits/stdc++.h>
using namespace std;
template <class T>
struct Seg {
  const T ID = {0, -1};
  T comb(T a, T b) { return a.first >= b.first ? a : b; }
  int n;
  vector<T> seg;
  Seg(int _n) {
    n = _n;
    seg.resize(2 * n, ID);
  }
  void pull(int p) { seg[p] = comb(seg[2 * p], seg[2 * p + 1]); }
  void upd(int p, T value) {
    p += n;
    seg[p] = comb(seg[p], value);
    for (p /= 2; p; p /= 2) pull(p);
  }
  T query(int l, int r) {
    T ra = ID, rb = ID;
    for (l += n, r += n + 1; l < r; l /= 2, r /= 2) {
      if (l & 1) ra = comb(ra, seg[l++]);
      if (r & 1) rb = comb(seg[--r], rb);
    }
    return comb(ra, rb);
  }
};
int main() {
  ios::sync_with_stdio(0);
  cin.tie(0);
  cout.tie(0);
  int n, d;
  cin >> n >> d;
  vector<long long> h(n);
  for (long long &i : h) cin >> i;
  auto coordinate_compress = [d](vector<long long> h) {
    map<long long, int> compressed;
    for (long long i : h)
      compressed[i]++, compressed[i + d]++, compressed[i - d]++;
    int rank = 0;
    for (pair<const long long, int> &p : compressed) p.second = rank++;
    return compressed;
  };
  map<long long, int> compressed = coordinate_compress(h);
  vector<int> dp(n, 0);
  vector<int> from(n, 0);
  int N = compressed.size() + 1;
  Seg<pair<int, int>> seg_tree(N);
  for (int i = 0; i < n; i++) {
    pair<int, int> l = seg_tree.query(0, compressed[h[i] - d]);
    pair<int, int> r = seg_tree.query(compressed[h[i] + d], N - 1);
    if (l.first > r.first) {
      dp[i] = l.first + 1;
      from[i] = l.second;
    } else {
      dp[i] = r.first + 1;
      from[i] = r.second;
    }
    seg_tree.upd(compressed[h[i]], {dp[i], i});
  }
  int mx_idx = 0;
  for (int i = 1; i < n; i++) {
    if (dp[i] > dp[mx_idx]) mx_idx = i;
  }
  vector<int> ans;
  while (mx_idx != -1) ans.push_back(mx_idx), mx_idx = from[mx_idx];
  reverse(ans.begin(), ans.end());
  cout << ans.size() << "\n";
  for (int i : ans) cout << i + 1 << " ";
  cout << endl;
  return 0;
}
