#include <algorithm>
#include <iostream>
#include <cstring>
#include <ctime>

#define end cout<<endl
#define lo long long 
int size;
#define forx for(int i=0;i<size;i++)
#define fast ios_base::sync_with_stdio(0),cin.tie(0),cout.tie(0);
using namespace std;
int main () 
{
	fast
	cin>>size;
	size=size%9;
	if(size==0)
	size=9;
	cout<<size;
	
}