// stack of integers
class Stack {
  private:
    int maxSize;
    int* items; 
    int current;
  public:
    Stack(int maxSize);
    void push(int item);
    int pop();
    int top();
};
