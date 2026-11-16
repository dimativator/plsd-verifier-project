#include <bits/stdc++.h>
using namespace std;
void fastscan(int &number) {
  bool negative = false;
  register int c;
  number = 0;
  c = getchar();
  if (c == '-') {
    negative = true;
    c = getchar();
  }
  for (; (c > 47 && c < 58); c = getchar()) number = number * 10 + c - 48;
  if (negative) number *= -1;
}
void Findsol() {
  string s[9];
  for (int i = 0; i < 9; i++) {
    getline(cin, s[i]);
  }
  char c1 = s[0].at(8);
  char c2 = s[0].at(7);
  for (int i = 0; i < 9; i++) {
    int ind = (i / 3 + 3 * (i % 3));
    if (s[i].at(ind) != c1) {
      s[i].at(ind) = c1;
    } else {
      s[i].at(ind) = c2;
    }
  }
  for (int i = 0; i < 9; i++) {
    cout << s[i] << "\n";
  }
}
int main() {
  int t;
  fastscan(t);
  while (t-- > 0) {
    Findsol();
  }
  return 0;
}
