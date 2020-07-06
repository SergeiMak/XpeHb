#pragma once

#ifndef SETTLEMENT_H
#define SETTLEMENT_H

#include <iostream>
#include <cstdlib> // для system
#include <map>
#include <vector>
#include "pops.h"

using namespace std;

class Settlement {
public:
	int size;
	char name;
	int population;
	vector<Pops> pop_dict;

	void set_name(char city_name);
	void count_population();
	void add_pop();

	Settlement(char city_name = 'G') {
		name = city_name;
	}

};


#endif