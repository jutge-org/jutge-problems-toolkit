#include <iostream>
using namespace std;

int main () {
    for (int h=1; h<=12; ++h) {
        for (int m=0; m<60; m+=15) {
            cout << h << ":" << m << " " <<  (m==0 ? h : 1) << endl;
        }
    } 
    for (int h=1; h<=12; ++h) {
        for (int m=0; m<60; m+=15) {
            cout << h << ":" << m << " " <<  (m==0 ? h : 1) << endl;
        }
    } 
}
