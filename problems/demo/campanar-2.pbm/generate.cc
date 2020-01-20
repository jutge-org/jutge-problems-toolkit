#include <iostream>
#include <cstdlib>

using namespace std;

int main (int argc, char** argv) {
    int n = atoi(argv[1]);  // nombre linies
    int m = atoi(argv[2]);  // modul del nombre de minuts
    while (n--) {
        cout << rand()%24 << " " << rand()%60 << " " << rand()%m << endl;
    } 
}
