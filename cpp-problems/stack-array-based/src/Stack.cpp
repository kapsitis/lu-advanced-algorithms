#include <iostream>
#include "Stack.h"

using namespace std;
Stack::Stack(int maxSize) {
    this->maxSize = maxSize;
    items = new int[maxSize];
    current = 0;
}

void Stack::push(int item) {
    if (current < maxSize) {
        items[current++] = item;
    } else {
        throw out_of_range("push(item) failed: Exceeded maxSize");
    }
}

int Stack::pop() {
    if (current > 0) {
        return items[--current]; 
    } else {
        throw out_of_range("pop() failed: Stack is empty");
    }
}

int Stack::top() {
    if (current > 0) {
        return items[current-1];
    } else {
        throw out_of_range("top() failed: Stack is empty");
    }
}

// void Stack::output() {
//     cout << "["; 
//     for (int i = 0; i < current; i++) {
//         cout << items[i] << " "; 
//     }
//     cout << "]" << endl;
// }


