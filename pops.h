#ifndef POPS_H
#define POPS_H
#include <vector>
#include <string>
#include <cstdlib> // для system
using namespace std;
#include "settlement.h"
#include "culture.h"
#include "religion.h"
#include "strata.h"
#include "state.h"

class Settlement;

class Pops
{
private:
    Settlement &location;
    vector<int> male_age;
    vector<int> female_age;
public:
    Pops(Settlement &pop_location, Culture &cult, Religion &rel, Strata &strat);
    Culture pop_culture;
    Religion pop_religion;
    Strata pop_strata;

    int total_population;
    //Pops();
    void popchange();
    void recalculate_population(vector<int> &vec_pop, int i);

};

#endif // POPS_H
