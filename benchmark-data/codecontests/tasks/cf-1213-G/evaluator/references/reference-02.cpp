#include <bits/stdc++.h>
using namespace std;
set<pair<long long, pair<long long, long long> > > st;
set<pair<long long, pair<long long, long long> > >::iterator it;
set<pair<long long, long long> > sl;
set<pair<long long, long long> >::iterator kt;
long long x[300005], y[300005], siz[300005], parent[300005], z[300005];
vector<long long> v;
vector<long long>::iterator jt;
void make_set(long long v) {
  parent[v] = v;
  siz[v] = 1;
}
long long find_set(long long v) {
  if (v == parent[v]) return v;
  return parent[v] = find_set(parent[v]);
}
long long unionn(long long a, long long b) {
  a = find_set(a);
  b = find_set(b);
  long long f = 0;
  if (a != b) {
    f = siz[a] * siz[b];
    if (siz[a] < siz[b]) swap(a, b);
    parent[b] = a;
    siz[a] += siz[b];
  }
  return f;
}
void add(long long lo, long long hi, long long val) {
  y[lo] += val;
  y[hi + 1] -= val;
}
int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);
  cout.tie(NULL);
  long long a = 0, b = 0, c, d, e, f = 0, l, g, m, n, k, i, j, t, p, q;
  cin >> n >> q;
  for (i = 1; i < n; i++) {
    cin >> a >> b >> c;
    st.insert({c, {a, b}});
  }
  for (i = 0; i < q; i++) {
    cin >> a;
    sl.insert({a, i});
    v.push_back(a);
  }
  sort(v.begin(), v.end());
  for (i = 1; i <= n; i++) {
    make_set(i);
  }
  it = st.begin();
  while (it != st.end()) {
    c = it->first;
    a = it->second.first;
    b = it->second.second;
    d = unionn(a, b);
    jt = lower_bound(v.begin(), v.end(), c);
    e = jt - v.begin();
    add(e, 300000, d);
    it++;
  }
  for (i = 1; i < 200005; i++) {
    y[i] += y[i - 1];
  }
  kt = sl.begin();
  a = 0;
  while (kt != sl.end()) {
    z[kt->second] = y[a];
    a++;
    kt++;
  }
  for (i = 0; i < q; i++) {
    cout << z[i] << ' ';
  }
  return 0;
}
