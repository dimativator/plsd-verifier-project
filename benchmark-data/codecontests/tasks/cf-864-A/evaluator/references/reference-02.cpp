#include <bits/stdc++.h>
using namespace std;
int num[105];
int main() {
  int n;
  cin >> n;
  set<int> s;
  while (n--) {
    int a;
    cin >> a;
    s.insert(a);
    num[a]++;
  }
  if (s.size() == 2 && num[*s.begin()] == num[*s.rbegin()]) {
    cout << "YES\n";
    cout << *s.begin() << " " << *s.rbegin() << endl;
  } else {
    cout << "NO\n";
  }
  return 0;
}
