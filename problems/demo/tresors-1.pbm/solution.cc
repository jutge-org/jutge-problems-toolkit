#include <iostream>
#include <vector>
using namespace std;


typedef vector<char> VC;
typedef vector<VC> VVC;
typedef vector<bool> VB;
typedef vector<VB> VVB;


bool busca(int f, int c, int n, int m, const VVC& mapa, VVB& vist) {
  if (f < 0 or f >= n or c < 0 or c >= m or vist[f][c]) return false;

  vist[f][c] = true;
  if (mapa[f][c] == 't') return true;
  if (mapa[f][c] == 'X') return false;

  return    busca(f + 1, c, n, m, mapa, vist)
         or busca(f - 1, c, n, m, mapa, vist)
         or busca(f, c + 1, n, m, mapa, vist)
         or busca(f, c - 1, n, m, mapa, vist);
}


int main() {
  int n, m;
  cin >> n >> m;
  VVC mapa(n, VC(m));
  for (int i = 0; i < n; ++i)
    for (int j = 0; j < m; ++j) cin >> mapa[i][j];
  int f, c;
  cin >> f >> c;

  VVB vist(n, VB(m, false));
  if (busca(f - 1, c - 1, n, m, mapa, vist)) cout << "1" << endl;
  else cout << "0" << endl;
}
