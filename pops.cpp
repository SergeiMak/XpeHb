#include <iostream>
#include <cstdlib> // äëÿ system
#include "pops.h"
#include <math.h>
#include <numeric>
#include <vector>

using namespace std;


Pops::Pops(Settlement pop_location, vector<int> male_population1, vector<int> female_population1) {

	location = pop_location;
	male_population = male_population1;
	female_population = female_population1;





}

void Pops::set_location(Settlement pop_location)
{
	location = pop_location;
}


void Pops::pop_change() {
	int i;
	float birth_rate = 0.1;
	for (i = 0; i <= male_population.size(); i++) {
		recalculate_population(male_population, i);
		recalculate_population(female_population, i);
	}
	int fertile_men;
	int fertile_women;
	fertile_men = accumulate(male_population.begin() + 14, male_population.end(), 0);
	fertile_women = accumulate(female_population.begin() + 14, female_population.begin() + 44, 0);

	if (fertile_men <= fertile_women) {

		male_population[0] = fertile_men * birth_rate / 2;
		female_population[0] = male_population[0];


	}
	else {
		male_population[0] = fertile_women * birth_rate / 2;
		female_population[0] = male_population[0];
	}
	male_population[74] = 0;
	female_population[74] = 0;

	total_population = fertile_men = accumulate(female_population.begin(), female_population.end(), 0) + accumulate(male_population.begin(), male_population.end(), 0);
	// ÈÌÏËÅÌÅÍÒÈÐÎÂÀÒÜ ÏÎÄÑ×¨Ò ÐÀÁÎ×ÈÕ
}

void Pops::recalculate_population(vector<int> vec_pop, int i) {
	if (vec_pop[74 - (i-1)] <= 100) {

		// òóò, íàâåðíîå, ìîæíî êàê-òî ïðîùå ñäåëàòü ìàññèâ ñëó÷àéíûõ ÷èñåë, íî ÿ õç êàê

		int deaths = 0;
		for (int j = 1; j < vec_pop[74 - (i - 1)]; j++) {
			if (rand() % 101 < ((1 / ((74 - (i + 1)) + 0.5)) + pow(((74 - (i + 1)) / 50 - 0.2), 5)) * 10) {
				deaths++;
			}
		}
		vec_pop[74 - (i)] = vec_pop[74 - (i - 1)] - deaths;
	}
	else {
		int deaths = 0;
		for (int j = 1; j < 100; j++) {
			if (rand() % 101 < ((1 / ((74 - (i + 1)) + 0.5)) + pow(((74 - (i + 1)) / 50 - 0.2), 5)) * 10) {
				deaths++;
			}
		}
		vec_pop[74 - (i)] = vec_pop[74 - (i - 1)] - (vec_pop[74 - (i - 1)]*deaths)/100;
	}
}