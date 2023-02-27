#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <vector>
#include<algorithm>
#include <fstream>
#include <sstream>
#include "CircularList.h"

using namespace ds_course;
using namespace std;

int main(){
    //cout << "I am here";

    CircularList myList;

    int howMany = 0;
    cin >> howMany;
    if(howMany == 0){
        myList.emptyFromTheBeginning();
    }
    //cout << howMany << "here";
    else{
        int number = 0;
        for(int i = 0; i < howMany; i++){
            //cout << i;
            cin >> number;
            //cout << "n" << number;
            myList.insertAt(i, number);
        }
    }


    string fun;
    int pos;
    int val;
    while(cin >> fun){

        try{
            if(fun == "insertAt"){
                cin >> pos;
                cin >> val;
                //cout << pos << val;
                myList.insertAt(pos, val);
            }
            else if(fun == "eraseAt"){
                cin >> pos;
                myList.eraseAt(pos);
            }
            else if(fun == "assignAt"){
                cin >> pos;
                cin >> val;
                myList.assignAt(pos, val);
            }
            else if(fun == "pushFront"){
                cin >> val;
                //cout<<"here"<<val;
                myList.pushFront(val);
            }
            else if(fun == "popFront"){
                myList.popFront();
            }
            else if(fun == "moveNext"){
                myList.moveNext();
            }
            else if(fun == "movePrev"){
                myList.movePrev();
            }
            else if(fun == "toString"){
                cout << myList.toString() << endl;
            }
            else{
                cerr << "Wrong operation" << endl;
            }
        }
        catch(const out_of_range &e){
            cout << e.what() << endl;
        }
        catch(const invalid_argument &e){
            cout << e.what() << endl;
        }
    }
    return 0;
    /*CircularList cL;
    cout << cL.toString()  << endl; ///== "[]");
    cerr << "aa" << endl << flush;
    cL.pushFront(2);
    cerr << "bb" << endl << flush;
    cout << cL.getSize() << endl; //== 1);
    cerr << "cc" << endl << flush;
    cout << cL.toString() << endl; // == "[2]");
    cL.pushFront(4);
    cout << cL.getSize() << endl; //== 2);
    cout << cL.toString() << endl; ///== "[4, 2]");
    cL.pushFront(6);
    cout << cL.getSize() << endl; //== 3);
    cout << cL.toString() << endl; // == "[6, 4, 2]");*/
}