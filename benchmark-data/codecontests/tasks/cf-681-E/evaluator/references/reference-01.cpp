#include <bits/stdc++.h>
using namespace std;
struct debugger {
  template <typename T>
  debugger& operator,(const T& v) {
    cerr << v << " ";
    return *this;
  }
} dbg;
struct circle {
  double x, y, r, a1, a2, d;
} cir[100010];
bool cmp(circle c1, circle c2) {
  if (c1.a1 == c2.a1) {
    if (c1.a2 == c2.a2) return c1.d < c2.d;
    return c1.a2 < c2.a2;
  }
  return c1.a1 < c2.a1;
}
int main() {
  double x0, y0, v, T;
  while (scanf("%lf %lf %lf %lf", &x0, &y0, &v, &T) == 4) {
    double R = v * T;
    int n, c = 0, f = 0;
    scanf("%d", &n);
    vector<pair<double, double> > thetas;
    int k = 0;
    for (int i = 0; i < n; i++) {
      double x1, y1, r;
      scanf("%lf %lf %lf", &x1, &y1, &r);
      x1 -= x0;
      y1 -= y0;
      if (x1 * x1 + y1 * y1 <= r * r) f = 1;
      double dis = sqrt(x1 * x1 + y1 * y1);
      if (dis < (r + R)) {
        double theta = atan2(y1, x1);
        double DS = sqrt(x1 * x1 + y1 * y1 - r * r);
        double phi;
        if (DS <= R)
          phi = asin(r / dis);
        else {
          phi = acos((dis * dis + R * R - r * r) / (2.0 * dis * R));
        }
        theta -= phi;
        phi = theta + phi * 2.0;
        if (theta < -acos(-1.0))
          thetas.push_back({theta + 2.0 * acos(-1.0), acos(-1.0)}),
              theta = -acos(-1.0);
        if (phi > acos(-1.0))
          thetas.push_back({-acos(-1.0), phi - 2.0 * acos(-1.0)}),
              phi = acos(-1.0);
        thetas.push_back({theta, phi});
      }
    }
    double ans;
    if (f)
      ans = 1.0;
    else {
      sort(thetas.begin(), thetas.end());
      double ang = 0.0;
      double b1 = -500.0, b2 = 0.0;
      for (int i = 0; i < (int)thetas.size(); i++) {
        if (b1 < thetas[i].first) b1 = thetas[i].first;
        if (thetas[i].second > b1) {
          ang += thetas[i].second - b1;
          b1 = thetas[i].second;
        }
      }
      ans = ang / (2.0 * acos(-1.0));
      ans = min(1.0, ans);
    }
    printf("%.15lf\n", ans);
  }
  return 0;
}
