#include <bits/stdc++.h>
using namespace std;
int main() {
  int n, x;
  cin >> n;
  multimap<int, int> m, m1, m2;
  multimap<int, int>::reverse_iterator it;
  multimap<int, int>::iterator it1;
  for (int i = 1; i <= n; i++) {
    cin >> x;
    m.insert(pair<int, int>(x, i));
  }
  it = m.rbegin();
  m1.insert(pair<int, int>(it->first, it->second));
  it++;
  if (it != m.rend()) it++;
  if (it != m.rend()) it++;
  while (it != m.rend()) {
    m1.insert(pair<int, int>(it->first, it->second));
    it++;
    if (it != m.rend())
      m1.insert(pair<int, int>(it->first, it->second));
    else
      break;
    it++;
    if (it != m.rend()) it++;
    if (it != m.rend()) it++;
  }
  it = ++m.rbegin();
  while (it != m.rend()) {
    m2.insert(pair<int, int>(it->first, it->second));
    it++;
    if (it != m.rend())
      m2.insert(pair<int, int>(it->first, it->second));
    else
      break;
    it++;
    if (it != m.rend()) it++;
    if (it != m.rend()) it++;
  }
  cout << m1.size() << endl;
  for (it1 = m1.begin(); it1 != m1.end(); it1++) cout << it1->second << " ";
  cout << endl;
  cout << m2.size() << endl;
  for (it1 = m2.begin(); it1 != m2.end(); it1++) cout << it1->second << " ";
  cout << endl;
  return 0;
}
