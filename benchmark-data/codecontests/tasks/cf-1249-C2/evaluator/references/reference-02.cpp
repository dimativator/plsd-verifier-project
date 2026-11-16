#include <bits/stdc++.h>
using namespace std;
void findpower(long long n, int times, vector<int> &p) {
  int remainder;
  if (n / 3 > 0) {
    remainder = n % 3;
    n /= 3;
    if (remainder != 0) {
      if (remainder == 1) {
        p.push_back(times);
      } else {
        p.push_back(times);
        p.push_back(times);
      }
    }
    times++;
    findpower(n, times, p);
  } else {
    if (n == 1 || n == 0) {
      p.push_back(times);
    } else {
      p.push_back(times);
      p.push_back(times);
    }
  }
}
long long makenumber(vector<int> powerof3) {
  long long number = 0;
  for (int i = 0; i < powerof3.size(); i++) {
    number += pow(3, powerof3[i]);
  }
  return number;
}
void optimize(vector<int> &q, long long n, long long number) {
  while (number >= n) {
    number -= pow(3, q.front());
    if (number >= n) {
      q.erase(q.begin());
    } else {
      number += pow(3, q.front());
      break;
    }
  }
  cout << number << "\n";
}
int main() {
  int q;
  long long n;
  cin >> q;
  while (q--) {
    long long number;
    vector<int> p;
    cin >> n;
    findpower(n, 0, p);
    vector<int> q;
    vector<int> l;
    map<int, int> m;
    int max1 = p.back() + 1;
    l.push_back(max1);
    for (int i = 0; i < p.size(); i++) {
      if (m.find(p[i]) == m.end()) {
        m[p[i]] = 1;
      } else {
        m[p[i]]++;
      }
    }
    map<int, int>::iterator it = m.begin();
    it = m.begin();
    while (it != m.end()) {
      if (it->second > 1) {
        if (m.find(it->first + 1) == m.end()) {
          m[it->first + 1] = 1;
        } else {
          m[it->first + 1]++;
        }
        it = m.erase(it);
      } else {
        it++;
      }
    }
    it = m.begin();
    for (it = m.begin(); it != m.end(); it++) {
      q.push_back(it->first);
    }
    int max2 = q.back();
    if (max1 == max2) {
      number = makenumber(l);
      cout << number << "\n";
    } else if (max2 < max1) {
      number = makenumber(q);
      optimize(q, n, number);
    }
  }
}
