#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const int mod =  1000000007;

int t, n;
string s;
int ans[20];

int main () 
{
    cin >> t;
    while (t--) {
        cin >> n;
        if (n > 45) {
            puts("-1");
        } else {
            int pos = 0;
            for (int i = 9; i >= 1; --i) {
                if (n > i) {
                    ans[pos++] = i;
                    n -= i;
                } else if (n == i) {
                    ans[pos++] = i;
                    break;
                }
            }
            for (int i = pos - 1; i >= 0; --i) {
                cout << ans[i];
            }
            cout << endl;    
        }
        
    }
    
    return 0;
}