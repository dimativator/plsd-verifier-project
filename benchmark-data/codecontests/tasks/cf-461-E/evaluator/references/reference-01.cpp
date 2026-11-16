#include <bits/stdc++.h>
using namespace std;
long long N;
char s[100005];
int M, D, A[3000005][4];
struct Mat {
  long long A[4][4];
  Mat() { memset(A, 0, sizeof(A)); }
  Mat operator*(const Mat& b) {
    Mat c;
    for (int i = 0; i <= 3; i++)
      for (int j = 0; j <= 3; j++) {
        c.A[i][j] = (1ll << 60);
        for (int k = 0; k <= 3; k++)
          c.A[i][j] = min(c.A[i][j], A[i][k] + b.A[k][j]);
      }
    return c;
  }
  Mat operator^(long long k) {
    Mat ret, a = *this;
    for (; k; k >>= 1, a = a * a)
      if (k & 1) ret = ret * a;
    return ret;
  }
} S;
void DFS(int u, int s, int d) {
  for (int i = 0; i <= 3; i++)
    if (A[u][i])
      DFS(A[u][i], s, d + 1);
    else
      S.A[s][i] = min(S.A[s][i], 1ll * d);
}
bool check(long long K) {
  Mat ret = S ^ K;
  long long x = 1ll << 60;
  for (int i = 0; i <= 3; i++)
    for (int j = 0; j <= 3; j++) x = min(x, ret.A[i][j]);
  return x < N;
}
int main() {
  scanf("%I64d%s", &N, s + 1);
  M = strlen(s + 1);
  for (int i = 1; i <= M; i++) {
    for (int x = 0, j = i; j <= i + 30 && j <= M; x = A[x][s[j] - 'A'], j++)
      if (!A[x][s[j] - 'A']) A[x][s[j] - 'A'] = ++D;
  }
  long long L = 0, R = N;
  for (int i = 0; i <= 3; i++)
    for (int j = 0; j <= 3; j++) S.A[i][j] = (1ll << 60);
  for (int i = 0; i <= 3; i++)
    if (A[0][i]) DFS(A[0][i], i, 1);
  for (; L + 1 < R;) {
    long long Mid = L + R >> 1;
    check(Mid) ? L = Mid : R = Mid;
  }
  printf("%I64d\n", L + 1);
}
