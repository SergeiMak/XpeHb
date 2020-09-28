#ifndef FACTORY_H
#define FACTORY_H
#include "settlement.h"

class Factory
{
public:
    Settlement location;
    Factory(Settlement &fac_location);
};

#endif // FACTORY_H
