import goods
import numpy as np

class Pops:


    def __init__(self, location, num, strata, dispers, money, unemployed, realnye = True):


        self.location = location                     # прописька есть? пройдёмте, гражданин
        self.strata = strata
        #self.unemployment = unemployment
        self.unemployed = unemployed
        self.inventory = {'Grain': 0, 'Fish':0}          # что у попа есть
        self.cons = {'Grain': 1,'Fish':1}                    # что попу надо потреблять
        self.male_age = np.array((0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10*num,0,0,0,0,0,0,0,0,
                                  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                                  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0), dtype=np.uint16)               # сколько кого по возрастам мужиков
        self.female_age = np.array((0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10*num,0,0,0,0,0,0,0,0,
                                  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                                  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0), dtype=np.uint16)                   # баб
        self.total_num = sum(self.male_age) + sum(self.female_age)                       # вестимо суммарно

        self.dispers = dispers                               # хуйня пока не пригодилась
        self.money = money
        if realnye:                                  # для болванчиков не работает
            #location.population += self.num
            location.serfs = self                  # связываем этот поп с городским попом безработных (пока что такая система, раньше была другая)
            location.pops[self] = self                 # записываем в словарь экземпляра поселения, что в нём есть этот поп
            Pops.popchange(self)
        self.migrate = 0




    def popchange(self):
        """короч, рождение, старение и смерть населения в попах
        суть в чём. поп делится на 75 частей - 75 лет. каждый год происходит обновление.
        при обновлении переносится в следующий год население с года предыдущего, при этом рандомное количество
        дохнет (распределение подобрал функцией так, чтоб в 0 лет дохло 20%, до 5 лет дохло 40%, а потом суммарно
        порядка 3-4% (все данные взяты с вики и с охуительного сайта с множеством данных https://ourworldindata.org/ )
        при этом если народу меньше 100 человек, то рандомит для каждого отдельно. если больше, то делится на 100 частей.

        рождение тоже простое. считается, кого больше мужиков или баб осталось (просто мужики имеют свойство дохнуть раньше
        и больше. например в войнах.
        (а ещё я думаю сделать систему "прямого взаимодействия государства с группами населения"
        всё по заветам аллоизыча и виссарионыча).
        после этого того, кого меньше умножаем на коэффициент воспроизводства.
        позже надо добавить другие коэффициенты (уже есть например связанный с социальным статусом), однако непонятно,
        что влияет на рождаемость. можно было бы предположить, что образование, но в РИ образованное дворянство плодилось
        с такой же скоростью, что и бедное и неграмотное крестьянство. причём крестьянство в среднем дохло меньше (4% смертность
        против 3,5%).
        искать, кого меньше, нужно для того, чтобы учесть то, что для зачатия нужен ровно 1 мужик и 1 баба. мы тут
        внебрачие не поощряем.
        причём баб учитываем с 15 до 45, а мужиков до смерти (будто бы они дольше 45 жили, хаха)
        """
        male_smertnost_koef = 0.003
        female_smertnost = 0.003
        child_smertnost_koef = 10
        rozhdaemost = 0.2 * self.strata.birth_rate
        for i in range(len(self.male_age) - 1):
            #self.male_age[74 - i] += self.male_age[74 - (i + 1)]# * (1 - ((1 / ((74 - (i + 1)) + 0.5)) + ((74 - (i + 1)) / 50 - 0.2) ** 5) / 10)
            if self.male_age[74 - i-1] < 100:
                r1 = np.random.sample(self.male_age[74 - i-1])
                r2 = sum(r1 < ((1 / ((74 - (i + 1)) + 0.5)) + ((74 - (i + 1)) / 50 - 0.2) ** 5) / 10)
                self.male_age[74 - i] += self.male_age[74 - (i + 1)] - r2
            else:
                r1 = np.random.sample(99)
                r2 = sum(r1 < ((1 / ((74 - (i + 1)) + 0.5)) + ((74 - (i + 1)) / 50 - 0.2) ** 5) / 10)
                self.male_age[74 - i] += self.male_age[74 - (i + 1)]*(1-r2/100)
            if self.female_age[74 - i-1] < 100:
                r1 = np.random.sample(self.female_age[74 - i-1])
                r2 = sum(r1 < ((1 / ((74 - (i + 1)) + 0.5)) + ((74 - (i + 1)) / 50 - 0.2) ** 5) / 10)
                self.female_age[74 - i] += self.female_age[74 - (i + 1)] - r2
            else:
                r1 = np.random.sample(99)
                r2 = sum(r1 < ((1 / ((74 - (i + 1)) + 0.5)) + ((74 - (i + 1)) / 50 - 0.2) ** 5) / 10)
                self.female_age[74 - i] += self.female_age[74 - (i + 1)]*(1-r2/100)
            self.male_age[74 - (i + 1)] = 0
            self.female_age[74 - (i + 1)] = 0
        koef_male = sum(self.male_age[15:])
        koef_female = sum(self.female_age[15:45])
        if koef_male <= koef_female:
            self.male_age[0] = (koef_male * rozhdaemost) / 2
            self.female_age[0] = self.male_age[0]
        else:
            self.male_age[0] = (koef_female * rozhdaemost) / 2
            self.female_age[0] = self.male_age[0]
        self.total_num = sum(self.male_age) + sum(self.female_age)
        """тут в зависимости от законов считаем, кто годится в рабочие"""
        if self.location.state.laws['Female_emans']:
            if self.location.state.laws['Children_labour']:
                self.num = sum(self.male_age[10:]) + sum(self.female_age[10:])
            else:
                self.num = sum(self.male_age[18:]) + sum(self.female_age[18:])
        else:
            if self.location.state.laws['Children_labour']:
                self.num = sum(self.male_age[10:])
            else:
                self.num = sum(self.male_age[18:])


    def popgrowth(self):
        """
        ЭТА ХУЙНЯ УЖЕ УСТАРЕЛА. ОПИСЫВАТЬ НЕ БУДУ
        УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
        УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
        УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
        ПЛАНЫ: дошкольное образование (т.е. для детей) напрямую усиливает ассимиляцию
        сделать тупо какую-нибудь аппроксимирующую функцию типа нормального распределения
        сделать ограничение реализации каких-либо социальных институтов: они доступны если есть открытие или
        у какой-нибудь страны это уже реализовано (надо тогда запрогать что-то типа "великого посольства")
        :return:
        """
        male_smertnost_koef = 0.003
        female_smertnost = 0.003                           # из вики по населению российской империи
        child_smertnost_koef = 10                          # (1/(x+2)+(x/100-0.1)^4)/10
        rozhdaemost = 0.2*self.strata.birth_rate           # 130 миллионов детей рождается ежегодно
        for i in range(len(self.male_age)-1):               # 6 миллионов - детская смертность в 2012 году
            self.male_age[74-i] += self.male_age[74-(i+1)]*(1-((1/((74-(i+1))+0.5))+((74-(i+1))/50-0.2)**5)/10)
            self.female_age[74 - i] += self.female_age[74 - (i + 1)]*(1-((1/((74-(i+1))+0.5))+((74-(i+1))/50-0.2)**5)/10)
            self.male_age[74 - (i + 1)] = 0
            self.female_age[74 - (i + 1)] = 0
        koef_male = sum(self.male_age[15:])
        koef_female = sum(self.female_age[15:45])
        if koef_male <= koef_female:
            self.male_age[0] = (koef_male*rozhdaemost)/2
            self.female_age[0] = self.male_age[0]
        else:
            self.male_age[0] = (koef_female*rozhdaemost)/2
            self.female_age[0] = self.male_age[0]
        self.total_num = sum(self.male_age) + sum(self.female_age)
        if self.location.state.laws['Female_emans']:
            if self.location.state.laws['Children_labour']:
                self.num = sum(self.male_age[10:]) + sum(self.female_age[10:])
            else:
                self.num = sum(self.male_age[18:]) + sum(self.female_age[18:])
        else:
            if self.location.state.laws['Children_labour']:
                self.num = sum(self.male_age[10:])
            else:
                self.num = sum(self.male_age[18:])


    def facsearch(self):
        """поиск работы"""
        for q in self.location.factories:
            if q.work_type == self.strata:          # подходит ли завод к распределяемому попу?
                raznost = self.location.factories[q].fullnum - self.location.factories[q].workers.num             # сколько завод может принять рабочих
                gotovo = self.num*self.location.factories[q].coef                 # сколько рабочих готово на НЕГО идти (в соответствии с коэффициентом)
                """рассматриваем разные варианты: готов ли принять завод столько рабочих?
                перемещаются в поп завода, кстати, рабочие прямо с детьми и жёнами"""
                if raznost >= gotovo:
                    for i in range(len(self.male_age)):
                        self.location.factories[q].workers.male_age[i] += self.male_age[i] * \
                                                                                               self.location.factories[
                                                                                                   q].coef
                        self.male_age[i] -= self.male_age[i] * \
                                                                 self.location.factories[q].coef
                        self.location.factories[q].workers.female_age[i] += self.female_age[i] * \
                                                                                                 self.location.factories[
                                                                                                     q].coef
                        self.female_age[i] -= self.female_age[i] * self.location.factories[q].coef
                    if self.num < 0:
                        print('DEBAG!!! POP-FACSEARCH < 0')

                else:
                    for i in range(len(self.male_age)):
                        self.location.factories[q].workers.male_age[i] += self.male_age[i] * raznost/self.num
                        self.male_age[i] -= self.male_age[i] * raznost/self.num
                        self.location.factories[q].workers.female_age[i] += self.female_age[i] * raznost/self.num
                        self.female_age[i] -= self.female_age[i] * raznost/self.num
                    if self.num < 0:
                        print('DEBAG!!! POP-FACSEARCH < 0')


    def serfworkerdeath(self):
        """
        УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
        УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
        УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
        надо походу всё-таки на каждый завод, на каждый ресурс делать свой поп"
        :return:
        """

    def consume(self):
        """
        потребление всего, кроме жратвы. но оно тут хуёво прописано. по-старому.
        :return:
        """
        for i in self.strata.consnf:
            if self.inventory[i] - self.total_num * self.strata.consnf[i] >= 0:
                self.inventory[i] -= self.total_num * self.strata.consnf[i]
            else:
                relatbadmood = self.inventory[i]/(self.total_num * self.strata.consnf[i])
                self.inventory[i] = 0

    def consume_food(self):
        """
        потребление жратвы.
        :return:
        """
        quant123 = 0
        fooddict = self.cons.copy()         # копируем словарь того, что поп в принципе может жрать
        notfound123 = True                   # вспомогательная штука для выхода из цикла вайл
        for i in self.cons:                  # пересчитываем, что в инвентаре вообще есть пожрать
            if self.inventory[i] > 0:
                quant123 += 1
            else:
                fooddict.pop(i)                  # если чего-то нет, то мы удаляем это из скопированного словаря
        if self.location.name == 'Govnovodsk':
            print('ИНВЕНТАРЬ и ДЕНЬГИ Говноводчан', self.inventory, self.money)
        if quant123 == 0:                        # если нихуя нет пожрать, то дохнут
            for q in range(len(self.male_age)):
                self.male_age[q] *=0.95
                self.female_age[q] *= 0.95
        else:
            while notfound123:   # распределяем жрачку по потреблению. чтоб съел либо 1 буханку хлеба, либо полбуханки и полпалки колбасы, либо треть одного, треть второго и треть третьего продукта
                fooddict, quant123, notfound123 = Pops.consume_exclude(self,fooddict,quant123)
                if quant123 == 0:
                    eaten = 0
                    for i in self.cons:
                        if self.inventory[i] > 0:
                            eaten += self.inventory[i]/(self.total_num * self.cons[i])
                            self.inventory[i] = 0
                            self.emigrate = min(self.migrate,1 - eaten)
                            self.migrate = 1 - eaten
                            #Pops.migration(self)                               # тут тип если еда есть, но недостаточно
                                                                                # тогда эмиграция или ещё что. пока не продумал до конца



                elif notfound123 == False:                   # если нашли достаточно продуктов для потребления - стопаем цикл и жрём
                    for i in fooddict:
                        self.inventory[i] -= (self.total_num * self.cons[i])/quant123

    def consume_exclude(self,fooddict,quant123):
        """вспомогательная функция для исключения того, чего слишком мало для пожирания"""
        qu123 = quant123
        notfound123 = True
        for i in list(fooddict):
            if self.inventory[i] < (self.total_num * self.cons[i])/quant123:
                quant123 -= 1
                fooddict.pop(i)
        if qu123 == quant123:
            notfound123 = False
        return fooddict, quant123, notfound123

    def serf_winter123(self):
        """
        УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
        УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
        УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
        короче типа заготовки на зиму крестьянам. прибирают себе излишки после вычитания налогов
         если набрали жратвы на год, то остатки еды продают и на эти деньги покупают себе на год
         то, что потребляют помимо еды. остаток денег служит для роскоши или соц лифта
        :return:
        """
        if self.strata.name == 'Serf':
            for i in self.strata.cons:
                if i in self.location.factories:
                    if self.location.factories[i].sell[i] >= self.num*self.strata.cons[i]:
                        self.location.factories[i].sell[i] -= self.num * self.strata.cons[i]
                        self.inventory[i] += self.num * self.strata.cons[i]
                    else:
                        self.inventory[i] += self.location.factories[i].sell[i]
                        self.location.factories[i].sell[i] = 0

    def popbuy(self):
        """
        покупка попами того, что они потребляют
        тут изначально заложен мини-баг - если попы сначала что-то недокупили, то по возможности в следующем месте
        они купят ВСЮ нужду, даже если это больше, чем надо. но да хрен с ним, будет аналогом покупки прозапас

        суть такова. заводы подают после корректировки цен собственно эти их цены на товары, что они продают, в словарь
        мы берём эти словари и пересчитываем цены с учётом расстояния (введено), пошлин (не введено), инфраструктуры:
        портов, рек, Ж/Д (не введено)

        после этого просто покупаем у того, кто суммарно дешевле продаст. если не хватило - покупаем у следующего. и т.д.
        :return:
        """
        #print('DEBUG MONEY BEFORE', self.location.name, self.money)
        roadcoef = 0.1
        for i in self.cons:
            pricedict = goods.Goods.gddict[i].prices.copy()
            for j in pricedict:
                pricedict[j] = pricedict[j] * (1 + roadcoef * np.sqrt((j.location.area[0][0] - self.location.area[0][0])**2 +
                                                 (j.location.area[0][1] - self.location.area[0][1])**2))
            #print('Pricedict is ',i, pricedict.values())
            flag1 = True
            if self.inventory[i] < self.cons[i] * self.total_num and self.money > 0:
                while flag1:
                    minpr = min(pricedict, key=pricedict.get)
                    #buylist.append(minpr)
                    if minpr.sell[i] >= self.cons[i]*self.total_num:
                        if self.money >= pricedict[minpr]*self.cons[i]*self.total_num:
                            minpr.money += pricedict[minpr]*self.cons[i]*self.total_num
                            self.money -= pricedict[minpr]*self.cons[i]*self.total_num
                            self.inventory[i] += self.cons[i]*self.total_num
                            minpr.sell[i] -= self.cons[i]*self.total_num
                        else:
                            if self.money > 0:
                                minpr.money += self.money
                                self.inventory[i] += self.money/pricedict[minpr]
                                minpr.sell[i] -= self.money/pricedict[minpr]
                                self.money -= self.money
                    else:
                        if self.money >= pricedict[minpr]*minpr.sell[i]:
                            minpr.money += pricedict[minpr]*minpr.sell[i]
                            self.money -= pricedict[minpr]*minpr.sell[i]
                            self.inventory[i] += minpr.sell[i]
                            minpr.sell[i] -= minpr.sell[i]
                        else:
                            if self.money > 0:
                                minpr.money += self.money
                                self.inventory[i] += self.money/pricedict[minpr]
                                minpr.sell[i] -= self.money/pricedict[minpr]
                                self.money -= self.money
                    if self.cons[i]*self.total_num <= self.inventory[i]:
                        flag1 = False
                    pricedict.pop(minpr)
                    if not pricedict:
                        flag1 = False
                    if self.money == 0:
                        flag1 = False

    def migration(self):
        """ещё нихуя нет))"""
        if self.emigrate > 0:
            print('Migration method')














    #def buying(self):



"""     def __init__(self, location, strata, num, culture, religion, literacy, unemployment, agr, consciousness, patriotism,
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
        self.birth = birth    def __init__(self, location, strata, num, culture, religion, literacy, unemployment, agr, consciousness, patriotism,
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
        self.birth = birth"""