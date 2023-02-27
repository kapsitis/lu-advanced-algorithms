#include <iostream>
using namespace std;

void hanoi(int n, char source, char dest, char temp) {
    if (n == 1) {
        cout << "Move disk 1 from " << source << " to " << dest << endl;
        return;
    }
    hanoi(n-1, source, temp, dest);
    cout << "Move disk " << n << " from " << source << " to " << dest << endl;
    hanoi(n-1, temp, dest, source);
}

int main() {
    int n = 3; // Number of disks
    hanoi(n, 'A', 'C', 'B');
    return 0;
}
