#include <bits/stdc++.h>
using namespace std;
const int mod = 1000000007;
int main() {
  int n, k;
  cin >> n >> k;
  if (n <= 2 * k + 1) {
    cout << 1 << endl;
    cout << n / 2 + 1 << endl;
  } else {
    int count = n / (2 * k + 1);
    int rem = n % (2 * k + 1);
    if (rem == 0) {
      int mid = k + 1;
      cout << count << endl;
      while (count) {
        cout << mid << " ";
        mid = mid + 2 * k + 1;
        count--;
      }
      cout << endl;
    } else if (rem >= k + 1) {
      cout << count + 1 << endl;
      int mid = k + 1;
      while (count) {
        cout << mid << " ";
        mid += 2 * k + 1;
        count--;
      }
      cout << n - (rem - (k + 1)) << endl;
    } else {
      int mid = 1;
      cout << count + 1 << endl;
      rem = rem + k;
      while (count) {
        cout << mid << " ";
        mid = mid + 2 * k + 1;
        count--;
      }
      cout << n - (rem - (k + 1)) << endl;
    }
  }
}
