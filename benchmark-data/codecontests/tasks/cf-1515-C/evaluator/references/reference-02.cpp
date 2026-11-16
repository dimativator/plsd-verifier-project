#include <bits/stdc++.h>
using namespace std;
#define debug(...) fprintf(stderr, __VA_ARGS__), fflush(stderr)
typedef long long int ll;
typedef long double ld;
#define trump(v,a) vector<ll> v(a); for(int i =0;i<a; ++i)cin>>v[i];
#define modi(v) for(auto i:v){ cout<<i<<" ";}cout<<endl;;
#define debug_pair(obg) for(auto i:obg) cerr<<i.F<<" "<<i.S<<endl;
#define modibaap(v) for(auto i :v){modi(i);};
#define F first
#define S second
#define p2 pair<ll,ll>


void solve() {
	ll a = 1, b = 0, c = 0, t = 0, ans = 0, ans2 = 0, k = -1, c1 = 0, c2 = 0, c3 = 0, c4 = 0 , n = 0, m = 0, x = 1e18;
	cin >> a >> b >> c;
	trump(v, a);
	std::vector<p2> y;
	// sort(v.rbegin(), v.rend());
	for (int i = 0; i < a; ++i)
	{
		/* code */
		y.push_back({v[i], i});
	}
	sort(y.rbegin(), y.rend());
	multiset<p2> mu;
	std::vector<ll> an(a);
	for (int i = 0; i < b; ++i)
	{
		/* code */
		mu.insert({y[i].F, i + 1});
		an[y[i].S] = i + 1;
	}
	for (int i = b; i < a; ++i)
	{
		/* code */
		auto tt = mu.begin();
		auto u = *tt;
		mu.erase(tt);
		an[y[i].S] = u.S;
		mu.insert({u.F + y[i].F, u.S});
	}
	std::vector<ll> uuu;

	for (auto i : mu) {
		uuu.push_back(i.F);
	}
	for (int i = 0; i < b - 1; ++i)
	{
		/* code */
		if (uuu[i + 1] - uuu[i] > c) {
			cout << "NO\n";
			return;
		}
	}
	cout << "YES\n";
	modi(an);
}


int main() {
	ios_base::sync_with_stdio(false);
	cin.tie(NULL);
	cout.tie(NULL);

#ifndef ONLINE_JUDGE
	freopen("input.txt", "r", stdin);
	freopen("output.txt", "w", stdout);
#endif

	clock_t z = clock();
	ll qc = 1, additionalv;
	cin >> qc;

	for (ll i = 1; i <= qc; i++) {
		// cout << "Case #" << i  << ": ";

		solve();
	}
	debug("Real Time: % .4Lf\n", (ld)(clock() - z) / CLOCKS_PER_SEC);
}

/*
some good points to think :-
1) Why are you alive
2) Is the array overflowing
3) will you ever be able to solve a graph question. YAY!!
3.a)Will you ever be able to solve a segment tree question.
4) The answer will be trivial always if its not its not worth solving
5) for xor a^b  = a+b-2a&b xor of multi element set counts only odd no. of set bits
6) char values are '0' =48 'a' = 97 'A' = 65
7) two pointers are good way for array sum /length based questions
8) dp on sums?
9) make black boxes
10) min/max at central tendencies and just iterate +- 5 around it.
11) prime factorisation by linear sieve + recursion.
12) for satisfiability see range of the variable.
13) never define endl fucks interactive
14) to_string(num) => str(int)+9
*/