#include <bits/stdc++.h>
using namespace std;
template <class T>
void debug(T a, T b) {
  for (; a != b; a++) cerr << *a << ' ';
  cerr << endl;
}
template <class T>
bool isprime(T x) {
  int till = (T)sqrt(x + .0);
  if (x <= 1) return 0;
  if (x == 2) return 1;
  if (x % 2 == 0) return 0;
  for (int i = 3; i <= till; i += 2)
    if (x % i == 0) return 0;
  return 1;
}
int n;
pair<int, int> s[100000];
int a[100000];
int b[100000];
int main() {
  cin >> n;
  for (int i = 0; i < int(n); i++) {
    cin >> s[i].first;
    s[i].second = i;
  }
  sort(s, s + n);
  for (int i = 0; i <= n / 3; i++) {
    a[s[i].second] = 0;
    b[s[i].second] = s[i].first;
  }
  for (int i = n / 3 + 1; i <= n / 3 * 2; i++) {
    a[s[i].second] = s[i].first;
    b[s[i].second] = 0;
  }
  for (int i = n / 3 * 2 + 1; i < n; i++) {
    a[s[i].second] = n - i;
    b[s[i].second] = s[i].first - (n - i);
  }
  cout << "YES\n";
  for (int i = 0; i < int(n); i++) cout << a[i] << " ";
  cout << "\n";
  for (int i = 0; i < int(n); i++) cout << b[i] << " ";
  cout << "\n";
  return EXIT_SUCCESS;
}
