import pops
import state

"""
КЛАССЫ У НАСЕЛЕНИЯ (КРЕСТЬЯНЕ, РАБОЧИЕ, СВЯЩЕННИКИ И ТД)

планы:
сделать систему школ и университетов, куда можно отдавать детей, чтобы они потом стали теми, кем захотят
а ещё для ассимиляции
причём тогда нужен лишь 1 поп на поселение - школьный поп. ну, для национальных школ, может, тоже надо
а ещё надо ввести солдатские изнасилования
"""
class Strata:
    Str_number = 0
    strSlovar = {}

    def __init__(self, name,state,birth_rate,cons123,consnf):
        self.name = name
        self.state = state
        Strata.Str_number  += 1

        self.number = Strata.Str_number
        self.cons = cons123             # типа то, что жрёт поп этого класса
        self.cons_notfood = consnf               # что потребляет не из еды
        self.birth_rate = birth_rate                      # тип разная скорость воспроизводства у профессоров и голожопых крестьян. но для 19 века это неправда :(
        Strata.strSlovar[self] = self
        self.factories_in_strata = []
        state.strats[self] = self.name


def Existing_Strat(state):
    serf = Strata('Serf',state,1,{'Grain':1,'Fish':1},{'Clothes':1})
    worker = Strata('Worker',state,1,{'Grain':1,'Fish':1},{'Clothes':1})
    soldier = Strata('Soldier',state,0,{'Grain':1,'Fish':1},{'Clothes':1})
    schoolers = Strata('Schooler',state,0.7,{'Grain':1,'Fish':1},{'Clothes':1})
    enterpreneurs = Strata('Enterpreneur',state, 1,{'Grain':1,'Fish':1},{'Clothes':1})
    return serf, worker, soldier,schoolers, enterpreneurs
