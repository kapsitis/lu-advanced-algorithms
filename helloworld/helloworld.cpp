#include <vector>
#include <iostream>

using namespace std;

class Pair
{
public:
    int nX, nY;

private:
};

int main(int argc, char **argv)
{

    vector<Pair> myVector;
    for (int i = 0; i < 10; i++)
    {
        int x, y;
        cin >> x >> y;
        Pair p;
        p.nX = x;
        p.nY = y;
        myVector.push_back(p);
    }

    for (auto it = myVector.begin(); it != myVector.end(); ++it)
    {
        cout << "(" << (*it).nX << "," << (*it).nY << ")" << endl;
    }
    return 0;
}
