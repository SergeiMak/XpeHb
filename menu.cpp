#include <iostream>
#include <cstdlib> // для system
#include "menu.h"
using namespace std;

int main()
{
    int choice1;
    setlocale(0, "");
    cout << "Это менюшка. Да, кривая, но какая есть." << endl;
    cout << "Короч, чтобы чё-нить выбрать, надо ввести число" << endl;
    cin >> choice1;

    if (choice1 == 1) {
        cout << "Молодец, долбоёб, ввёл единицу" << endl;
        main_cycle();
    }
    else {
        cout << "Молодец, долбоёб, ввёл " << choice1 << endl;
    }
    system("pause"); // Только для тех, у кого MS Visual Studio
    return 0;
}