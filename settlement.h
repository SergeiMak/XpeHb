#ifndef SETTLEMENT_H
#define SETTLEMENT_H
#include "pops.h"
#include "state.h"
#include <vector>
#include <string>
#include <functional>
using namespace std;

class Pops;

class Settlement
{
public:
    Settlement() = default ;
    Settlement(string name, State &l_state, int city_location[2]);
    void add_pop(Pops &pop);
    void list_pops();
    void calculate_population();
    int population = 0;
    State loc_state;

private:
    int size = 0;
    //vector<int[2]> area;
    //vector<int[2]> possible_area;
    //vector<int[2]> grain_fields;
    //vector<int[2]> possible_grain_fields;
    string name;
    int location[2];
    vector<std::reference_wrapper<Pops> > pop_list;

    //научиться передавать экземпляр класса по ссылке без копировани
    // и соответственно сделать вектор из попов/ссылок на попов


};

#endif // SETTLEMENT_H
