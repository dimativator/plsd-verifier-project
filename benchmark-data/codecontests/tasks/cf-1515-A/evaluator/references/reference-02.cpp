#include <bits/stdc++.h>
using namespace std;
int main()
{
    int n;
    cin >> n;
    while (n--)
    {
        long long int a, x, s = 0, d = 0, k;
        cin >> a >> x;
        int arr[a];
        for (int i = 0; i < a; i++)
        {
            cin >> arr[i];
            s = s + arr[i];
        }
        if (s == x)
            cout << "NO" << endl;
        else
        {
            s = 0;
            d = 0;
            cout << "YES" << endl;
            for (int i = 0; i < a; i++)
            {
                if (s + arr[i] == x)
                    d = arr[i];
                else
                {
                    cout << arr[i] << " ";
                    s = s + arr[i];
                }
                if (d != 0&&s+d!=x)
                {
                    cout << d << " ";
                    s = s + d;
                    d=0;
                }
                
            }
            cout<<endl;
        }
    }
    return 0;
}