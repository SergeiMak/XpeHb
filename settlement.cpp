#include "settlement.h"
#include <cstdlib> // для system
#include <iostream>

Settlement::Settlement(string city_name,State &l_state, int city_location[2]):loc_state(l_state), name(city_name)
{
    location[0] = city_location[0];
    location[1] = city_location[1];
}

void Settlement::add_pop(Pops &pop)
{
    pop_list.push_back(pop);
}

void Settlement::list_pops(){
    for(int count =0; count < pop_list.size();count++){
        std::cout<<pop_list[count].get().pop_religion.name<<endl;
    }
}

void Settlement::calculate_population(){
    population = 0;
    for(int count = 0; count < pop_list.size();count++){
        population += pop_list[count].get().total_population;
    }
}
