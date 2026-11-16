#include <bits/stdc++.h>
using namespace std;
struct DP {
  pair<int, int> five, two;
  bool invalid;
} dp[1001][1001];
long long arr[1001][1001], two[1001][1001], five[1001][1001];
int main() {
  ios_base::sync_with_stdio(0);
  int n;
  cin >> n;
  bool zero = false;
  pair<int, int> idx_zero;
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < n; ++j) {
      cin >> arr[i][j];
      if (arr[i][j] == 0) {
        idx_zero = pair<int, int>(i, j);
        zero = true;
      }
    }
  }
  int temp;
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < n; ++j) {
      temp = arr[i][j];
      if (arr[i][j] == 0) continue;
      while (temp % 2 == 0) {
        temp /= 2;
        two[i][j]++;
      }
      while (temp % 5 == 0) {
        temp /= 5;
        five[i][j]++;
      }
    }
  }
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < n; ++j) {
      if (arr[i][j] == 0) {
        dp[i][j].invalid = true;
        continue;
      }
      if (i == 0) {
        if (j == 0) {
          dp[i][j].five = pair<int, int>(0, five[0][0]);
          dp[i][j].two = pair<int, int>(0, two[0][0]);
        } else {
          dp[i][j].invalid = dp[i][j - 1].invalid;
          dp[i][j].five =
              pair<int, int>(0, dp[i][j - 1].five.second + five[i][j]);
          dp[i][j].two = pair<int, int>(0, dp[i][j - 1].two.second + two[i][j]);
        }
      } else {
        if (j == 0) {
          dp[i][j].invalid = dp[i - 1][j].invalid;
          dp[i][j].five =
              pair<int, int>(1, dp[i - 1][j].five.second + five[i][j]);
          dp[i][j].two = pair<int, int>(1, dp[i - 1][j].two.second + two[i][j]);
        } else {
          dp[i][j].invalid = (dp[i - 1][j].invalid && dp[i][j - 1].invalid);
          if (dp[i][j].invalid) continue;
          dp[i][j].five.second = 1000000000;
          dp[i][j].two.second = 1000000000;
          if (!dp[i - 1][j].invalid) {
            dp[i][j].five = pair<int, int>(1, dp[i - 1][j].five.second);
            dp[i][j].two = pair<int, int>(1, dp[i - 1][j].two.second);
          }
          if (!dp[i][j - 1].invalid) {
            if (dp[i][j - 1].five.second < dp[i][j].five.second)
              dp[i][j].five = pair<int, int>(0, dp[i][j - 1].five.second);
            if (dp[i][j - 1].two.second < dp[i][j].two.second)
              dp[i][j].two = pair<int, int>(0, dp[i][j - 1].two.second);
          }
          dp[i][j].five.second += five[i][j];
          dp[i][j].two.second += two[i][j];
        }
      }
    }
  }
  if (dp[n - 1][n - 1].invalid == true) {
    cout << 1 << "\n";
    int dx = idx_zero.first, dy = idx_zero.second;
    for (int r = 0; r < dx; ++r) cout << "D";
    for (int c = 0; c < n - 1; ++c) cout << "R";
    for (int r = dx; r < n - 1; ++r) cout << "D";
    return 0;
  }
  int ans = min(dp[n - 1][n - 1].two.second, dp[n - 1][n - 1].five.second);
  if (zero == true and ans >= 1) {
    cout << 1 << "\n";
    int dx = idx_zero.first, dy = idx_zero.second;
    for (int r = 0; r < dx; ++r) cout << "D";
    for (int c = 0; c < n - 1; ++c) cout << "R";
    for (int r = dx; r < n - 1; ++r) cout << "D";
    return 0;
  }
  cout << ans << "\n";
  int min_path;
  if (dp[n - 1][n - 1].two.second < dp[n - 1][n - 1].five.second)
    min_path = 2;
  else
    min_path = 5;
  string str;
  int row = n - 1, col = n - 1;
  while (1) {
    if (row == 0 and col == 0) break;
    if (min_path == 5) {
      if (dp[row][col].five.first == 1) {
        str += "D";
        row--;
      } else {
        str += "R";
        col--;
      }
    } else {
      if (dp[row][col].two.first == 1) {
        str += "D";
        row--;
      } else {
        str += "R";
        col--;
      }
    }
  }
  reverse(str.begin(), str.end());
  cout << str;
  return 0;
}
