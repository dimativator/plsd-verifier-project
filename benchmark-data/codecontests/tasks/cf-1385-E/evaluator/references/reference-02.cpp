#include <bits/stdc++.h>
#pragma GCC optimize("O3")
#pragma GCC optimize("unroll-loops")
using namespace std;
using ull = unsigned long long;
using ll = long long;
using ld = long double;
using pii = pair<int, int>;
using pll = pair<long long, long long>;
using pil = pair<int, long long>;
using pli = pair<long long, int>;
using vi = vector<int>;
using vd = vector<double>;
using vl = vector<ll>;
using vii = vector<pii>;
using vll = vector<pll>;
constexpr char ln = '\n';
constexpr char sp = ' ';
constexpr int dy[] = {-1, 1, 0, 0, -1, -1, 1, 1};
constexpr int dx[] = {0, 0, -1, 1, -1, 1, -1, 1};
const ld PI = acos((ld)-1);
template <int fp>
struct fastio {
  fastio() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    if (fp) cout << fixed << setprecision(fp);
  }
};
template <typename Type>
void input(Type &arg) {
  cin >> arg;
}
template <typename Type, typename... Types>
void input(Type &arg, Types &...args) {
  cin >> arg;
  input(args...);
}
template <typename Type>
void output(Type arg) {
  cout << arg;
}
template <typename Type, typename... Types>
void output(Type arg, Types... args) {
  cout << arg;
  output(args...);
}
template <typename Type>
inline ostream &operator<<(ostream &out, const vector<Type> &v) {
  for (auto &i : v) out << i << ' ';
  return out;
}
template <typename Type>
inline istream &operator>>(istream &in, vector<Type> &v) {
  for (auto &i : v) in >> i;
  return in;
}
template <typename T>
T power(T a, T b, T mod = numeric_limits<T>::max()) {
  if (b == 0) return 1;
  if (b % 2) return a * power(a, b - 1, mod) % mod;
  return power(a * a % mod, b >> 1, mod);
}
vector<vector<int>> graph;
vector<int> indegree;
vector<pii> edge;
int main() {
  fastio<0>();
  int t;
  cin >> t;
  while (t--) {
    int n, m;
    cin >> n >> m;
    graph.clear();
    graph.resize(n);
    edge.clear();
    indegree.clear();
    indegree.resize(n);
    for (int i = 0; i < (m); i++) {
      int t, a, b;
      cin >> t >> a >> b;
      --a;
      --b;
      if (t == 1) {
        indegree[b]++;
        graph[a].push_back(b);
      } else
        edge.emplace_back(a, b);
    }
    queue<int> q;
    for (int i = 0; i < (n); i++)
      if (!indegree[i]) q.push(i);
    vector<int> res;
    while (!q.empty()) {
      int cur = q.front();
      q.pop();
      res.push_back(cur);
      for (auto &nxt : graph[cur]) {
        if (--indegree[nxt] == 0) q.push(nxt);
      }
    }
    if ((int)(res).size() < n) {
      cout << "NO\n";
      continue;
    } else {
      cout << "YES\n";
      vector<int> ans(n);
      for (int i = 0; i < (n); i++) ans[res[i]] = i;
      for (auto [a, b] : edge) {
        if (ans[a] > ans[b]) swap(a, b);
        cout << a + 1 << ' ' << b + 1 << ln;
      }
      for (int i = 0; i < n; i++) {
        for (auto &nxt : graph[i]) {
          cout << i + 1 << ' ' << nxt + 1 << ln;
        }
      }
    }
  }
  return 0;
}
