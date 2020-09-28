#include <iostream>
#include <cstdlib> // для syste
#include <math.h>
#include <numeric>
#include <vector>
#include "pops.h"
#include "settlement.h"

using namespace std;

Pops::Pops(Settlement &pop_location, Culture &cult,Religion &rel,Strata &strat):location(pop_location), pop_culture(cult), pop_religion(rel), pop_strata(strat)
{
    //location = pop_location;
    for(int count = 0; count < 75; ++count){
        male_age.push_back(0);
        female_age.push_back(0);
    }
    male_age[20] = 100;
    female_age[20]=100;
    location.add_pop(*this);
    for(int count = 0; count < male_age.size();count++){
        cout<<male_age[count]<<endl;
    }
}

void Pops::popchange(){
    int i;
    float birth_rate = 0.1;
    for (i = 0; i < male_age.size(); i++) {
        recalculate_population(male_age, i);
        recalculate_population(female_age, i);
    }
    int fertile_men;
    int fertile_women;
    fertile_men = accumulate(male_age.begin() + 14, male_age.end(), 0);
    fertile_women = accumulate(female_age.begin() + 14, female_age.begin() + 44, 0);

    if (fertile_men <= fertile_women) {

        male_age[0] = fertile_men * birth_rate / 2;
        female_age[0] = male_age[0];


    }
    else {
        male_age[0] = fertile_women * birth_rate / 2;
        female_age[0] = male_age[0];
    }
    male_age[74] = 0;
    male_age[74] = 0;
    total_population = accumulate(female_age.begin(), female_age.end(), 0) + accumulate(male_age.begin(), male_age.end(), 0);
    cout<<"Population of "<<pop_religion.name<<" is "<<total_population<<endl;
    // ИМПЛЕМЕНТИРОВАТЬ ПОДСЧЁТ РАБОЧИХ КОГДА СДЕЛАЮ ГОСУДАРСТВА И ЗАКОНЫ
}

void Pops::recalculate_population(vector<int> &vec_pop, int i) {
    if (vec_pop[74 - i-1] <= 100) {

        // тут, наверное, можно как-то проще сделать массив случайных чисел, но я хз как

        int deaths = 0;
        for (int j = 0; j < vec_pop[74 - i - 1]; j++) {
            if (rand() % 101 < ((1 / ((74 - (i + 1)) + 0.5)) + pow(((74 - (i + 1)) / 50 - 0.2), 5)) * 10) {
                deaths++;
            }
        }
        vec_pop[74 - i] = vec_pop[74 - i - 1] - deaths;
    }
    else {
        int deaths = 0;
        for (int j = 0; j < 100; j++) {
            if (rand() % 101 < ((1 / ((74 - (i + 1)) + 0.5)) + pow(((74 - (i + 1)) / 50 - 0.2), 5)) * 10) {
                deaths++;
            }
        }
        vec_pop[74 - i] = vec_pop[74 - i - 1] - (vec_pop[74 - i - 1]*deaths)/100;
    }
}
