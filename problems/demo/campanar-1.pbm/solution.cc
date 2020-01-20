#include <iostream>
using namespace std;


int main() {
    int h,m,l;
    while (cin >> h >> m >> l) {
    
        int c = 0;
        while (l--) {
            if (m==0) {
                c += 4;
                if (h==12)      c += 100;
                else if (h==0)  c += 12;
                else if (h<12)  c += h;
                else            c += h - 12;
            } else if (m==15)   c += 1;
              else if (m==30)   c += 2;
              else if (m==45)   c += 3;
            if (++m==60) {
                m = 0;
                if (++h==24) {
                    h = 0;
                        c += 484*(l/1440);
                        l = l % 1440; 
        }   }   }                
        cout << c << endl;
}   }    

//    484 és el nombre de campanades desde les 0:0 fins a les 23:59. 1440 és 24*60.
