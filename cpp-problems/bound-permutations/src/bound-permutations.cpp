#include <iostream>
#include <string>
#include <sstream>
#include <vector>

using namespace std;

vector<int> getNumbers(string line)
{
    vector<int> result;
    istringstream istream(line);
    int num;
    while (istream >> num)
    {
        result.push_back(num);
    }
    return result;
}

string twoArrays(int k, vector<int> A, vector<int> B)
{
    int n = A.size();
    vector<int> BTaken(n, 0);
    bool found = false;
    for (int i = 0; i < n; i++)
    {
        found = false;
        int minFeasible = 0;
        int idxTaken = -1;
        // find the smallest feasible in B and mark as taken
        for (int j = 0; j < n; j++)
        {
            if (A.at(i) + B.at(j) >= k && BTaken.at(j) == 0)
            {
                if (!found)
                {
                    found = true;
                    idxTaken = j;
                    minFeasible = B.at(j);
                }
                if (found && B.at(j) < minFeasible)
                {
                    minFeasible = B.at(j);
                    idxTaken = j;
                }
            }
        }
        if (!found)
            break;
        else
        {
            BTaken[idxTaken] = 1;
        }
    }
    return (found ? "true" : "false");
}

int main()
{

    string line1;
    string line2;
    //istringstream istream(line);

    while (true)
    {
        if (!getline(cin, line1))
        {
            break;
        }

        int t;
        cin >> t;

        if (t == 0)
        {
            break;
        }

        if (!getline(cin, line1) || !getline(cin, line2))
        {
            break;
        }

        vector<int> v1 = getNumbers(line1);
        vector<int> v2 = getNumbers(line2);
        string result = twoArrays(t, v1, v2);
        cout << result << endl;
    }

    return 0;
}
