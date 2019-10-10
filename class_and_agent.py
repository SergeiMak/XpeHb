class Culture:
    Cult_number = 0

    def __init__(self, name):
        self.name = name
        Culture.Cult_number  += 1

        self.number = Culture.Cult_number


class Religion:
    Rel_number = 0

    def __init__(self, name):
        self.name = name
        Religion.Rel_number  += 1

        self.number = Religion.Rel_number


class Strata:
    Str_number = 0

    def __init__(self, name):
        self.name = name
        Strata.Str_number  += 1

        self.number = Strata.Str_number



class Pops:


    def __init__(self, location, strata, num, culture, religion, literacy, unemployment, agr, consciousness, patriotism,
                 needs_v, goods_v, desire_v, polit_v, dispers, money, birth):

        self.num = num
        self.culture = culture
        self.location = location
        self.strata = strata
        self.religion = religion
        self.literacy = literacy
        self.unemployment = unemployment
        self.agr = agr
        self.consciousness = consciousness
        self.patriotism = patriotism
        self.needs_v = needs_v      # daily needs, rich shit
        self.goods_v = goods_v      # what needs for daily needs, which rich shit
        self.desire_v = desire_v    # desires for laws
        self.polit_v = polit_v      # ideology support
        self.dispers = dispers
        self.money = money
        self.birth = birth


    def display_info(self):
        print('Number: {}. Location: {}'.format(self.num, self.location))



class Settlement:
    Settl_number = 0

    def __init__(self, coordinates, mm, name):
        self.size = 1
        mm[coordinates] = 2
        self.area = np.array(coordinates)
        self.name = name

        Settlement.Settl_number  += 1

        self.number = Settlement.Settl_number


    def display_inform(self):
        print('Number: {}. Population: {}'.format(self.number, self.population))


    def growth(self, mm):
        if self.population > 5000*self.size:
            self.size  += 1
            mm[self.area] = 2               # max + or min -



    def type_change(self, mm):
        if self.size > 10:
            for i in len(self.area):
                mm[self.area[i]] = 3



class Factory:
    Fact_number = 0

    def __init__(self, location, num_workers, work_type, good, money,number):
        self.location = location
        self.work_type = work_type
        self.num_workers = num_workers
        self.good = good
        self.money = money
        Factory.Fact_number  += 1

        self.number = Factory.Fact_number

    def display_inform(self):
        print('Number: {}. Population: {}'.format(self.number, self.population))