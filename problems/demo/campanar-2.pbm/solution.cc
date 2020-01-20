#include <iostream>
using namespace std;


/* 
    Les busques es creuen a les:
       00 00 00
       01 05 27
       02 10 55
       03 16 22
       04 21 49
       05 27 16
       06 32 44
       07 38 11
       08 43 38
       09 49 05
       10 54 33
       12 00 00
*/


int tocs (int h, int m, int l) {
    int n = (l/(24*60))*22;
    l %= 24*60;
    while (l!=0) {
        if (h%12== 0 and m== 0) ++n;
        if (h%12== 1 and m== 5) ++n;
        if (h%12== 2 and m==10) ++n;
        if (h%12== 3 and m==16) ++n;
        if (h%12== 4 and m==21) ++n;
        if (h%12== 5 and m==27) ++n;
        if (h%12== 6 and m==32) ++n;
        if (h%12== 7 and m==38) ++n;
        if (h%12== 8 and m==43) ++n;
        if (h%12== 9 and m==49) ++n;
        if (h%12==10 and m==54) ++n;
        --l;
        if (++m==60) {
            m = 0;
            if (++h==24) {
                h = 0;
    }   }   }        
    return n;
}


int main() {
    int h, m, l;    
    while (cin >> h >> m >> l) {
        cout << tocs(h,m,l) << endl;
}   }

