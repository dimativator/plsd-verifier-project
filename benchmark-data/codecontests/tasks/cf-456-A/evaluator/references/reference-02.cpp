#include <bits/stdc++.h>
using namespace std;
struct lap {
  int a;
  int b;
};
lap l[100005];
bool cmp(lap l1, lap l2) { return l1.a > l2.a; }
int main() {
  int n;
  cin >> n;
  for (int i = 0; i < n; i++) {
    cin >> l[i].a >> l[i].b;
  }
  sort(&l[0], &l[n], cmp);
  for (int i = n - 2; i >= 0; i--) {
    if (l[i].a > l[i + 1].a && l[i].b < l[i + 1].b) {
      cout << "Happy Alex";
      return 0;
    }
  }
  cout << "Poor Alex";
  return 0;
}
