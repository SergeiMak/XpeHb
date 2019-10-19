"""
сделать коррекцию количества производства - а надо ли это делать? пускай по максимуму производят и удешевляют товар
сделать бы ещё банковский сектор и кредитование. это так-то пиздец важно для капиталистической экономики 19-21 веков
"""

import random
import goods
import pops
import numpy as np

"""
Как переделать систему к многопопной системе?
Переделать суммирование рабочей силы и распределение денег.
Сделать систему создания/уничтожения попов
        - после popchange заносить в общий словарь попы, население которых нулевое.
        - а потом удалять их (или вовсе сразу)
Сделать систему миграции.
        - если уже есть такая же группа (по культуре, религии и месту жительства) то туда добавляем и пересчитываем
            грамотность, агрессивность, сознательность и так далее.
Сделать систему увольнения
        - проверять, есть ли уже соответствующий поп или ещё нет
Сделать изменение оплаты труда - по сути рынок труда.
Сделать систему основания новых поселений при миграции.
"""


"""
стоит обратить внимание, что все параметры эффективности производства хранятся непосредственно в экземпляре завода.
т.е. с открытием новой технологии не происходит автоматически распространение её на ВСЕ заводы. хорошо, кстати, моделирует
современное состояние промышленности в восточной европе.
владельцы заводов должны будут покупать модернизации к ним. купят они или нет - зависит от их консервативности.
нужно ввести государственные субсидии на модернизацию производства - государство платит владельцу (частинику, капиталисту)
чтобы он модернизировал своё производство - конкурентоспособность в перспективе и увеличение (или не падение) налогов
и пошлин в будущем
"""

"""
можно ввести в будущем в зависимости от политики государства разные методы (методы в питоне) распределения зарплаты и
подобного между попами. сейчас всё распределяется поровну (при, например, недостатке средств на производство), а можно
сделать несколько методов, срабатывающих при определённой политике государства (или владельца завода) - например простая
дискриминация: введение очереди получения денег попами (притесняемым не будет хватать)
"""
class Factory:
    Fact_number = 0
    slovar = dict()                          # словарь всех заводов. вот только нахуя?

    def __init__(self, location, work_type, good, money,gehalt,fullnum, num_workers = 0,type=0):
        self.location = location                         # где завод располагается, в каком городе
        self.work_type = work_type                               # чей труд применяется? крестьян? рабочих? учителей?

        #self.workers = pops.Pops(location,0,work_type,1.0,0,0)               # создаём для этих трудяг отдельный поп
        self.good = good                             # по сути тип завода
        self.money = money                                  # деньги завода
        self.gehalt = gehalt                         #  зарплата трудящихся
        self.sell = {}                               # типа инвентаря готовой продукции. на продажу
        self.buy = {}                            # инвентарь требуемых для производства ресурсов
        self.notfull = 1                     # полон ли завод? рабочих в смысле
        self.type = type     # есть идея сделать сельский завод отдельным типом со своими методами. ибо крестьянин на себя пашет, а не на буржуя
        self.fullnum = fullnum             # максимальное количество рабочих
        self.coef = 0                            # коэффициент для распределения на работу
        self.bonuses = {}                        # бонусы при производстве в зависимости от технологий              (для каждого продукта свой бонус)
        self.effectiveness = {}                      # сколько 1 рабочий производит итогового товара                (для каждого продукта своя эффективноть)
        self.usage = {}                                  # сколько он при этом потребляет требуемых ресурсов        (для каждого продукта своё потребление)
        self.booster = {}                                # инвентарь ускорителей/катализаторов/бустеров производства(и так далее...)
        self.boosterusage = {}                   # сколько 1 работяга потребляет бустеров                           (и тому подобное...)
        self.boosterbonus = {}                           # какой бонус даёт в итоге бустер
        self.buyingcoef = {}                         # УСТАРЕВШАЯ ХУЙНЯ
        self.price_changed = {}                          # как изменилась с прошлого изменения цен цена? увеличилась или уменьшилась?
        self.soldprevious = {}                               # сколько в прошлый раз продали товара (в единицах)
        if self.good.name == 'Grain':                    # нужно для многих В БУДУЩЕМ вещей, которые сложно описать с помощью знака #. ныне бесполезно
            self.serf_average_effectiveness = 1     # сколько может 1 работник обрабатывать земли. если ему предоставляют её в достаточном количестве

        self.workers_dict = {}
        self.num_workers = 0
        self.unpaid = 0
        for key in self.workers_dict:
            self.num_workers += key.num                           # количество уже нанятых трудяг

        Factory.types(self)                                  # метод заполняет для этого завода sell, buy, boost, usage и так далее. в зависимости от типа завода
        Factory.setgoodsforpricechange(self)                     # вспомогательная хрень для изменения цены. типа поставить, что они ни на что пока ещё не менялись

        self.after_creation = self.sell.copy()                   # нужно чтобы следить сколько продали товара. after creation - сколько товара лежит после последнего
        self.sell_previous = self.sell.copy()                    # цикла производства. sell previous вроде как не пригодилась. но не уверен. возможно тоже для проверки

        #location.factories[self.good.name] = self
        location.factories[self] = self             # записываем в словарь заводов в городе, в котором стоит завод
        location.facnum += 1

        self.number = Factory.Fact_number                    # присваиваем номер этому заводу
        Factory.Fact_number  += 1
        Factory.slovar[self.number] = self                   # записываем в общий словарь заводов
        good.prices[self] = self.startingprice                       # записываем в словарь продаваемого товара свою цену

    def setgoodsforpricechange(self):
        """вспомогательная хрень для изменения цены. типа поставить, что они ни на что пока ещё не менялись
        """
        for i in self.sell:
            self.price_changed[i] = 0
            print(i, self.price_changed[i])

    def types(self):
        """
        назначаем все характеристики ЭТОГО ТИПА завода
        :return:
        """

        if self.good.name == 'Fish':
            self.sell['Fish'] = 0
            self.effectiveness['Fish'] = 5
            self.bonuses['Fish'] = 0
            self.startingprice = 1

        if self.good.name == 'Grain':
            self.sell['Grain'] = 0
            self.booster['Fertilizer'] = 0
            self.boosterbonus['Fertilizer'] = 1.5
            self.effectiveness['Grain'] = 10
            self.bonuses['Grain'] = 0
            #self.usage['Fertilizer'] = 1
            self.boosterusage['Fertilizer'] = 1
            self.startingprice = 0.5


        if self.good.name == 'Fertilizer':
            self.sell['Fertilizer'] = 0
            self.effectiveness['Fertilizer'] = 10
            self.bonuses['Fertilizer'] = 0
            self.startingprice = 0.3

        if self.good.name == 'Whool':
            self.sell['Whool'] = 0
            self.effectiveness['Whool'] = 3
            self.bonuses['Whool'] = 0
            self.startingprice = 2

        if self.good.name == 'Fabric':
            self.sell['Fabric'] = 0
            self.effectiveness['Fabric'] = 1
            self.bonuses['Fabric'] = 0
            self.usage['Whool'] = 2
            self.usage['Fertilizer'] = 1
            self.startingprice = 5

        if self.good.name == 'Iron':
            self.sell['Iron'] = 0
            self.effectiveness['Iron'] = 10
            self.bonuses['Iron'] = 0
            self.startingprice = 0.5

    def coef(self):
        """высчитываем коэффициент для распределения попов на работу"""
        if self.fullnum == self.num_workers:
            self.coef = 0
            self.notfull = 0
            print('factory in ',self.location.name,' is FULL')
        else:
            self.coef = (self.gehalt ** 3) / self.location.gehsum[self.work_type.name]
            self.notfull = 1

    def create(self,gm):
        """производство товаров

        по сути просто смотрится, каковы условия работы (есть ли деньги платить людям, хватает ли ресурсов на производство
        есть ли бустеры, нужно ли вообще что-либо из закупочных ресурсов или всё достаём из земли и так далее и тому подобное)
        а потом в соответствии с этими условиями тратится всё, что нужно/есть и производится товар. а деньги (зарплата) выплачиваются
        попу
        """
        self.num_workers = 0
        for key in self.workers_dict:
            self.workers_dict[key] = key.num
            self.num_workers += key.num
        whatisdone = {}
        """
        тут короч надо переделать структуру if-else
        должно быть:
        если хватает ресурсов
            если хватает денег
            или
        или
            если денег больше, чем хватает ресурсов
            или
        """
        if len(self.buy) != 0:
            enoughresources = True
            min_workers = self.num_workers
            for keysell in self.buy:
                if self.buy[keysell] < self.num_workers * self.usage[keysell]:
                    enoughresources = False
                    if min_workers > self.buy[keysell] / self.usage[keysell]:
                        min_workers = self.buy[keysell] / self.usage[keysell]
                        fewest = keysell
            if enoughresources:
                if self.money >= self.num_workers * self.gehalt:
                    for key in self.buy:
                        self.buy[key] -= self.num_workers * self.usage[key]
                    for key in self.sell:
                        whatisdone[key] = self.num_workers * self.effectiveness[key] * (1 + self.bonuses[key])
                    for key in self.booster:
                        if self.booster[key] >= self.num_workers * self.boosterusage[key]:
                            self.booster[key] -= self.num_workers * self.boosterusage[key]
                            for key1 in self.sell:
                                whatisdone[key1] *= self.boosterbonus[key]
                    for key1 in self.sell:
                        self.sell[key1] += whatisdone[key1]
                    self.money -= self.num_workers * self.gehalt
                    for j in self.workers_dict:
                        j.money += j.num * self.gehalt
                else:
                    koefic = self.money / self.gehalt
                    for key in self.buy:
                        self.buy[key] -= self.usage[key] * koefic
                    for key in self.sell:
                        whatisdone[key] = self.effectiveness[key] * (1 + self.bonuses[key]) * koefic
                    for key in self.booster:
                        if self.booster[key] >= self.boosterusage[key] * koefic:
                            self.booster[key] -= self.boosterusage[key] * koefic
                            for key1 in self.sell:
                                whatisdone[key1] *= self.boosterbonus[key]
                    for key1 in self.sell:
                        self.sell[key1] += whatisdone[key1]
                    for j in self.workers_dict:
                        j.money += self.money * j.num / self.num_workers
                    self.money -= self.money
                    leaving = min(self.unpaid, 1 - koefic/self.num_workers)  # если какая-то часть населения дважды не уплочена, то она частично уволится
                    if leaving != 0:
                        Factory.leavework(self,leaving)
                    self.unpaid = 1 - koefic/self.num_workers

            else:
                if (self.money / self.gehalt) >= min_workers:

                    for key in self.buy:
                        self.buy[key] -= min_workers * self.usage[key]
                    for key in self.sell:
                        whatisdone[key] = min_workers * self.effectiveness[key] * (1 + self.bonuses[key])
                    for key in self.booster:
                        if self.booster[key] >= min_workers * self.boosterusage[key]:
                            self.booster[key] -= min_workers * self.boosterusage[key]
                            for key1 in self.sell:
                                whatisdone[key1] *= self.boosterbonus[key]
                    for key1 in self.sell:
                        self.sell[key1] += whatisdone[key1]
                    self.money -= min_workers * self.gehalt
                    for j in self.workers_dict:
                        j.money += j.num * self.gehalt * min_workers/self.num_workers
                    leaving = min(self.unpaid,
                                  1 - min_workers / self.num_workers)  # если какая-то часть населения дважды не уплочена, то она частично уволится
                    if leaving != 0:
                        Factory.leavework(self, leaving)
                    self.unpaid = 1 - min_workers / self.num_workers
                else:
                    koefic = self.money / self.gehalt
                    for key in self.buy:
                        self.buy[key] -= self.usage[key] * koefic
                    for key in self.sell:
                        whatisdone[key] = self.effectiveness[key] * (1 + self.bonuses[key]) * koefic
                    for key in self.booster:
                        if self.booster[key] >= self.boosterusage[key] * koefic:
                            self.booster[key] -= self.boosterusage[key] * koefic
                            for key1 in self.sell:
                                whatisdone[key1] *= self.boosterbonus[key]
                    for key1 in self.sell:
                        self.sell[key1] += whatisdone[key1]
                    for j in self.workers_dict:
                        j.money += self.money * j.num / self.num_workers
                    self.money -= self.money
                    leaving = min(self.unpaid,
                                  1 - koefic / self.num_workers)  # если какая-то часть населения дважды не уплочена, то она частично уволится
                    if leaving != 0:
                        Factory.leavework(self, leaving)
                    self.unpaid = 1 - koefic / self.num_workers
        elif not self.type:
            if self.money >= self.num_workers * self.gehalt:
                self.money -= self.num_workers * self.gehalt
                for j in self.workers_dict:
                    j.money += j.num * self.gehalt
                for key in self.sell:
                    whatisdone[key] = self.num_workers * self.effectiveness[key] * (1 + self.bonuses[key])
                for key in self.booster:
                    if self.booster[key] >= self.num_workers * self.boosterusage[key]:
                        self.booster[key] -= self.num_workers * self.boosterusage[key]
                        for key1 in self.sell:
                            whatisdone[key1] *= self.boosterbonus[key]
                for key1 in self.sell:
                    self.sell[key1] += whatisdone[key1]
                if self.money < 0:
                    print('<0 11')
            else:
                if self.money > 0:
                    for key in self.sell:
                        whatisdone[key] = self.effectiveness[key] * (1 + self.bonuses[key]) * self.money/self.gehalt
                    for key in self.booster:
                        if self.booster[key] >= self.boosterusage[key] * self.money/self.gehalt:
                            self.booster[key] -= self.boosterusage[key] * self.money/self.gehalt
                            for key1 in self.sell:
                                whatisdone[key1] *= self.boosterbonus[key]
                    for key1 in self.sell:
                        self.sell[key1] += whatisdone[key1]
                    if self.money < 0:
                        print('<0 22')
                    for j in self.workers_dict:
                        j.money += self.money * j.num / self.num_workers
                    self.money -= self.money
                    leaving = min(self.unpaid,
                                  1 - (self.money/self.gehalt) / self.num_workers)  # если какая-то часть населения дважды не уплочена, то она частично уволится
                    if leaving != 0:
                        Factory.leavework(self, leaving)
                    self.unpaid = 1 - (self.money/self.gehalt) / self.num_workers

        elif self.type and self.good.name != 'Grain':                 # это для крестьян. чтоб при отсутсутствии денег у завода, всё равно бы продолжалось производство зерна, ибо зерно крестьяне, а не завод делают
            for key in self.sell:
                whatisdone[key] = self.num_workers * self.effectiveness[key] * (1 + self.bonuses[key])
            for key in self.booster:
                if self.booster[key] >= self.num_workers * self.boosterusage[key]:
                    self.booster[key] -= self.num_workers * self.boosterusage[key]
                    for key1 in self.sell:
                        whatisdone[key1] *= self.boosterbonus[key]
            for key1 in self.sell:
                self.sell[key1] += whatisdone[key1]
            if self.money < 0:
                print('<0 11')
        elif self.type and self.good.name == 'Grain':

            for key in self.sell:
                whatisdone[key] = 0
            for key in self.sell:
                for coord in self.location.grain_fields:
                    whatisdone[key] += gm[coord] * self.effectiveness[key] * (1 + self.bonuses[key])
            for key in self.booster:
                if self.booster[key] >= self.num_workers * self.boosterusage[key]:
                    self.booster[key] -= self.num_workers * self.boosterusage[key]
                    for key1 in self.sell:
                        whatisdone[key1] *= self.boosterbonus[key]
            for key1 in self.sell:
                self.sell[key1] += whatisdone[key1]
            if self.money < 0:
                print('<0 11')



        self.after_creation = self.sell.copy()
        if self.money < 0:
            print('<0 CREATE')


    def factbuy(self):
        """покупка необходимых ресурсов для производства

        погляди этот же процесс описан для попов - popbuy

        ПЛАНЫ
        учесть отсутствие товаров у некоторых продавцов
        учесть отсутствие товаров в целом
        для этого можно в начале посчитать сумму мировых запасов и если на этой итерации они кончились,
        то не продолжать покупки

        потом учесть эмбарго и подобное

        учесть нерентабельность покупки и неполноту производства - соответственно неполноту оплаты трудящимся
        а после нескольких циклов неоплаты они уходят, а лучше посчитать, сколько раз в году им не заплатили
        и если больше N, то попы уходят с завода
        """
        roadcoef = 0.1
        for i in self.buy:
            if self.good.name == 'Fish':
                print('FISHBUY')
            pricedict = goods.Goods.gddict[i].prices.copy()
            for j in pricedict:
                pricedict[j] = pricedict[j] * (
                            1 + roadcoef * np.sqrt((j.location.area[0][0] - self.location.area[0][0]) ** 2 +
                                                   (j.location.area[0][1] - self.location.area[0][1]) ** 2))
            #print('Pricedict is ', pricedict)
            flag1 = True
            if self.buy[i] < self.num_workers * self.usage[i] and self.money != 0:
                while flag1:
                    minpr = min(pricedict, key=pricedict.get)
                    if minpr.sell[i] >= self.num_workers * self.usage[i]:
                        if self.money >= self.num_workers * self.usage[i]*pricedict[minpr]:
                            minpr.money += pricedict[minpr] * self.num_workers * self.usage[i]
                            self.money -= pricedict[minpr] * self.num_workers * self.usage[i]
                            self.buy[i] += self.num_workers * self.usage[i]
                            minpr.sell[i] -= self.num_workers * self.usage[i]
                            if self.money < 0:
                                print('<0 1')
                        else:
                            minpr.money += self.money
                            self.buy[i] += self.money / pricedict[minpr]
                            minpr.sell[i] -= self.money / pricedict[minpr]
                            self.money -= self.money
                            if self.money < 0:
                                print('<0 2')
                    else:
                        if self.money >= pricedict[minpr] * minpr.sell[i]:
                            minpr.money += pricedict[minpr] * minpr.sell[i]
                            self.money -= pricedict[minpr] * minpr.sell[i]
                            self.buy[i] += minpr.sell[i]
                            minpr.sell[i] -= minpr.sell[i]
                            if self.money < 0:
                                print('<0 3')
                        else:
                            minpr.money += self.money
                            self.buy[i] += self.money / pricedict[minpr]
                            minpr.sell[i] -= self.money / pricedict[minpr]
                            self.money -= self.money
                            if self.money < 0:
                                print('<0 4')
                    if self.num_workers * self.usage[i] <= self.buy[i]:
                        flag1 = False
                    pricedict.pop(minpr)
                    if not pricedict:
                        flag1 = False
                    if self.money == 0:
                        flag1 = False
        if self.money < 0:
            print('<0 BUY')

    def factboostbuy(self):
        """то же самое, только теперь покупается бустер"""
        roadcoef = 0.1
        summa = 0
        for qwe in self.effectiveness:
            summa += self.effectiveness[qwe] * (1 + self.bonuses[qwe])
        for i in self.booster:
            pricedict = goods.Goods.gddict[i].prices.copy()
            for j in pricedict:
                pricedict[j] = pricedict[j] * (
                            1 + roadcoef * np.sqrt((j.location.area[0][0] - self.location.area[0][0]) ** 2 +
                                                   (j.location.area[0][1] - self.location.area[0][1]) ** 2))
            flag1 = True
            if self.type:
                condition = self.type
                money_sum = 0
                for work_iter in self.workers_dict:
                    money_sum += work_iter.money
            else:
                condition = self.money !=0
            if self.booster[i] < self.num_workers * self.boosterusage[i] and condition:       # and self.money != 0
                while flag1:
                    minpr = min(pricedict, key=pricedict.get)
                    """
                    тут ввожу, есть ли смысл покупать бустер производства. проверка:
                     цена бустера < (множитель_бустера - 1) * сумма(эффективность_пр-ва_i-го_товара * (1 + бонус_i)) / траты_бустера_на_ед-цу_товара
                     выкладки у меня на листике 
                    """
                    if pricedict[minpr] > (self.boosterbonus[i] - 1)* summa / self.boosterusage[i]:
                        break
                    if minpr.sell[i] >= self.num_workers * self.boosterusage[i]:
                        if self.money >= self.num_workers * self.boosterusage[i]*pricedict[minpr]:
                            minpr.money += pricedict[minpr] * self.num_workers * self.boosterusage[i]
                            self.money -= pricedict[minpr] * self.num_workers * self.boosterusage[i]
                            self.booster[i] += self.num_workers * self.boosterusage[i]
                            minpr.sell[i] -= self.num_workers * self.boosterusage[i]
                            print('BOOST1 enough')

                        elif self.type and money_sum + self.money >= self.num_workers * self.boosterusage[i]*pricedict[minpr]:
                            for work_iter in self.workers_dict:
                                work_iter.money -= work_iter.num * self.boosterusage[i]*pricedict[minpr] - self.money * work_iter.num / self.num_workers
                            self.money += self.num_workers * self.boosterusage[i]*pricedict[minpr] - self.money

                            minpr.money += pricedict[minpr] * self.num_workers * self.boosterusage[i]
                            self.money -= pricedict[minpr] * self.num_workers * self.boosterusage[i]
                            self.booster[i] += self.num_workers * self.boosterusage[i]
                            minpr.sell[i] -= self.num_workers * self.boosterusage[i]
                            print('BOOST enough')
                        elif self.type and money_sum + self.money < self.num_workers * self.boosterusage[i]*pricedict[minpr]:
                            self.money += money_sum
                            for work_iter in self.workers_dict:
                                work_iter.money = 0
                            minpr.money += self.money
                            self.booster[i] += self.money / pricedict[minpr]
                            minpr.sell[i] -= self.money / pricedict[minpr]
                            self.money -= self.money
                            print('BOOST NOT enough')

                        elif not self.type:
                            minpr.money += self.money
                            self.booster[i] += self.money / pricedict[minpr]
                            minpr.sell[i] -= self.money / pricedict[minpr]
                            self.money -= self.money
                            print('BOOST 2enough')

                    else:
                        if self.money >= pricedict[minpr] * minpr.sell[i]:
                            minpr.money += pricedict[minpr] * minpr.sell[i]
                            self.money -= pricedict[minpr] * minpr.sell[i]
                            self.booster[i] += minpr.sell[i]
                            minpr.sell[i] -= minpr.sell[i]
                            print('BOOST 3enough')

                        elif self.type and money_sum + self.money >= pricedict[minpr] * minpr.sell[i]:
                            for work_iter in self.workers_dict:
                                work_iter.money -= (work_iter.num * pricedict[minpr] * minpr.sell[i] - self.money * work_iter.num) / self.num_workers
                            self.money += pricedict[minpr] * minpr.sell[i] - self.money
                            minpr.money += pricedict[minpr] * minpr.sell[i]
                            self.money -= pricedict[minpr] * minpr.sell[i]
                            self.booster[i] += minpr.sell[i]
                            minpr.sell[i] -= minpr.sell[i]
                            print('BOOST4 enough')

                        elif self.type and money_sum + self.money < pricedict[minpr] * minpr.sell[i]:
                            self.money += money_sum
                            for work_iter in self.workers_dict:
                                work_iter.money = 0
                            minpr.money += self.money
                            self.booster[i] += self.money / pricedict[minpr]
                            minpr.sell[i] -= self.money / pricedict[minpr]
                            self.money -= self.money
                            print('BOOST55 enough')

                        elif not self.type:
                            minpr.money += self.money
                            self.booster[i] += self.money / pricedict[minpr]
                            minpr.sell[i] -= self.money / pricedict[minpr]
                            self.money -= self.money
                            print('BOOST6enough')

                    if self.num_workers * self.boosterusage[i] <= self.booster[i]:
                        flag1 = False
                    pricedict.pop(minpr)
                    if not pricedict:
                        flag1 = False
                    if self.money == 0:
                        flag1 = False

    def pricechange(self):
        """
        надо сделать такую систему: во-первых, если максимум продан - увеличивать цену и наоборот
        во-вторых, применить использование производных. если при изменении цены доходы упали, то сделать обратное изменение цены - хуйня не надо
        x, y          x', y'               х - продажи, у - цена, k - изменение цены
        y' = ky
        x'y' > xy
        x' > x/k - условие выгодности изменения цены при изменении продаж

        nuff said. эта схема тут и осуществлена
        :return:
        """

        for i in self.sell:
            if self.after_creation[i] == 0:
                continue
            if 1 - self.sell[i]/self.after_creation[i] > 0.9:
                self.good.prices[self] *= 1.1
                self.price_changed[i] = 1
            elif 1 - self.sell[i]/self.after_creation[i] < 0.5:
                self.good.prices[self] /= 1.1
                self.price_changed[i] = 2
        for i in self.sell:
            self.soldprevious[i] = self.after_creation[i] - self.sell[i]

    def pricechangeagain(self):
        """в зависимости от того, как изменилась цена в предыдущий раз, и как изменилась прибыль, либо продолжаем изменять
        цену в том же духе, либо наоборот"""
        for i in self.price_changed:
            if self.soldprevious[i] == 0:
                continue
            if self.price_changed[i] == 1:
                 if (self.after_creation[i] - self.sell[i])/self.soldprevious[i] > 1/1.1:
                     self.good.prices[self] *= 1.1
                     self.price_changed[i] = 1
                 else:
                     self.good.prices[self] /= 1.1
                     self.price_changed[i] = 2
            elif self.price_changed[i] == 2:
                 if (self.after_creation[i] - self.sell[i])/self.soldprevious[i] > 1.1:
                     self.good.prices[self] /= 1.1
                     self.price_changed[i] = 2
                 else:
                     self.good.prices[self] *= 1.1
                     self.price_changed[i] = 1
        for i in self.sell:
            self.soldprevious[i] = self.after_creation[i] - self.sell[i]

    def givefoodmoney(self):
        """
        суть такова. в main-е после покупки всего и вся, во время смены цены мы отдаём крестьянам деньги и еду
        в Main-e смотрим, завод ли это типа 1 (или типа True). если да то далее
        прогоняем по всем вещам, что крестьяне потребляют
        смотрим, есть ли у них достаточно еды, если достаточно, то хрен с ними
        :return:
        """
        if len(self.workers_dict.keys()) != 0 and self.num_workers != 0:
            for j in self.workers_dict:
                j.money += self.money * j.num / self.num_workers
            self.money = 0

            consum = self.workers_dict.keys()
            for worker_iter in consum:
                for key in worker_iter.cons:
                    if key in self.sell.keys() and self.sell[key] >= worker_iter.cons[key] * worker_iter.total_num*1.5:
                        if worker_iter.inventory[key] < worker_iter.cons[key] * worker_iter.total_num*1.5:                  # 1.5 - это просто на всякий случай коэффициент. если дети родятся, то чтоб не голодали
                            difference = worker_iter.cons[key] * worker_iter.total_num*1.5 - worker_iter.inventory[key]
                            worker_iter.inventory[key] = worker_iter.cons[key] * worker_iter.total_num*1.5
                            self.sell[key] -= difference


    def leavework(self, percent):
        shortname = self.location.pops
        not_found = True
        for workers_iter in self.workers_dict:
            for key in shortname:
                if workers_iter.culture == key.culture and workers_iter.religion == key.religion and workers_iter.strata == key.strata and key.unemployed == 1:
                    print('one same pop for factory LEAVEWORK found in ', self.location.name)
                    for i in range(len(self.male_age)):
                        key.male_age[i] += workers_iter.male_age[i] * percent
                        workers_iter.male_age[i] -= workers_iter.male_age[i] * percent
                        key.female_age[i] += workers_iter.female_age[i] * percent
                        workers_iter.female_age[i] -= workers_iter.female_age[i] * percent
                    key.money += workers_iter.money * percent
                    workers_iter.money -= workers_iter.money * percent
                    if workers_iter.num < 0:
                        print('DEBAG!!! POP-LEAVING < 0')

                    not_found = False
            if not_found:
                m_age = np.array(
                    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), dtype=np.uint16)
                f_age = np.array(
                    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), dtype=np.uint16)
                for i in range(len(workers_iter.male_age)):
                    m_age[i] = workers_iter.male_age[i] * percent
                    workers_iter.male_age[i] -= workers_iter.male_age[i] * percent
                    f_age[i] = workers_iter.female_age[i] *percent
                    workers_iter.female_age[i] -= workers_iter.female_age[i] * percent

                print('male', m_age, 'female', f_age)
                new_money = workers_iter.money * percent
                workers_iter.money -= workers_iter.money * percent
                pops.Pops(workers_iter.location, m_age.copy(), f_age.copy(), workers_iter.strata, workers_iter.culture, workers_iter.religion, new_money,1)
