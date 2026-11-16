#include <bits/stdc++.h>
using namespace std;
template <class T>
using vv = vector<vector<T>>;
template <class T>
ostream &operator<<(ostream &os, const vector<T> &t) {
  os << "{";
  for (int(i) = 0; (i) < (t.size()); ++(i)) {
    os << t[i] << ",";
  }
  os << "}" << endl;
  return os;
}
template <class T, size_t n>
ostream &operator<<(ostream &os, const array<T, n> &t) {
  os << "{";
  for (int(i) = 0; (i) < (n); ++(i)) {
    os << t[i] << ",";
  }
  os << "}" << endl;
  return os;
}
template <class S, class T>
ostream &operator<<(ostream &os, const pair<S, T> &t) {
  return os << "(" << t.first << "," << t.second << ")";
}
template <class S, class T, class U>
ostream &operator<<(ostream &os, const tuple<S, T, U> &t) {
  return os << "(" << get<0>(t) << "," << get<1>(t) << "," << get<2>(t) << ")";
}
template <class S, class T, class U, class V>
ostream &operator<<(ostream &os, const tuple<S, T, U, V> &t) {
  return os << "(" << get<0>(t) << "," << get<1>(t) << "," << get<2>(t) << ","
            << get<3>(t) << ")";
}
template <class S, class T, class U, class V, class W>
ostream &operator<<(ostream &os, const tuple<S, T, U, V, W> &t) {
  return os << "(" << get<0>(t) << "," << get<1>(t) << "," << get<2>(t) << ","
            << get<3>(t) << "," << get<4>(t) << ")";
}
template <class T>
inline bool MX(T &l, const T &r) {
  return l < r ? l = r, 1 : 0;
}
template <class T>
inline bool MN(T &l, const T &r) {
  return l > r ? l = r, 1 : 0;
}
const long long MOD = 1e9 + 7;
template <class T>
class RMxQ {
  vv<T> vals;

 public:
  inline T get(int l, int r) {
    if (l == r) return vals[0][l];
    const int d = 31 - __builtin_clz(l ^ r);
    return max(vals[d][l], vals[d][r]);
  }
  RMxQ(){};
  RMxQ(vector<T> &v, T e = MOD) { init(v, e); }
  void init(vector<T> &v, T e) {
    int n = v.size();
    int d = 1, N = 2;
    while (N < n) N *= 2, ++d;
    vals.resize(d, vector<T>(N, e));
    for (int(i) = 0; (i) < (n); ++(i)) vals[0][i] = v[i];
    for (int(i) = 1; (i) < (d); ++(i))
      for (int(j) = 0; (j) < (N); ++(j)) {
        const int b = (j >> i | 1) << i;
        vals[i][j] = j >> i & 1 ? get(b, j) : get(j, b - 1);
      }
  }
};
template <class T>
class RMQ {
  vv<T> vals;

 public:
  inline T get(int l, int r) {
    if (l == r) return vals[0][l];
    const int d = 31 - __builtin_clz(l ^ r);
    return min(vals[d][l], vals[d][r]);
  }
  RMQ(){};
  RMQ(vector<T> &v, T e = -MOD) { init(v, e); }
  void init(vector<T> &v, T e) {
    int n = v.size();
    int d = 1, N = 2;
    while (N < n) N *= 2, ++d;
    vals.resize(d, vector<T>(N, e));
    for (int(i) = 0; (i) < (n); ++(i)) vals[0][i] = v[i];
    for (int(i) = 1; (i) < (d); ++(i))
      for (int(j) = 0; (j) < (N); ++(j)) {
        const int b = (j >> i | 1) << i;
        vals[i][j] = j >> i & 1 ? get(b, j) : get(j, b - 1);
      }
  }
};
class Lca {
 public:
  vector<int> dep, cld;
  vector<pair<int, int>> et;
  vector<int> l, r;
  vector<long long> wdep;
  vector<int> par;
  int weighted;
  vv<int> wei;
  RMQ<pair<int, int>> rmq;
  void dfs(const vv<int> &g, int root) {
    int n = g.size();
    vector<int> vst(n);
    stack<int> st;
    st.push(root);
    while (!st.empty()) {
      int v = st.top();
      st.pop();
      if (vst[v] == 1) {
        vst[v] = 2;
        r[v] = et.size() - 1;
        for (int(i) = 0; (i) < (g[v].size()); ++(i))
          if (g[v][i] != par[v]) cld[v] += cld[g[v][i]] + 1;
        if (par[v] >= 0) et.emplace_back(dep[par[v]], par[v]);
      } else if (vst[v] == 0) {
        st.push(v);
        vst[v] = 1;
        l[v] = et.size();
        et.emplace_back(dep[v], v);
        for (int(i) = 0; (i) < (g[v].size()); ++(i))
          if (!vst[g[v][i]]) {
            dep[g[v][i]] = dep[v] + 1;
            wdep[g[v][i]] = wdep[v] + (weighted ? wei[v][i] : 1);
            par[g[v][i]] = v;
            st.push(g[v][i]);
          }
      }
    }
  }
  Lca(const vv<int> &g) : weighted(0) {
    int n = g.size();
    par.resize(n);
    dep.resize(n);
    wdep.resize(n);
    cld.resize(n);
    l.resize(n);
    r.resize(n);
    dfs(g, 0);
    rmq.init(et, pair<int, int>(MOD, 0));
  }
  Lca(const vv<pair<int, int>> &h) : weighted(1) {
    int n = h.size();
    vv<int> g(n);
    wei.resize(n);
    for (int(i) = 0; (i) < (n); ++(i))
      for (pair<int, int> x : h[i]) {
        g[i].push_back(x.first);
        wei[i].push_back(x.second);
      }
    par.resize(n);
    dep.resize(n);
    wdep.resize(n);
    cld.resize(n);
    l.resize(n);
    r.resize(n);
    dfs(g, 0);
    rmq.init(et, pair<int, int>(MOD, 0));
  }
  int LCA(int v, int w) {
    v = l[v];
    w = l[w];
    if (v > w) swap(v, w);
    return rmq.get(v, w).second;
  }
  long long dist(int v, int w) {
    return wdep[v] + wdep[w] - 2 * wdep[LCA(v, w)];
  }
};
int main() {
  ios_base::sync_with_stdio(false);
  cout << fixed << setprecision(0);
  cin.tie(0);
  int n, q;
  cin >> n >> q;
  vv<int> g(n);
  for (int(i) = 1; (i) < (n); ++(i)) {
    int p;
    cin >> p;
    --p;
    g[p].push_back(i);
  }
  Lca lca(g);
  vector<pair<int, int>> l(n);
  for (int(i) = 0; (i) < (n); ++(i)) l[i] = pair<int, int>(lca.l[i], i);
  RMQ<pair<int, int>> rmq(l, pair<int, int>(MOD, MOD));
  RMxQ<pair<int, int>> rMq(l, pair<int, int>(0, 0));
  (lca.et, lca.l, 1);
  auto kick = [&](int l, int r, int v) {
    int L = MOD, R = 0;
    if (l != v) {
      MN(L, rmq.get(l, v - 1).first);
      MX(R, rMq.get(l, v - 1).first);
    }
    if (r != v) {
      MN(L, rmq.get(v + 1, r).first);
      MX(R, rMq.get(v + 1, r).first);
    }
    (l, r, v, L, R, 1);
    return lca.rmq.get(L, R).first;
  };
  while (q--) {
    int l, r;
    cin >> l >> r;
    --l;
    --r;
    (l, r, 1);
    int a = rmq.get(l, r).second;
    int b = rMq.get(l, r).second;
    (rmq.get(l, r), rMq.get(l, r), 1);
    int x = kick(l, r, a);
    int y = kick(l, r, b);
    (a, b, x, y, 1);
    if (x < y) {
      cout << b + 1 << " " << y << "\n";
    } else {
      cout << a + 1 << " " << x << "\n";
    }
  }
  return 0;
}
