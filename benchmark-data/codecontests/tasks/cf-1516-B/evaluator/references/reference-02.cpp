#include<bits/stdc++.h>
using namespace std;
long long a[2005];
long long n;

void work(){
	long long temp1 = 0,temp2;
	for(int i=n;i>=1;i--){
		temp1 = temp1 xor a[i];
		temp2 = 0;
		for(int j=i-1;j>=1;j--){
			temp2 = temp2 xor a[j];
			if(temp1 == temp2){
				if(j == 1){
					puts("YES");
					return;
				}
				temp2 = 0;
			}	
		}
	}
	puts("NO");
	return;
}

int main(){
	int T;	
	cin>>T;
	while(T--){
		scanf("%lld",&n);
		for(int i=1;i<=n;i++)
			scanf("%lld",&a[i]);
		work();
	}
}