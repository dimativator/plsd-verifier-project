#include <bits/stdc++.h>
//#include <atcoder/all>
#define int long long
#define rep(i,a) for (int i = 0; i < (a); i++ )
#define Rep(i,start,a) for (int i = start; i < (a); i++ )
#define ALL(vec) (vec).begin(), (vec).end()
#define Sort(vec) sort((vec).begin(), (vec).end()) // 小さい順
#define SORT(vec) sort((vec).begin(), (vec).end(), [](auto a, auto b){return a>b;}) // 大きい順
#define SORTll(vec) sort((vec).begin(), (vec).end(), [](long long a, long long b){return a>b;}) // 大きい順
#define debug(x) cerr << #x << " = " << (x) << endl
#define Bit(s,k) (s>>k)&1
#define VI vector<int>
#define VLL vector<long long>
#define PII pair<int,int>
#define VPII vector<PII>
#define VB vector<bool>
#define VVI vector<vector<int>>
#define VVVI vector<vector<vector<int>>>
#define Graph vector<vector<int>>
#define PB emplace_back
#define USI unordered_set<int>
#define Maze vector<string>
#define Pqueue priority_queue
#define MP make_pair
#define WeightedGraph vector<vector<pair<int,ll>>> // parent, (to, cost)
//#define mat vector<vector<long long>>

#define vecdebug(vec) {cerr << #vec << " = [" ; for(auto x : (vec)){cerr << (x) << ", ";} cerr << "]" << endl; }
#define vdebug(vec,i) cerr << #vec << "[" << (i) << "] = " << (vec)[(i)] << endl
#define vvdebug(vec,i,j) cerr << #vec << "[" << (i) << "][" << (j) << "] = " << (vec)[(i)][(j)] << endl
#define vvvdebug(vec,i,j,k) cerr << #vec << "[" << (i) << "][" << (j) << "][" << (k) <<"] = " << (vec)[(i)][(j)][(k)] << endl
#define pdebug(p) cerr << #p << " = [" << (p).first << ", " << (p).second << "]" << endl

typedef long long ll;
typedef long double ld;

const ll mod = 998244353;
const ll MOD = 1000000007;
const ll INFLL = (1LL << 62) -1;
const int INF = (1 << 30) -1;
const int dx[4] = {1, 0, -1, 0};
const int dy[4] = {0, 1, 0, -1};
const long double pi = 2*asin(1);

using namespace std;
//using namespace atcoder;

//using mint = modint1000000007;
//using mint = modint998244353;
//using mint = modint998244353;
//using mint = static_modint<7>;


template<typename T>
inline void chmin(T &x, T y){
  if(x>y) x=y;
}

template<typename T>
inline void chmax(T &x, T y){
  if(x<y) x=y;
}

inline int tonum(char X){
  return (int)(X-'a');
}

inline int ctoi(char x){
  return (int)(x-'0');
}

int Max(int x, int y){
  if(x>y) return x;
  return y;
}

int Min(int x, int y){
  if(x<y) return x;
  return y;
}

inline int tochar(int n){
  return (char)('a' + n);
}

inline int ABS(int n){
  if(n<0) return -n;
  return n;
}


ll GCD(ll a, ll b){
  if(a%b==0) return b;
  return GCD(b,a%b);
}

ll LCM(ll a, ll b){
  return a / GCD(a,b) *b;
}


set<int> bit(int n){
  set<int> ret;
  int m = n;
  rep(i,70){
    if(m&1) ret.insert(i);
    m >>= 1;
  }
  return ret;
}

void solve(){
  int n; cin >> n;
  VI a(n); rep(i,n) cin >> a[i];

  int m = INF;
  int ind = -1;
  rep(i,n){
    if(m > a[i]){
      ind = i;
      m = a[i];
    }
  }

  VI ans;

  Rep(i,ind,n-1){
    if(GCD(a[i], a[i+1]) > 1){
      a[i+1] = MOD;
      ans.PB(i+2);
    }
  }

  for(int i = ind; i > 0; i--){
    if(GCD(a[i], a[i-1]) > 1){
      a[i-1] = MOD;
      ans.PB(i);
    }
  }

  cout << ans.size() << endl;
  for(int k : ans){
    cout << 1+ind << " " << k << " " << a[ind] << " " << MOD << endl;
  }
}

signed main(){
  cin.tie(nullptr);
  ios::sync_with_stdio(false);
  cout << fixed << setprecision(16);

  
  int t; cin >> t;
  rep(i,t) solve();
}