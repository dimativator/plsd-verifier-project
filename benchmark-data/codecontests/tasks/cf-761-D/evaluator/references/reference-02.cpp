#include <bits/stdc++.h>
void probs();
int main() {
  probs();
  return 0;
}
void probs() {
  int n, l, r, *a, *b;
  scanf("%d%d%d", &n, &l, &r);
  int k, max;
  a = (int*)malloc(n * sizeof(int));
  b = (int*)malloc(n * sizeof(int));
  for (int i = 0; i < n; i++) scanf("%d", &a[i]);
  for (int i = 0; i < n; i++) {
    scanf("%d", &b[i]);
    b[i] = a[i] + b[i];
  }
  max = b[0];
  for (int i = 1; i < n; i++) {
    if (b[i] > max) max = b[i];
  }
  k = max - r;
  for (int i = 0; i < n; i++) {
    b[i] -= k;
    if (b[i] < l) {
      printf("%d", -1);
      return;
    }
  }
  for (int i = 0; i < n; i++) printf("%d ", b[i]);
  free(a);
  free(b);
}
