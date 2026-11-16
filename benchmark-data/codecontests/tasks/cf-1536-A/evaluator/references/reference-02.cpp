#include<bits/stdc++.h>
typedef int LL;
typedef double dl;
#define opt operator
#define pb push_back
#define pii std::pair<LL,LL>
const LL maxn=1e6+9,mod=998244353,inf=0x3f3f3f3f;
LL Read(){
	LL x(0),f(1); char c=getchar();
	while(c<'0' || c>'9'){
		if(c=='-') f=-1; c=getchar();
	}
	while(c>='0' && c<='9'){
		x=(x<<3ll)+(x<<1ll)+c-'0'; c=getchar();
	}return x*f;
}
void Chkmin(LL &x,LL y){
	if(y<x) x=y;
}
void Chkmax(LL &x,LL y){
	if(y>x) x=y;
}
LL add(LL x,LL y){
	return x+=y,x>=mod?x-mod:x;
}
LL dec(LL x,LL y){
	return x-=y,x<0?x+mod:x;
}
LL mul(LL x,LL y){
	return 1ll*x*y%mod;
}
LL Pow(LL base,LL b){
	LL ret(1); while(b){
		if(b&1) ret=mul(ret,base); base=mul(base,base); b>>=1;
	}return ret;
}
LL T,n;
LL a[maxn];
void Init(){
	n=Read();
	for(LL i=1;i<=n;++i) a[i]=Read();
}
void Solve(){
	LL flag(0);
	for(LL i=1;i<=n;++i) flag|=(a[i]<0);
	if(flag){
		puts("NO");
		return;
	}
	while(true && n<=300){
		static LL vis[200];
		for(LL i=1;i<=n;++i) if(a[i]>=0) vis[a[i]]=1;
		static LL b[maxn];
		LL m(0);
		for(LL i=1;i<=n;++i){
			for(LL j=i+1;j<=n;++j){
				LL x(std::abs(a[i]-a[j]));
				if(!vis[x]){
					b[++m]=x;
					vis[x]=1;
				}
			}
		}
		for(LL i=1;i<=m;++i) a[++n]=b[i];
		for(LL i=1;i<=n;++i) vis[a[i]]=0;
		if(!m){
			break;
		}
	}
	if(n<=300){
		puts("YES");
		printf("%d\n",n);
		for(LL i=1;i<=n;++i) printf("%d ",a[i]); puts("");
	}else puts("NO");
}
int main(){
//	freopen("y1.txt","r",stdin);
	T=Read();
	while(T--){
		Init();
		Solve();
	}
	return 0;
}



