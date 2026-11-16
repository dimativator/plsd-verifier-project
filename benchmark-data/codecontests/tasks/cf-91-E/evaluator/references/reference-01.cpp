#include <bits/stdc++.h>
using namespace std;
struct line {
  long long int a, b, id;
  line() { a = b = id = 0; }
  line(long long int i, long long int j) : a(i), b(j) {}
  line(long long int i, long long int j, long long int k) : a(i), b(j), id(k) {}
  long long int value_at(long long int x) { return a * x + b; }
  bool operator<(line g) const { return (a != g.a) ? (a < g.a) : (b > g.b); }
  bool operator==(line g) const { return a == g.a && b == g.b; }
};
struct cht {
  vector<line> ch;
  cht() { ch.clear(); }
  void printa() {
    printf("\nCH:\n");
    for (long long int i = 0; i < ch.size(); i++) {
      printf("%lld x  + %lld\n", ch[i].a, ch[i].b);
    }
    printf("\n");
  }
  bool can_pop(line ant, line top, line at) {
    return (at.b - ant.b) * (ant.a - top.a) <= (top.b - ant.b) * (ant.a - at.a);
  }
  void add_line(long long int a, long long int b, long long int i) {
    line at(a, b, i);
    long long int sz = ch.size();
    while (sz > 1 && can_pop(ch[sz - 2], ch[sz - 1], at)) {
      ch.pop_back();
      sz--;
    }
    ch.push_back(at);
  }
  long long int query(long long int x) {
    long long int sz = ch.size();
    long long int ini = 0, fim = sz - 2, meio;
    if (sz == 1) return 0;
    long long int ans = sz - 1;
    while (ini <= fim) {
      meio = (ini + fim) / 2;
      if (ch[meio].value_at(x) < ch[meio + 1].value_at(x)) {
        ini = meio + 1;
      } else {
        ans = meio;
        fim = meio - 1;
      }
    }
    return ans;
  }
};
cht st[101010 << 2];
long long int A[101010], B[101010], n, q;
void join(long long int p, long long int esq, long long int dir) {
  vector<line> aux;
  for (long long int i = 0; i < st[esq].ch.size(); i++)
    aux.push_back(st[esq].ch[i]);
  for (long long int i = 0; i < st[dir].ch.size(); i++)
    aux.push_back(st[dir].ch[i]);
  sort(aux.begin(), aux.end());
  st[p].add_line(aux[0].a, aux[0].b, aux[0].id);
  for (long long int i = 1; i < aux.size(); i++) {
    if (aux[i].a == aux[i - 1].a) continue;
    st[p].add_line(aux[i].a, aux[i].b, aux[i].id);
  }
}
void build(long long int p, long long int l, long long int h) {
  if (l == h) {
    st[p].add_line(A[l], B[l], l);
    return;
  }
  long long int mid = (l + h) >> 1, nxt = p << 1;
  build(nxt, l, mid);
  build(nxt + 1, mid + 1, h);
  join(p, nxt, nxt + 1);
}
pair<long long int, long long int> query(long long int p, long long int l,
                                         long long int h, long long int a,
                                         long long int b, long long int x) {
  if (h < a || l > b) return pair<long long int, long long int>(-1000, -1000);
  if (a <= l && b >= h) {
    long long int ans = st[p].query(x);
    return pair<long long int, long long int>(st[p].ch[ans].id,
                                              st[p].ch[ans].value_at(x));
  }
  long long int mid = (l + h) >> 1, nxt = p << 1;
  pair<long long int, long long int> u = query(nxt, l, mid, a, b, x);
  pair<long long int, long long int> v = query(nxt + 1, mid + 1, h, a, b, x);
  if (u.second > v.second) return u;
  return v;
}
int main() {
  scanf("%lld %lld", &n, &q);
  for (long long int i = 1; i <= n; i++) {
    scanf("%lld %lld", &B[i], &A[i]);
  }
  build(1, 1, n);
  long long int a, b, x;
  while (q--) {
    scanf("%lld %lld %lld", &a, &b, &x);
    pair<long long int, long long int> ans = query(1, 1, n, a, b, x);
    printf("%lld\n", ans.first);
  }
}
