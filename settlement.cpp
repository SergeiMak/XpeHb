#include <iostream>
#include <cstdlib> // для system
#include "settlement.h"
#include "pops.h"
#include <numeric>
#include <vector>
#include <math.h>

using namespace std;

void Settlement::set_name(char city_name) {
	name = city_name;
}

void Settlement::count_population()
{
	population = 0;
	int i;
	for (i = 0; i <= pop_dict.size(); i++) {
		population += pop_dict[i].total_population;
	}
}

void Settlement::add_pop()
{
	Pops new_pop(this, )
	pop_location.pop_dict.push_back(this);
}

