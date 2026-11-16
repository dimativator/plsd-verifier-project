#include <bits/stdc++.h>
const int N=200005;
struct note{
	int x,y;
}opt[N];
int t[N],a[N],n,cnt,vis[N],ed[N],s[N],tot,siz[N];
void Swap(int x,int y){
	opt[++tot]={x,y};
	std::swap(a[x],a[y]); 
}
void solve(int x){
	int nn=0;
	for (int i=a[x];i!=x;i=a[i])
		t[++nn]=i;
	for (int i=1;i<=nn;i++)
		Swap(t[i],x);
}
void merge(int x,int y){
	Swap(x,y);
	Swap(a[x],a[y]);
	solve(a[x]),solve(a[y]);
}
int main(){
	scanf("%d",&n);
	for (int i=1;i<=n;i++) scanf("%d",&a[i]);
	for (int i=1;i<=n;i++){
		if (vis[i] || a[i]==i) continue;
		s[++cnt]=i;
		for (int x=i;!vis[x];x=a[x])
			vis[x]=i,ed[cnt]=x,siz[cnt]++;
	}
	for (int i=1;i<cnt;i+=2)
		merge(s[i],s[i+1]);
	if (cnt&1){
		if (siz[cnt]==2){
			int i=1;
			while (vis[i]==cnt) i++;
			int v1=s[cnt],v2=ed[cnt];
			Swap(v1,i);
			Swap(i,v2);
			Swap(v1,i);	
		}else{
			int v1=s[cnt],v2=a[s[cnt]],vm=ed[cnt];
			Swap(v1,v2),Swap(v2,vm);
			solve(v1); 	
		}
	}
	printf("%d\n",tot);
	for (int i=1;i<=tot;i++) printf("%d %d\n",opt[i].x,opt[i].y);
}