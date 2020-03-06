#include <iostream>
#include <cstdlib>

using namespace std;

int main () {
    for (int i=0; i<100000; ++i) {
        cout << rand()%24 << " " << rand()%60 << " " << rand()%100000000 << endl;
    }
}
