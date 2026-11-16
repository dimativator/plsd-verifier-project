#include <bits/stdc++.h>
using namespace std;
string s;
unsigned int last_q = 1000010;
long long free_space = 0;
unsigned int t_lenght = 0;
unsigned int got['z' + 1];
unsigned int required['z' + 1];
unsigned int nextlast() {
  unsigned int i = last_q + 1;
  while (i < s.size()) {
    if (s[i] == '?')
      break;
    else
      ++i;
  }
  return i;
}
int main() {
  for (unsigned int i = 0; i < 'z' + 1; ++i) got[i] = required[i] = 0;
  cin >> s;
  unsigned int i;
  for (i = 0; i < s.size(); ++i) {
    if (s[i] == '?') {
      last_q = i;
      ++free_space;
      break;
    } else
      ++got[s[i]];
  }
  for (++i; i < s.size(); ++i) {
    if (s[i] == '?') {
      ++free_space;
    } else
      ++got[s[i]];
  }
  char k;
  while (cin >> k) {
    ++required[k];
    ++t_lenght;
  }
  while (true) {
    if (free_space == 0) {
      cout << s;
      return 0;
    } else {
      for (char i = 'a'; i < 'z' + 1 && free_space > 0; ++i) {
        while ((got[i] < required[i]) && (free_space > 0)) {
          ++got[i];
          --free_space;
          s[last_q] = i;
          last_q = nextlast();
        }
      }
      for (char i = 'a'; i < 'z' + 1; ++i) got[i] -= required[i];
    }
  }
  return 0;
}
