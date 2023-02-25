#include <iostream>

using namespace std;
int findMax(int arr[][5], int &rowNum, int &colNum)
{
    int max = arr[0][0];
    for (int i = 0; i < 3; i++)
    {
        for (int j =0; j < 5; j++) {
            if (arr[i][j]>=max) {
                max = arr[i][j];
                rowNum = i;
                colNum = j;
            }
        }
    }
    return max;
}

int main()
{
    int arr[3][5];
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 5; j++)
            cin >> arr[i][j];
    int i, j;
    int maxValue = findMax(arr, i, j);
    cout << maxValue << " " << i << " " << j << endl;
}