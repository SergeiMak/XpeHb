#include <iostream>
#include <cstdlib> // ��� system
#include "menu.h"
using namespace std;

int main()
{
    int choice1;
    setlocale(0, "");
    cout << "��� �������. ��, ������, �� ����� ����." << endl;
    cout << "�����, ����� ��-���� �������, ���� ������ �����" << endl;
    cin >> choice1;

    if (choice1 == 1) {
        cout << "�������, ������, ��� �������" << endl;
        main_cycle();
    }
    else {
        cout << "�������, ������, ��� " << choice1 << endl;
    }
    system("pause"); // ������ ��� ���, � ���� MS Visual Studio
    return 0;
}