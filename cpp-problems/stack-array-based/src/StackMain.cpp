#include <iostream>
#include <string>
#include "Stack.h"

// Given an expression (postfix notation) from strings. 
// Compute the expression (using Stack) and output its value.
using namespace std;
int main() {
    // Expression 2*(17-1)+3*4
    string ss[] = {"2", "17", "1", "-", "*", "3", "4", "*", "+"};

    Stack stack(10);
    for (int i = 0; i < 9; i++) {
        if (ss[i] == "+") {
            int op2 = stack.pop();
            int op1 = stack.pop();
            stack.push(op1 + op2);
        }
        else if (ss[i] == "-") {
            int op2 = stack.pop();
            int op1 = stack.pop();
            stack.push(op1 - op2);
        }
        else if (ss[i] == "*") {
            int op2 = stack.pop();
            int op1 = stack.pop();
            stack.push(op1 * op2);
        }
        else {
            int a = stoi(ss[i]);
            stack.push(a);
        }
    }
    cout << stack.top() << endl;
}