#include <bits/stdc++.h>
using namespace std;
int main() {
  char war[55][20] = {
      "WASHINGTON", "ADAMS",     "JEFFERSON", "MADISON",    "MONROE",
      "ADAMS",      "JACKSON",   "Van BUREN", "HARRISON",   "TYLER",
      "POLK",       "TAYLOR",    "FILLMORE",  "PIERCE",     "BUCHANAN",
      "LINCOLN",    "JOHNSON",   "GRANT",     "HAYES",      "GARFIELD",
      "ARTHUR",     "CLEVELAND", "HARRISON",  "Cleveland",  "McKinley",
      "ROOSEVELT",  "TAFT",      "WILSON",    "HARDING",    "COOLIDGE",
      "HOOVER",     "ROOSEVELT", "TRUMAN",    "EISENHOWER", "KENNEDY",
      "JOHNSON",    "NIXON",     "FORD",      "CARTER",     "REAGAN",
      "BUSH",       "CLINTON"};
  int num = 0;
  cin >> num;
  num--;
  string cur = war[num];
  istringstream iss(cur);
  string in = "";
  vector<string> print;
  while (iss >> in) {
    string p = "";
    if (num == 24) {
      p += in;
      print.push_back(p);
      continue;
    }
    for (int i = 0; i < in.size(); i++) {
      if (i == 0)
        p += in[i];
      else if (in[i] >= 'A' && in[i] <= 'Z')
        p += in[i] + 32;
      else
        p += in[i];
    }
    print.push_back(p);
  }
  for (int i = 0; i < print.size(); i++) {
    if (i == 0)
      cout << print[i];
    else
      cout << " " << print[i];
  }
  cout << endl;
  return 0;
}
