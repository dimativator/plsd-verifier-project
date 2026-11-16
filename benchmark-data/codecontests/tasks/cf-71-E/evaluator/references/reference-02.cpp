#include <bits/stdc++.h>
const int INF = 2147483647;
const int INF2 = 0x3f3f3f3f;
const long long INF64 = (long long)2e18;
const double INFD = 1e30;
const double EPS = 1e-9;
const double PI = std::acos(-1);
const int MOD = 1e9 + 7;
template <typename T>
inline T read() {
  T X = 0, w = 0;
  char ch = 0;
  while (!isdigit(ch)) {
    w |= ch == '-';
    ch = getchar();
  }
  while (isdigit(ch)) X = (X << 3) + (X << 1) + (ch ^ 48), ch = getchar();
  return w ? -X : X;
}
const int MAXN = 25;
const int MAXV = (1 << 17) + 5;
int n, m, k;
int dr[4] = {0, 1, 0, -1};
int dc[4] = {-1, 0, 1, 0};
int dr2[8] = {1, 1, 1, -1, -1, -1, 0, 0};
int dc2[8] = {1, 0, -1, 1, 0, -1, 1, -1};
int CASE = 1;
std::string element[110] = {
    "",   "H",  "He", "Li", "Be", "B",  "C",  "N",  "O",  "F",  "Ne", "Na",
    "Mg", "Al", "Si", "P",  "S",  "Cl", "Ar", "K",  "Ca", "Sc", "Ti", "V",
    "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br",
    "Kr", "Rb", "Sr", "Y",  "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag",
    "Cd", "In", "Sn", "Sb", "Te", "I",  "Xe", "Cs", "Ba", "La", "Ce", "Pr",
    "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu",
    "Hf", "Ta", "W",  "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi",
    "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "U",  "Np", "Pu", "Am",
    "Cm", "Bk", "Cf", "Es", "Fm"};
std::map<std::string, int> _map;
int A[MAXN];
int B[MAXN];
int sum[MAXV];
bool dp[20][MAXV];
int tr[20][MAXV];
std::vector<int> sat[1900];
int main() {
  for (int i = 1; i <= 105; i++) {
    _map[element[i]] = i;
  }
  scanf("%d%d", &n, &m);
  char str[10];
  for (int i = 0; i < n; i++) {
    scanf("%s", str);
    A[i] = _map[std::string(str)];
  }
  for (int i = 0; i < m; i++) {
    scanf("%s", str);
    B[i] = _map[std::string(str)];
  }
  for (int i = 0; i < (1 << n); i++) {
    for (int j = 0; j < n; j++) {
      if (i >> j & 1) sum[i] += A[j];
    }
    sat[sum[i]].push_back(i);
  }
  dp[0][(1 << n) - 1] = true;
  tr[0][(1 << n) - 1] = -1;
  for (int i = 0; i < m; i++) {
    for (int j = 0; j < (1 << n); j++) {
      if (dp[i][j]) {
        for (auto s : sat[B[i]]) {
          if ((s & j) != s) continue;
          dp[i + 1][j ^ s] = true;
          tr[i + 1][j ^ s] = s;
        }
      }
    }
  }
  std::vector<std::vector<int>> res;
  for (int i = 0; i < (1 << n); i++) {
    if (dp[m][i]) {
      for (int j = m - 1; j >= 0; j--) {
        int s = tr[j + 1][i];
        std::vector<int> e;
        for (int k = 0; k < n; k++) {
          if (s >> k & 1) {
            e.push_back(A[k]);
          }
        }
        e.push_back(B[j]);
        res.push_back(e);
        i |= s;
      }
      std::reverse(res.begin(), res.end());
      printf("YES\n");
      for (auto a : res) {
        printf("%s", element[a[0]].c_str());
        for (int i = 1; i < a.size() - 1; i++) {
          printf("+%s", element[a[i]].c_str());
        }
        printf("->%s\n", element[a[a.size() - 1]].c_str());
      }
      return 0;
    }
  }
  printf("NO\n");
  return 0;
}
