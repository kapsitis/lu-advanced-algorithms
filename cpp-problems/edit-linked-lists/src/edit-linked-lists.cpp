#include <iostream>

struct Node
{
    int info;
    Node *next;
};

using namespace std;
void print(Node *first)
{
    Node *current = first;
    while (current != NULL)
    {
        cout << current->info << " ";
        current = current->next;
    }
    cout << endl;
}

void insert(Node *&first, Node *&last, int a)
{
    Node *current = new Node{a, NULL};
    if (first == NULL && last == NULL)
    {
        first = last = current;
    }
    else
    {
        last->next = current;
        last = current;
    }
}

void deleteAll(Node *&first, int val)
{
    // remove stuff from the beginning
    while (first->info == val)
    {
        if (first -> next == NULL)
        {
            // TODO: Remove
            first = NULL;            
        }
        else
        {
            // TODO: Remove
            first = first->next;
        }
    }
    cout << "AAA" << endl;
    print(first);
    cout << "BBB" << endl;
    // now walk through the list (current always points to node -> info != val)
    Node *current = first;
    while (current->next != NULL)
    {
        // just move ahead
        if (current->next->info != val)
        {
            current = current->next;
        }
        else
        {
            while (current->next->info == val)
            {
                // TODO: Remove
                current->next = current->next->next;
            }
        }
    }
}


void changeList(Node *&listHead)
{
    // if list is nonempty
    Node *current = listHead;
    if (listHead != NULL)
    {
        while (current->next->next != NULL)
        {
            current = current->next;
        }
        Node *temp = current->next;
        temp->next = listHead->next;
        current->next = listHead; 
        listHead = temp;
    }
    deleteAll(listHead, 0);
}

int main()
{
    int n;
    cin >> n;
    Node *first = NULL;
    Node *last = NULL;
    for (int i = 0; i < n; i++)
    {
        int a;
        cin >> a;
        insert(first, last, a);
    }
    print(first);

    deleteAll(first,0);

    //changeList(first);

    print(first);
}
