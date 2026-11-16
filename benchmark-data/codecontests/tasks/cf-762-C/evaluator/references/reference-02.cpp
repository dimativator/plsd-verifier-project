#include <bits/stdc++.h>
using namespace std;
long long gcd(long long a, long long b) { return b == 0 ? a : gcd(b, a % b); }
const int MAXLEN = 100000;
char a[MAXLEN + 1];
int alen;
char b[MAXLEN + 1];
int blen;
int ldp[MAXLEN + 1];
int rdp[MAXLEN + 1];
int nxt[MAXLEN + 1][26];
int prv[MAXLEN + 1][26];
void run() {
  scanf("%s%s", a, b);
  alen = strlen(a);
  blen = strlen(b);
  for (int j = (0); j < (26); ++j) nxt[alen][j] = INT_MAX;
  for (int i = alen - 1; i >= 0; --i)
    for (int j = (0); j < (26); ++j)
      nxt[i][j] = a[i] - 'a' == j ? i : nxt[i + 1][j];
  for (int j = (0); j < (26); ++j) prv[0][j] = INT_MIN;
  for (int i = (0); i < (alen); ++i)
    for (int j = (0); j < (26); ++j)
      prv[i + 1][j] = a[i] - 'a' == j ? i : prv[i][j];
  ldp[0] = 0;
  for (int i = (0); i < (blen); ++i) {
    int cur = nxt[ldp[i]][b[i] - 'a'];
    ldp[i + 1] = cur == INT_MAX ? INT_MAX : cur + 1;
  }
  rdp[blen] = alen;
  for (int i = blen - 1; i >= 0; --i) rdp[i] = prv[rdp[i + 1]][b[i] - 'a'];
  int ret = 0, retl = 0, retr = blen;
  int curl = 0, curr = blen;
  while (curr >= 0) {
    while (curl + 1 < curr && ldp[curl + 1] <= rdp[curr]) ++curl;
    while (curl - 1 >= 0 && ldp[curl] > rdp[curr]) --curl;
    if (ldp[curl] > rdp[curr]) break;
    int cur = curl + blen - curr;
    if (cur > ret) ret = cur, retl = curl, retr = curr;
    --curr;
    if (curl > curr) curl = curr;
  }
  if (ret == 0)
    printf("-\n");
  else {
    for (int i = (0); i < (retl); ++i) printf("%c", b[i]);
    for (int i = (retr); i < (blen); ++i) printf("%c", b[i]);
    puts("");
  }
}
int main() {
  run();
  return 0;
}
