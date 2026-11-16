#include <bits/stdc++.h>
std::mt19937 rng(
    (int)std::chrono::steady_clock::now().time_since_epoch().count());
struct Edge {
  int u, v;
  Edge() {}
  Edge(int a, int b) : u(std::min(a, b)), v(std::max(a, b)) {}
  bool operator<(const Edge &o) const { return u != o.u ? u < o.u : v < o.v; }
  bool operator==(const Edge &o) const { return u == o.u && v == o.v; }
};
class ChoiceMatroid {
 public:
  ChoiceMatroid(const std::vector<int> &freq) : limit(freq) {}
  bool isIndependent(const std::vector<Edge> &a) {
    return getRank(a) == (int)a.size();
  }
  int getRank(const std::vector<Edge> &a) {
    cur = limit;
    int ans = 0;
    for (auto e : a) {
      if (cur[e.u] && cur[e.v]) {
        cur[e.u]--;
        cur[e.v]--;
        ans++;
      }
    }
    return ans;
  }

 private:
  std::vector<int> limit, cur;
};
class GraphicMatroid {
 public:
  GraphicMatroid(int n) : par(n, -1) {}
  bool isIndependent(const std::vector<Edge> &a) {
    return getRank(a) == (int)a.size();
  }
  int getRank(const std::vector<Edge> &a) {
    int ans = 0;
    for (auto e : a) {
      ans += makeUnion(e.u, e.v) ? 1 : 0;
    }
    for (auto e : a) {
      par[e.u] = par[e.v] = -1;
    }
    return ans;
  }

 private:
  std::vector<int> par;
  int getPar(int x) { return par[x] < 0 ? x : par[x] = getPar(par[x]); }
  bool makeUnion(int a, int b) {
    a = getPar(a), b = getPar(b);
    if (a == b) return false;
    if (par[a] < par[b]) std::swap(a, b);
    par[b] += par[a];
    par[a] = b;
    return true;
  }
};
template <class M1, class M2, class T>
class MatroidIntersection {
 public:
  MatroidIntersection(M1 m1, M2 m2, const std::vector<T> &obj)
      : n((int)obj.size()), objects(obj), present(obj.size(), false) {
    for (int i = 0; i < n; i++) {
      if (test(m1, i) && test(m2, i)) {
        present[i] = true;
        curAns++;
      }
    }
    while (augment(m1, m2))
      ;
  }
  std::vector<T> getSet(int o = -1) {
    std::vector<T> ans;
    for (int i = 0; i < n; i++) {
      if (present[i] && i != o) {
        ans.push_back(objects[i]);
      }
    }
    return ans;
  }

 private:
  int curAns = 0;
  int n;
  std::vector<T> objects;
  std::vector<bool> present;
  template <class M>
  bool test(M &m, int add, int rem = -1) {
    if (present[add] || (rem != -1 && !present[rem])) return false;
    auto st = getSet(rem);
    st.push_back(objects[add]);
    return m.isIndependent(st);
  }
  bool augment(M1 &m1, M2 &m2) {
    std::queue<int> q;
    std::vector<int> dist(n, -1);
    std::vector<int> frm(n, -1);
    std::vector<std::vector<int>> layers;
    for (int i = 0; i < n; i++) {
      if (test(m1, i)) {
        q.push(i);
        dist[i] = 0;
      }
    }
    if (q.empty()) {
      return false;
    }
    int limit = 1e9;
    auto outArc = [&](int u, bool phase) {
      std::vector<T> st;
      std::vector<int> others;
      if (present[u]) {
        for (int i = 0; i < n; i++) {
          if (present[i] && i != u) {
            st.push_back(objects[i]);
          } else if (!present[i] && dist[i] == (phase ? dist[u] + 1 : -1)) {
            others.push_back(i);
          }
        }
        auto _test = [&](int l, int r) {
          auto cur = st;
          for (int i = l; i < r; i++) {
            cur.push_back(objects[others[i]]);
          }
          return m1.getRank(cur) >= curAns;
        };
        int l = 0, r = (int)others.size();
        if (l == r || !_test(l, r)) return -1;
        while (l + 1 != r) {
          int mid = (l + r) / 2;
          if (_test(l, mid)) {
            r = mid;
          } else {
            l = mid;
          }
        }
        return others[l];
      } else {
        for (int i = 0; i < n; i++) {
          if (present[i] && dist[i] != (phase ? dist[u] + 1 : -1)) {
            st.push_back(objects[i]);
          } else if (present[i]) {
            others.push_back(i);
          }
        }
        auto _test = [&](int l, int r) {
          auto cur = st;
          for (int i = 0; i < l; i++) {
            cur.push_back(objects[others[i]]);
          }
          for (int i = r; i < (int)others.size(); i++) {
            cur.push_back(objects[others[i]]);
          }
          cur.push_back(objects[u]);
          return m2.isIndependent(cur);
        };
        int l = 0, r = (int)others.size();
        if (l == r || !_test(l, r)) return -1;
        while (l + 1 != r) {
          int mid = (l + r) / 2;
          if (_test(l, mid)) {
            r = mid;
          } else {
            l = mid;
          }
        }
        return others[l];
      }
    };
    while (!q.empty()) {
      int on = q.front();
      q.pop();
      if ((int)layers.size() <= dist[on]) layers.emplace_back(0);
      layers[dist[on]].push_back(on);
      if (dist[on] == limit) continue;
      for (int i = outArc(on, false); i != -1; i = outArc(on, false)) {
        assert(dist[i] == -1 &&
               (dist[on] % 2 == 0 ? test(m2, on, i) : test(m1, i, on)));
        q.push(i);
        dist[i] = dist[on] + 1;
        frm[i] = on;
        if (limit > n && test(m2, i)) {
          limit = dist[i];
        }
      }
    }
    if (limit > n) return false;
    auto rem = [&](int on) {
      assert(dist[on] != -1);
      auto it = std::find(layers[dist[on]].begin(), layers[dist[on]].end(), on);
      assert(it != layers[dist[on]].end());
      layers[dist[on]].erase(it);
      dist[on] = -1;
    };
    std::function<bool(int)> dfs = [&](int on) {
      if (dist[on] == 0 && !test(m1, on)) {
        rem(on);
        return false;
      }
      if (dist[on] == limit) {
        rem(on);
        if (test(m2, on)) {
          present[on] = !present[on];
          return true;
        } else {
          return false;
        }
      }
      for (int to = outArc(on, true); to != -1; to = outArc(on, true)) {
        if (dfs(to)) {
          rem(on);
          present[on] = !present[on];
          return true;
        }
      }
      rem(on);
      return false;
    };
    bool got = false;
    while (!layers[0].empty()) {
      if (dfs(layers[0].back())) {
        got = true;
        assert(m1.isIndependent(getSet()) && m2.isIndependent(getSet()));
        curAns++;
      }
    }
    assert(got);
    return true;
  }
};
int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  int t;
  std::cin >> t;
  while (t--) {
    int n, m;
    std::cin >> n >> m;
    std::vector<Edge> edges;
    std::vector<std::string> mat(n);
    std::vector<int> restriction(n * m);
    int need = 0;
    for (int i = 0; i < n; i++) {
      std::cin >> mat[i];
      for (int j = 0; j < m; j++) {
        if (mat[i][j] == 'O') {
          restriction[i * m + j] = (i + j) % 2 == 0 && i + j != 0 ? 2 : 4;
          if ((i + j) % 2 == 0 && i + j != 0) {
            need += 2;
          }
        } else {
          restriction[i * m + j] = 0;
        }
      }
    }
    for (int i = 0; i < n; i++) {
      for (int j = 0; j < m; j++) {
        if (mat[i][j] != 'O') continue;
        if (i != 0 && mat[i - 1][j] == mat[i][j])
          edges.emplace_back(i * m + j, (i - 1) * m + j);
        if (j != 0 && mat[i][j - 1] == mat[i][j])
          edges.emplace_back(i * m + j, i * m + j - 1);
      }
    }
    restriction[0] = 0;
    GraphicMatroid m1(n * m);
    ChoiceMatroid m2(restriction);
    auto ans =
        MatroidIntersection<GraphicMatroid, ChoiceMatroid, Edge>(m1, m2, edges)
            .getSet();
    if ((int)ans.size() == need) {
      std::cout << "YES\n";
      for (auto o : edges) {
        ans.push_back(o);
        if (!m1.isIndependent(ans)) {
          ans.pop_back();
        }
      }
      std::vector<std::string> wtf(2 * n - 1, std::string(2 * m - 1, ' '));
      for (auto o : ans) {
        int i = (o.u / m * 2 + o.v / m * 2) / 2;
        int j = (o.u % m * 2 + o.v % m * 2) / 2;
        wtf[i][j] = 'O';
      }
      for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
          wtf[2 * i][2 * j] = mat[i][j];
        }
      }
      for (auto str : wtf) {
        std::cout << str << '\n';
      }
    } else {
      std::cout << "NO\n";
    }
  }
}
