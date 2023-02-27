#include <string>
#include<iostream>
#include <iostream>
#include "CircularList.h"

using namespace std;
using namespace ds_course;

CircularList::CircularList(){
    size = 0;
}

CircularList::~CircularList(){
}

void CircularList::emptyFromTheBeginning(){
    size = 0;
    tail_->next = NULL;
    tail_->prev = NULL;
}

bool CircularList::isEmpty() const{
    if(size == 0){
        return true;
    }
    else{
        return false;
    }
}

int& CircularList::head() const{
    if(isEmpty()){
        throw new out_of_range("OutOfRange: List is empty");
    }
    else{
        CLNode* first = tail_->next;
        return first->info;
    }
}

int& CircularList::tail() const{
    if(isEmpty()){
        throw new out_of_range("OutOfRange: List is empty");
    }
    else{
        return tail_->info;
    }
}

void CircularList::pushFront(int val){
    if(val > 1000000000 || val < 0){
        throw invalid_argument("InvalidArgument: Number not inserted");
    }
    else if(isEmpty()){
        //cout << "here";
        CLNode* newNode = new CLNode();
        newNode->info = val;
        newNode->next = newNode;
        newNode->prev = newNode;
        tail_ = newNode;
        size++;
    }
    else{
        //cout<<size;
        //cout<< "here";
        CLNode* newNode = new CLNode();
        newNode->info = val;
        //cout<<tail_->info;
        CLNode* first = tail_->next;
        //cout<<first->info;
        newNode->prev = tail_;
        newNode->next = first;
        tail_->next = newNode;
        first->prev = newNode;
        size++;
        //cout<< tail_->next->info;
        //cout<<size;
    }
}

void CircularList::popFront(){
    if(isEmpty()){
        throw out_of_range("OutOfRange: List is empty");
    }
    else{
        CLNode* last = tail_;
        CLNode* second = tail_->next->next;
        CLNode* first = tail_->next;
        last->next = second;
        second->prev = last;
        first->next = NULL;
        first->prev = NULL;
        size--;
    }
}

int count = 0;
void CircularList::insertAt(int pos, int val){
    if(count == 0){
        size = 0;
        count++;
    }
    //cout << size;
    //cout << "now?";
    //cout << getSize();
    //cout << val;
    if(val > 1000000000 || val < 0){
        throw invalid_argument("InvalidArgument: Number not inserted");
    }
    else if(isEmpty() && pos == 0){
        CLNode* newNode = new CLNode();
        newNode->info = val;
        newNode->next = newNode;
        newNode->prev = newNode;
        tail_ = newNode;
        //cout << size;
        size++;
        //cout << size;
    }
    else if(pos < 0 || pos >= size + 1){
        //cout << "size";
        throw out_of_range("OutOfRange: Non-existent position");
    }
    else if(pos == size){
        CLNode* newNode = new CLNode();
        newNode->info = val;
        CLNode* before = tail_;
        CLNode* after = tail_;
        for(int j = 0; j < size - 1; j++){
            //cout << "t";
            after = after->prev;
        }
        //cout << after->info;
        newNode->prev = before;
        newNode->next = after;
        before->next = newNode;
        after->prev = newNode;
        tail_ = newNode;
        //cout << tail_->info;
        size++;
    }
    else if(pos == 0){
        pushFront(val);
    }
    else{
        CLNode* newNode = new CLNode();
        newNode->info = val;
        //cout << tail_->info;
        CLNode* before = tail_;
        for(int j = 0; j < pos + 2; j++){
            before = before->prev;
        }
        //cout << before->info;
        CLNode* after = before->next;
        //cout << after->info;
        newNode->prev = before;
        newNode->next = after;
        before->next = newNode;
        after->prev = newNode;
        size++;
    }
    //cout << toString() << endl;
    //cout << "next" << endl;
    //cout << pos << endl;
    //cout << val << endl;
    //cout << size << endl;
}

void CircularList::eraseAt(int pos){
    if(isEmpty() || pos >= size || pos < 0){
        throw out_of_range("OutOfRange: Non-existent position");
    }
    else{
        CLNode* before = tail_->next; //go to first
        for(int j = 0; j < pos - 1; j++){
            before = before->next;
        }
        //cout << before->info;
        CLNode* after = before->next->next;
        //cout << after->info;
        before->next = after;
        after->prev = before;
        size--;
    }
}


void CircularList::moveNext(){
    tail_ = tail_->next;
}

void CircularList::movePrev(){
    tail_ = tail_->prev;
}

string CircularList::toString(){
    string result;
    if(isEmpty()){
        result = "[]";
    }
    else{
        CLNode* current = tail_->next; //first
        result = "[";
        for(int i = 0; i < size; i++){
            if(i == size - 1){
                result = result + to_string(current->info);
            }
            else{
                result = result + to_string(current->info) + ", ";
                current = current->next;
            }
        }
        result = result + "]";
    }
    return result;
}

int CircularList::getSize(){
    return size;
}

void CircularList::assignAt(int pos, int val){
    //cout << size;
    //cout << pos;
    if(val > 1000000000 || val < 0){
        throw invalid_argument("InvalidArgument: Number not inserted");
    }
    else if(isEmpty() && pos == 0){
        CLNode* newNode = new CLNode();
        newNode->info = val;
        newNode->next = newNode;
        newNode->prev = newNode;
        tail_ = newNode;
        //cout << size;
        size++;
        //cout << size;
    }
    else if(pos < 0 || pos >= size + 1){
        throw out_of_range("OutOfRange: Non-existent position");
    }
    else{
        CLNode* placeWhereToAdd = tail_;
        for(int j = 0; j < pos + 1; j++){
            placeWhereToAdd = placeWhereToAdd->next;
        }
        //cout << placeWhereToAdd->info;
        placeWhereToAdd->info = val;
    }
}