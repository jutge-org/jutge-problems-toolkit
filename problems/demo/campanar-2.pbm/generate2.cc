#include <iostream>
#include <cstdlib>

using namespace std;

int main () {
    for (int h=0; h<12; ++h) {
        for (int m=0; m<60; ++m) {
            for (int l=0; l<=24*60; ++l) if (rand()%1024<100) {
                cout << h << " " << m << " " << l << endl;
}   }   }   }

