#include <bits/stdc++.h>
using namespace std;
int main() {
  long long i, j;
  long long N, H;
  cin >> N >> H;
  for (i = 1; i < N; i++) printf("%.6f ", ((float)sqrt(i) * H) / sqrt(N));
  return 0;
}
