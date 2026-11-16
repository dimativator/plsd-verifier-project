#include <bits/stdc++.h>
using namespace std;
vector<long long> zero, one, two;
map<long long, long long> mp, mp1;
int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);
  cout.tie(NULL);
  ;
  long long n, i, j, flag = 0;
  cin >> n;
  long long a[n + 5];
  for (i = 0; i < n; i++) {
    cin >> a[i];
    if (a[i] != 0) {
      mp[i + 1] = a[i];
      mp1[a[i]] = i + 1;
    }
  }
  for (i = 1; i <= n; i++) {
    if (mp[i] != 0 && mp1[i] != 0) {
    } else if (mp[i] != 0 && mp1[i] == 0) {
      two.push_back(i);
    } else if (mp[i] == 0 && mp1[i] != 0) {
      one.push_back(i);
    } else {
      zero.push_back(i);
    }
  }
  i = 0;
  if (zero.size() >= 2) {
    long long start = zero[i];
    for (i = 0; i < zero.size(); i++) {
      if (i == zero.size() - 1) {
        mp[zero[i]] = start;
        mp1[start] = zero[i];
        i++;
        break;
      }
      mp[zero[i]] = zero[i + 1];
      mp1[zero[i + 1]] = zero[i];
    }
  }
  for (; i < zero.size(); i++) {
    if (two.empty() == false && one.empty() == false) {
      mp[zero[i]] = two.back();
      mp1[two.back()] = zero[i];
      two.pop_back();
      mp1[zero[i]] = one.back();
      mp[one.back()] = zero[i];
      one.pop_back();
    }
  }
  for (i = 0; i < one.size(); i++) {
    mp[one[i]] = two[i];
    mp1[two[i]] = one[i];
  }
  for (i = 0; i < n; i++) {
    cout << mp[i + 1] << " ";
  }
}
