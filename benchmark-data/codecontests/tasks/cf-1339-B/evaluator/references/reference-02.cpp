#include <bits/stdc++.h>
using namespace std;
void fast() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);
  cout.tie(NULL);
}
bool isPrime(long long int n) {
  if (n <= 1) return false;
  if (n <= 3) return true;
  if (n % 2 == 0 || n % 3 == 0) return false;
  for (long long int i = 5; i * i <= n; i = i + 6)
    if (n % i == 0 || n % (i + 2) == 0) return false;
  return true;
}
vector<long long int> primes;
void sieve(long long int n) {
  vector<bool> prime(n + 1, true);
  for (long long int p = 2; p * p <= n; p++) {
    if (prime[p] == true) {
      for (long long int i = p * 2; i <= n; i += p) prime[i] = false;
    }
  }
  for (int p = 2; p <= n; p++)
    if (prime[p]) primes.push_back(p);
}
long long int gcd(long long int x, long long int y) {
  if (y == 0) return x;
  return gcd(y, x % y);
}
long long int lcm(long long int a, long long int b) {
  return (a * b) / gcd(a, b);
}
vector<long long int> vin(long long int n) {
  vector<long long int> a(n);
  for (long long int i = 0; i < n; i++) cin >> a[i];
  return a;
}
void out(vector<long long int> a) {
  for (int i = 0; i < (long long int)a.size(); i++) {
    cout << a[i] << ' ';
  }
  cout << '\n';
}
void in(long long int *a, long long int n) {
  for (long long int i = 0; i < n; i++) cin >> a[i];
}
void out(long long int *a, long long int n) {
  for (long long int i = 0; i < n; i++) {
    cout << a[i] << " ";
  }
}
void out1(vector<long long int> v) {
  for (long long int i = 0; i < (long long int)v.size(); i++) {
    cout << v[i] << " ";
  }
  cout << '\n';
}
int main() {
  long long int t;
  cin >> t;
  while (t--) {
    long long int n;
    cin >> n;
    long long int a[n];
    for (long long int i = 0; i < n; i++) cin >> a[i];
    sort(a, a + n);
    vector<long long int> v1, v2, v3;
    for (long long int i = 0; i < n / 2; i++) {
      v1.push_back(a[i]);
    }
    if (n % 2 == 0) {
      for (long long int i = n / 2; i < n; i++) {
        v2.push_back(a[i]);
      }
    } else {
      for (long long int i = n / 2 + 1; i < n; i++) {
        v2.push_back(a[i]);
      }
    }
    reverse(v2.begin(), v2.end());
    for (long long int i = 0; i < v1.size(); i++) {
      v3.push_back(v2[i]);
      v3.push_back(v1[i]);
    }
    if (n % 2 != 0) {
      v3.push_back(a[n / 2]);
    }
    reverse(v3.begin(), v3.end());
    for (long long int i = 0; i < v3.size(); i++) {
      cout << v3[i] << " ";
    }
    cout << endl;
  }
  return 0;
}
