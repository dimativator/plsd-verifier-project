#include <bits/stdc++.h>
using namespace std;
const long long N = 2000;
long long calcula(long long l, long long r, long long k) {
  long long d1 = -r;
  long long d2 = l - r;
  long long aum = d2 - d1;
  long long lim1 = d1;
  long long lim2 = d1 + (r * 1000000 - 1) * aum;
  if (lim1 <= k && k <= lim2 && (k - d1) % aum == 0) {
    long long num = (k - d1) / aum + 1;
    return num;
  }
  return -1;
}
int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);
  cout.precision(10);
  cout << fixed;
  long long k;
  cin >> k;
  for (long long i = 1; i <= N; i++) {
    for (long long j = 1; j <= N; j++) {
      if (i + j > N) break;
      long long aux = calcula(i, j, k);
      if (aux != -1) {
        cout << i + j << endl;
        for (long long a = 0; a < i - 1; a++) {
          cout << 0 << " ";
        }
        cout << -1 << " ";
        for (long long a = 0; a < j; a++) {
          cout << min(aux, 1000000ll) << " ";
          aux -= min(aux, 1000000ll);
        }
        cout << endl;
        return 0;
      }
    }
  }
  cout << -1 << endl;
  return 0;
}
