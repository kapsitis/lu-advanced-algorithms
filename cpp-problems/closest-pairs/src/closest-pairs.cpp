#include <iostream>

using namespace std;

// int abs(int a, int b)
// {
//     return (a - b) > 0 ? (a - b) : (b - a);
// }

void print_array(int *arr, int size)
{
    for (int i = 0; i < size; i++)
    {
        cout << arr[i] << " ";
    }
    cout << endl;
}

int main()
{
    int a[2000] = {0};
    // is this number already used
    bool taken[2000] = {false};
    int b[1000] = {0};
    int c[1000] = {0};

    int n = 0;
    for (int i = 0; i < 2000; i++)
    {
        int var;
        cin >> var;
        if (var == 0)
        {
            n = i / 2;
            break;
        }
        a[i] = var;
        taken[i] = false;
    }
    //cout << "n = " << n << endl;

    for (int i = 0; i < n; i++)
    {
        //cout << "i = " << i << endl;
        int first = 0;
        int second = 0;
        int minabs = 1000000000;
        for (int ii = 0; ii < 2 * n; ii++)
        {
            if (!taken[ii])
            {
                //cout << "   ii = " << ii << endl;
                for (int jj = ii + 1; jj < 2 * n; jj++)
                {
                    if (!taken[jj] && abs(a[ii] - a[jj]) < minabs)
                    {
                        minabs = abs(a[ii] - a[jj]);
                        //cout << "##" << a[ii] << " " << a[jj] << " " << minabs << endl;
                        first = ii;
                        second = jj;
                    }
                    else if (!taken[jj])
                    {
                        //cout << "  --" << a[ii] << " " << a[jj] << " " << abs(a[ii] - a[jj]) << endl;
                    }
                }
            }
        }
        taken[first] = true;
        taken[second] = true;
        if (a[first] <= a[second])
        {
            b[i] = a[first];
            c[i] = a[second];
        }
        else
        {
            b[i] = a[second];
            c[i] = a[first];
        }
    }

    print_array(b, n);
    print_array(c, n);

    return 0;
}
