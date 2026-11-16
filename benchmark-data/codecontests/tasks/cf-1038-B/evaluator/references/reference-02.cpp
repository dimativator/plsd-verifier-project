#include <bits/stdc++.h>
using namespace std;
vector<long long> let(26, 0);
int main() {
  long long n;
  cin >> n;
  if (n <= 2) {
    cout << "No" << endl;
  } else {
    cout << "Yes" << endl;
    cout << n - 1 << " ";
    for (int i = 0; i < n - 1; i++) {
      cout << i + 1 << " ";
    }
    cout << endl << 1 << " " << n << endl;
  }
  return 0;
}
