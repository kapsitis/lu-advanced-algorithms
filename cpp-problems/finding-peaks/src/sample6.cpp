#include <iostream>
#include <string>

using namespace std;
struct StrInt { string s; int a; };

void printStrInt(StrInt arg) {
    cout << "(" << arg.s << "," << arg.a << ")";
}

static int numOfCompareCalls = 0;
// This function should return 0, if both structs are equal
// It should return a negative number, if the struct "A" is less than "B"
// It should return a positive number, if "A" is more than "B"
int compare(StrInt A, StrInt B) {
    numOfCompareCalls++;
    int strComparison = A.s.compare(B.s);
    if (strComparison == 0) {
        return A.a - B.a;
    }
    else {
        return strComparison; 
    }
}



int findPeak(StrInt* arr, int left, int right) {
    if (right - left <= 1) {        
        return left;
    }
    else {
        int middle = left + (right-left)/2; 
        if (compare(arr[middle-1], arr[middle]) > 0) {
            return findPeak(arr, left, middle-1);
        }
        else {
            return findPeak(arr,middle, right);
        }
    }
}


// Your implementation of main()
int main() {
    int N; 
    cin >> N; 
    StrInt* arr = new StrInt[N];
    for (int i = 0; i < N; i++) {
        cin >> arr[i].s;
        cin >> arr[i].a;
    }
    int index = findPeak(arr, 0, N);
    cout << "PeakLocation " << index << endl;
    cout << "PeakValue "; 
    printStrInt(arr[index]);
    cout << endl;
    cout << "Comparisons " << numOfCompareCalls << endl;
}