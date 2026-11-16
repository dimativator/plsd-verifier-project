#include <bits/stdc++.h>
using namespace std;
bool possible(map<int, int> &M) {
  map<int, int>::iterator it = M.begin(), jt = M.begin();
  jt++;
  if (M.size() == 2) {
    return (jt->first == 1 + it->first) and (it->second == jt->second);
  }
  if (jt->second < 2) return false;
  it->second--;
  if (it->second == 0) M.erase(it);
  jt->second--;
  return possible(M);
}
int main() {
  ios::sync_with_stdio(false);
  int n;
  cin >> n;
  if (n % 2 == 1) {
    cout << "NO" << endl;
    return 0;
  }
  map<int, int> M;
  int a;
  for (int i = 0; i < n; i++) {
    cin >> a;
    M[a]++;
  }
  if (possible(M)) {
    cout << "YES" << endl;
  } else {
    cout << "NO" << endl;
  }
  return 0;
}
