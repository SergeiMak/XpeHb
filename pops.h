#pragma once

#ifndef POPS_H
#define POPS_H
#include "settlement.h"
#include <vector>

#include <iostream>
#include <cstdlib> // для system
using namespace std;

class Pops {
public:
	Settlement location;
	vector<int> male_population;
	vector<int> female_population;
	int total_population;
	
	Pops(Settlement pop_location, vector<int> male_population1, vector<int> female_population1);


	void set_location(Settlement pop_location);
	void recalculate_population(vector<int> vec_pop, int i);
	void pop_change();
	// vector<int> male_population1 = this.male_population, vector<int> female_population1 = female_population


};

#endif