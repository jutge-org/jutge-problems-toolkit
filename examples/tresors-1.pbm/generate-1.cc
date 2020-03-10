#include "atzar.cc"
#include <iostream>
#include <vector>
using namespace std;


atzar A(0);


int main() {
  int n = A.uniforme(1, 100);
  int m = A.uniforme(1, 100);
  cout << n << ' ' << m << endl;

  int x = A.uniforme(1, n);
  int y = A.uniforme(1, m);

  for (int i = 1; i <= n; ++i) {
    for (int j = 1; j <= m; ++j)
      if ((i == x and j == y) or A.probabilitat(0.6)) cout << '.';
      else cout << (A.probabilitat(0.04) ? 't' : 'X');
    cout << endl;
  }

  cout << x << ' ' << y << endl;
}
