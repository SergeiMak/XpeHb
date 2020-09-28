#include "settlement.h"
#pragma once
#include "pops.h"
#include "culture.h"
#include "religion.h"
#include "strata.h"
#include "state.h"
#include <iostream>
#include <string>
#include <cstdlib> // для system
using namespace std;

void game_start(bool start){
    bool cycle = start;
    const int oneday = 100;
    const int oneweek = 700;
    const int onemonth = 3000;
    const int oneyear = 36000;
    const vector<string> weekdays = {"Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"};
    const vector<string> months = {"January","February","March","April","May","June","July","August","September","October","November","December"};
    int current_day = 0;
    int current_week_day = 0;
    int current_month = 0;
    int current_year = 1800;
    int time = 1;

    int city_place[2] = {10,0};
    State state1("Pakistan");
    Culture cult1("pakistani");
    Religion rel1("jewish");
    Religion rel2("makaronni");
    Strata serf("serf");
    Settlement city1("Gownozhujsk",state1,city_place);
    Pops pop1(city1,cult1,rel1,serf);
    Pops pop2(city1,cult1,rel2,serf);
    city1.list_pops();
    while(cycle){

        if(time == oneday){
            cout<<current_day<<" "+months[current_month]<<" "<<current_year<<endl;

            if(current_week_day==6){
                current_week_day = 0;
                pop1.popchange();
                cout<<"Population: "<<city1.population<<endl;
            } else{
                current_week_day += 1;
            }
            if (current_day == 29){
                current_day = 0;
                if(current_month == 11){
                    current_month = 0;
                    current_year += 1;
                } else{
                    current_month += 1;
                }
            } else{
                current_day += 1;
            }
            time = 1;
        }
        ++time;

    }
    //return 0;
}
