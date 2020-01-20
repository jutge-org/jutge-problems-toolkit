#include <vector>
#include <string>
using namespace std;


struct Estudiant {
    int dni;
    string nom;
    double nota;
    bool repetidor;
};


const double NP = -1;


void informacio(const vector<Estudiant>& es, double& min, double& max, double& mitj) {
    min = 11;
    max = 0;
    double sum = 0;  
    int cnt = 0;

    for (int i = 0; i < es.size(); ++i) {
        double x = es[i].nota;
        if (not es[i].repetidor and x != NP) {
            ++cnt;
            sum += x;
            if (x < min) min = x;
            if (x > max) max = x;
        }
    }
    if (cnt==0) {
        min = max = mitj = -1;
    } else {
        mitj = sum / cnt;
    }
}
