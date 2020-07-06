#pragma once
#include "settlement.h"

class Factory
{
public:
	Settlement location;
	float money;
	void set_location(char city_name);
};

