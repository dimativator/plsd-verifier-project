#include <bits/stdc++.h>
using namespace std;
int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);
  cout.tie(NULL);
  int TESTS = 1;
  while (TESTS--) {
    int i, n;
    cin >> n;
    if (n < 6)
      cout << "-1" << endl;
    else {
      cout << "1 3" << endl << "1 2" << endl << "1 4" << endl;
      for (i = 5; i < n + 1; i++) cout << "2 " << i << endl;
    }
    for (i = 2; i < n + 1; i++) cout << "1 " << i << endl;
  }
}
