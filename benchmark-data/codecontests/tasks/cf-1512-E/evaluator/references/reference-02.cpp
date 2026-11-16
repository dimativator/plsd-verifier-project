#include<iostream>
#include<map>
#include<cstring>
using namespace std;
typedef long long ll;
map<int,int>mp;
int an[210210];
int ans[210200];
int main(){
	int T;
	cin>>T;
	for(int i=1;i<=600;i++)an[i]=i;
	while(T--){
		memset(ans,0,sizeof ans);
		mp.clear();
		int n,a,b,s;
		cin>>n>>a>>b>>s;
		int num=b-a+1;
		int minn=0,maxx=0;
		for(int i=1;i<=num;i++){
			minn+=an[i];
		}
		for(int i=n-num+1;i<=n;i++){
			maxx+=an[i];
		}
		if(s<minn||s>maxx){
			printf("-1\n");
			continue;
		}
		int di=s-minn;
		int kk=n-num;
		for(int i=a,j=num;i<=b;i++,j--){
			int u=kk;
			ans[i]=j;
			if(di)
			for(int pp=1;pp<=kk;pp++){
				ans[i]++;
				di--;
				if(di==0)break;
			}
			mp[ans[i]]++;
		}
		for(int i=1;i<=n;i++){
			if(ans[i]==0){
				int uu=0;
				for(int i=1;i<=n;i++){
					if(!mp[i]){
						mp[i]=1;
						uu=i;
						break;
					}
				}
				ans[i]=uu;
			}
		}
		for(int i=1;i<=n;i++){
			printf("%d ",ans[i]);
		}
		printf("\n");
	}
}