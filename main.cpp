#pragma once
#include "mainwindow.h"
#include "settlement.h"
#include "pops.h"
#include <iostream>
#include <string>
#include <cstdlib> // для system
#include "game_cycle.h"
using namespace std;


int main()
{
    vector<string> menu = {"","",""};
    menu[0] = "startui ili pizdui - 1";
    menu[1] = "gruzi ili pizdi - 2";
    menu[2] = "sjebat - 3";
    for(int count = 0; count<3;++count){
        cout<<menu[count]<<endl;
    }
    int decision;
    cout<<"Wwedi swoj wybor, stalker:"<<endl;
    cin>>decision;
    if(decision == 1){
        cout<<"sosi hui"<<endl;

        game_start(true);
    }else if(decision == 2){
        cout<<"tozhe sosi";
    }else if(decision == 3){
        cout<<"nu i idi nahui";
        cout<<"i wwedi null, jeblan";
        cin>>decision;
        if(decision == 0){
            return decision;
        }
    }
    return 0;
}
