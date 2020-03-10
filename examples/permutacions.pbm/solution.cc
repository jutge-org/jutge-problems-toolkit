#include <iostream>
#include <string>
#include <vector>
using namespace std;


typedef vector<int> VE;
typedef vector<string> VS;


void escriu(int i, int n, VE& v, VE& usat, const VS& s) {
  if (i == n) {
    cout << '(';
    for (int j = 0; j < n - 1; ++j) cout << s[v[j]] << ',';
    cout << s[v[n - 1]] << ')' << endl;
    return;
  }

  for (int j = 0; j < n; ++j)
    if (not usat[j]) {
      v[i] = j;
      usat[j] = true;
      escriu(i + 1, n, v, usat, s);
      usat[j] = false;
    }
}


int main() {
  int n;
  cin >> n;
  VS s(n);
  for (int i = 0; i < n; ++i) cin >> s[i];
  VE v(n), usat(n, false);
  escriu(0, n, v, usat, s);
}
