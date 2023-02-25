#include <iostream>
#include <string>

void eraseChars(char* arg) {
    int left = 0; 
    int right = 0;
    // state = 0: default/initial state - keep current char; proceed left.
    // state = 1: currently moving forward 
    int state = 0; 

    while (arg[left] != '\0') {
        if (state == 0) {
            if (arg[left] < 'A' || arg[left] > 'Z' || (left > 0 && arg[left-1] < arg[left])) {
                left++;
                state = 0; 
            }
            else {
                right = left + 1;
                state = 1;                 
            }
        }
        else if (state == 1) {
            if (arg[left] < 'A' || arg[left] > 'Z') {
                
            }
        }
    }
}

using namespace std;
int main() {
    string line; 
    while(getline(cin, line)) {
        if (line == "") {
            break;
        }
        cout << line << endl;
        
    }
}
