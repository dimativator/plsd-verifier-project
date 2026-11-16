#include <bits/stdc++.h>
using namespace std;
void err(istream_iterator<string> it) {}
template <typename T, typename... Args>
void err(istream_iterator<string> it, T a, Args... args) {
  cerr << *it << " = " << a << ", ";
  err(++it, args...);
}
long long mod(long long n) {
  return (n % 1000000007 + 1000000007) % 1000000007;
}
int32_t main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);
  long long n;
  cin >> n;
  vector<long long> vec(n);
  long long tot_sum = 0;
  for (long long i = 0; i < n; ++i) {
    cin >> vec[i];
    tot_sum += vec[i];
  }
  bool flag = false;
  vector<long long> index;
  for (long long i = 1; i < (1 << n) - 1 and !flag; ++i) {
    long long sum = 0;
    index.clear();
    for (long long j = 0; j < n; ++j) {
      if (i & (1 << j)) {
        sum += vec[j];
        index.emplace_back(j + 1);
      }
    }
    if (sum != (tot_sum - sum)) {
      flag = true;
    }
  }
  if (!flag) {
    cout << -1 << '\n';
  } else {
    cout << (long long)(index).size() << '\n';
    for (auto i : (index)) {
      cout << i << " ";
    }
    cout << '\n';
  }
  return 0;
}
