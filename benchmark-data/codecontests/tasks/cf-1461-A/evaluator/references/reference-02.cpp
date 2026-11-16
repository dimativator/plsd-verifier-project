#include <bits/stdc++.h>
using namespace std;
int main()
{
     ios_base :: sync_with_stdio(false); cin.tie(NULL);
     int t ; cin >> t ; while(t--)
     {
         int a , b ; cin >> a >> b ;
   a-=b ;
   while(b--) cout << 'a' ;
   string d = "cba" ;
   for(int i = 0 ; i < a ; i++)
   {
       cout << d[i % 3] ;
   }
   cout << endl ;
     }

}




