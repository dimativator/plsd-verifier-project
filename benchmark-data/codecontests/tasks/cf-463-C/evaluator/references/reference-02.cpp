#include <bits/stdc++.h>
using namespace std;
const long double PI = 4 * atan((long double)1);
const long long INF = 1e18;
const long long mod = 1e9 + 7;
const long long N = 2005;
long long n;
long long a[N][N];
vector<vector<long long> > b1(N, vector<long long>(N, 0));
vector<vector<long long> > b2(N, vector<long long>(N, 0));
void go1(long long i, long long j) {
  long long row = i, col = j;
  while (row < n and col < n) {
    b1[i][j] += a[row][col];
    row++, col++;
  }
  row = i, col = j;
  while (row < n and col < n) {
    b1[row][col] = b1[i][j];
    row++, col++;
  }
}
void go2(long long i, long long j) {
  long long row = i, col = j;
  while (row >= 0 and col < n) {
    b2[i][j] += a[row][col];
    row--, col++;
  }
  row = i, col = j;
  while (row >= 0 and col < n) {
    b2[row][col] = b2[i][j];
    row--, col++;
  }
}
int main() {
  ios::sync_with_stdio(false);
  cin.tie(0);
  cout.tie(0);
  long long tt = 1;
  for (long long qq = 1; qq <= (tt); ++qq) {
    cin >> n;
    for (long long i = 0; i < (n); ++i)
      for (long long j = 0; j < (n); ++j) cin >> a[i][j];
    {
      for (long long i = 0; i < (n); ++i) {
        go1(i, 0);
        if (i) go1(0, i);
      }
    }
    {
      for (long long i = 0; i < (n); ++i) {
        go2(i, 0);
        if (i) go2(n - 1, i);
      }
    }
    long long ma = 0, mb = 0;
    pair<long long, long long> p1, p2;
    for (long long i = 0; i < (n); ++i) {
      for (long long j = 0; j < (n); ++j) {
        long long z = b1[i][j] + b2[i][j] - a[i][j];
        if ((i + j) & 1) {
          if (ma <= z) {
            ma = z;
            p1 = {i + 1, j + 1};
          }
        } else {
          if (mb <= z) {
            mb = z;
            p2 = {i + 1, j + 1};
          }
        }
      }
    }
    cout << ma + mb << '\n';
    cout << p1.first << " " << p1.second << " " << p2.first << " " << p2.second
         << '\n';
  }
}
