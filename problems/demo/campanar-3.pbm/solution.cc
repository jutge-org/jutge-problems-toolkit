#include <iostream>
using namespace std;


int main () {
    int h, m;
    
    while (cin >> h >> m) {
        if (h >= 12) h -= 12;
        
        if (h==0 and m==0) {
            cout << "12 0" << endl;
        } else if (h==0) {
            if (m<=15) {
                cout << "7 " << 105-m << endl;
            } else if (m<=30) {
                cout << "8 " << 120-m << endl;
            } else if (m<=45) {
                cout << "7 " << 120-m << endl;
            } else {
                cout << "6 " << 120-m << endl;
            }
        } else if (h==1 and m==0) {
            cout << "6 60" << endl;            
        } else {
            if (m==0) {
                cout << h << " 0" << endl;
            } else {
                int c = 0;
                if (m <= 15) ++c;
                if (m <= 30) ++c;
                if (m <= 45) ++c;
                c += h+1;
                cout << c << " " << 60-m << endl;
            }
        }
    }
}
