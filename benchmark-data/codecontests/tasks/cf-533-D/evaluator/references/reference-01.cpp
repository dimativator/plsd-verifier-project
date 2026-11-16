#include <bits/stdc++.h>
using namespace std;
const int md = 1000000007;
const int maxn = 101010;
const int maxn4 = 4 * maxn;
const long long inf = 2020202020202020202LL;
int n;
double x[maxn], d[maxn];
double dr[maxn], dl[maxn];
vector<pair<int, int>> rf(maxn);
double poly[maxn];
void dodo(double dr[]) {
  dr[0] = x[n + 1];
  dr[n + 1] = -1;
  poly[0] = inf;
  poly[n + 1] = inf;
  rf[0] = make_pair(0, 1);
  rf[n + 1] = make_pair(n, n + 1);
  for (int i = 1; i <= n; i++) {
    poly[i] = d[i];
    rf[i] = make_pair(i - 1, i + 1);
  }
  vector<int> st;
  for (int i = 1; i <= n; i++) {
    poly[i] = d[i] - (x[i] - x[rf[i].first]) / 2;
    poly[rf[i].first] -= (x[i] - x[rf[i].first]) / 2;
    if (poly[rf[i].first] < 0) st.push_back(rf[i].first);
    while (st.size()) {
      int h = st[st.size() - 1];
      st.pop_back();
      double e = x[rf[h].second] - x[rf[h].first];
      e = e / 2;
      poly[rf[h].second] += (x[rf[h].second] - x[h]) / 2;
      poly[rf[h].second] -= e;
      poly[rf[h].first] += (-x[rf[h].first] + x[h]) / 2;
      poly[rf[h].first] -= e;
      if (poly[rf[h].first] < 0) st.push_back(rf[h].first);
      if (poly[rf[h].second] < 0 && rf[h].second < i)
        st.push_back(rf[h].second);
      rf[rf[h].second].first = rf[h].first;
      rf[rf[h].first].second = rf[h].second;
    }
    if (poly[i] <= 0)
      dr[i] = -1;
    else
      dr[i] = poly[i] * 2 + x[i];
  }
}
vector<pair<double, int>> santa, santa2, candy;
int main() {
  ios::ios_base::sync_with_stdio(0);
  cin >> n;
  for (int i = 0; i < n + 2; i++) {
    int a;
    scanf("%d", &a);
    x[i] = a;
  }
  for (int i = 0; i < n; i++) {
    int a;
    scanf("%d", &a);
    d[i + 1] = a;
  }
  dodo(dr);
  for (int i = 0; i < n + 2; i++) x[i] = x[n + 1] - x[i];
  reverse(x, x + n + 2);
  reverse(d, d + n + 2);
  dodo(dl);
  for (int i = 0; i < n + 2; i++) {
    dl[i] = x[n + 1] - dl[i];
    x[i] = x[n + 1] - x[i];
  }
  reverse(x, x + n + 2);
  reverse(d, d + n + 2);
  reverse(dl, dl + n + 2);
  for (int i = 0; i < n; i++)
    if (dl[i + 1] <= 0) {
      cout << "0";
      return 0;
    }
  for (int i = 0; i < n + 2; i++)
    if (dr[i] != -1) candy.push_back(make_pair(dr[i], i));
  for (int i = 0; i < n + 2; i++)
    if (dl[i] != 1 + x[n + 1]) santa.push_back(make_pair(dl[i], i));
  sort((candy).begin(), (candy).end());
  sort((santa).begin(), (santa).end());
  double ans = inf;
  int s = 0;
  set<int> xmas;
  for (int i = 0; i < candy.size(); i++) {
    if (s != santa.size())
      while (santa[s].first <= candy[i].first) {
        xmas.insert(santa[s].second);
        s++;
        if (s == santa.size()) break;
      }
    set<int>::iterator it = xmas.upper_bound(candy[i].second);
    if (it == xmas.end()) continue;
    double res = (x[*it] - x[candy[i].second]) / 2;
    if (res < ans) ans = res;
  }
  cout << ans;
  return 0;
}
