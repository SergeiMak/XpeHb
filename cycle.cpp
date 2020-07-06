#include <iostream>
#include <cstdlib> // äëÿ system
#include "pops.h"
using namespace std;

void main_cycle()
{
	int cycle = 1;

	while (cycle < 10) {
		cout << "ÕÓÉ ÏÈÇÄÀ ÄÆÈÃÓÐÄÀ" << endl;
		cycle++;
	}
	cout << "¨áíèòå-êà íàçâàíèå ãîðîäà äëÿ Æîïû: " << endl;

	vector<int> male_population(74,0);
	male_population[20] = 100;
	vector<int> female_population(74, 0);
	female_population[20] = 100;
	Settlement city1;
	char city_name;
	Pops pop1(city1, male_population, female_population);


	cin >> city_name;

	city1.set_name(city_name);

	cout << 


}