#include <iostream>
#include <string>
#include <vector>
using namespace std;


typedef vector<string> VS;
typedef vector<bool> VB;


int n;
VS S;
VB B;


void escriu(int i) {
  if (i == n) {
    cout << '{';
    bool primer = true;
    for (int j = 0; j < n; ++j)
      if (B[j]) {
        if (primer) primer = false;
        else cout << ',';
        cout << S[j];
      }
    cout << '}' << endl;
    return;
  }

  B[i] = false;
  escriu(i + 1);
  B[i] = true;
  escriu(i + 1);
}


int main() {
  cin >> n;
  S = VS(n);
  for (int i = 0; i < n; ++i) cin >> S[i];
  B = VB(n);
  escriu(0);
}
