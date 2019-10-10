"""
сделать коррекцию количества производства - а надо ли это делать? пускай по максимуму производят и удешевляют товар
"""

import random
import goods
import pops
import numpy as np


class Factory:
    Fact_number = 0
    slovar = dict()                          # словарь всех заводов. вот только нахуя?

    def __init__(self, location, work_type, good, money,gehalt,fullnum, num_workers = 0,type=0):
        self.location = location                         # где завод располагается, в каком городе
        self.work_type = work_type                               # чей труд применяется? крестьян? рабочих? учителей?
        self.num_workers = num_workers                           # количество уже нанятых трудяг
        self.workers = pops.Pops(location,0,work_type,1.0,0,0)               # создаём для этих трудяг отдельный поп
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
            self.range = 10

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

    def buying(self):
        """
        УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
        УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
        УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
        УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
        УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
        УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
        найдено: словарь с номерами 5 дешёвых заводов и с ценами там
        надо сделать: определить порядок покупки
        проверить суммарную достаточность наличия товаров
            если не достаточно, то искать дальше, пока не будет достаточно
                в этом случае скупить с дешёвых всё подчистую, а с добавленного докупить нехватку
            если вообще мало соответствующих заводов, то покупать с <5
                тогда вестимо всё подчистую
        найти проценты и проверить отдельные достаточности
            если в отдельных маловато, то нехватку купить у самого дешёвого (или распределить?)
        если всё получилось - купить]


        учесть отсутствие товаров у некоторых продавцов
        учесть отсутствие товаров в целом
        для этого можно в начале посчитать сумму мировых запасов и если на этой итерации они кончились,
        то не продолжать покупки

        потом учесть эмбарго и подобное

        учесть нерентабельность покупки и неполноту производства - соответственно неполноту оплаты трудящимся
        а после нескольких циклов неоплаты они уходят, а лучше посчитать, сколько раз в году им не заплатили
        и если больше N, то попы уходят с завода
        :return:
        """
        for key in self.usage:
            cnt = 0
            pricedict = self.good.prices.copy()
            buylist = []
            flag1 = True
            flag2 = True
            while flag1:
                buylist.append(min(pricedict, key=pricedict.get))
                pricedict.pop(buylist[cnt])
                sum123 = 0
                for i in range(len(buylist)):
                    sum123 += Factory.slovar[buylist[i]].sell[key]
                if sum123 < self.usage[key]*self.num_workers:
                    cnt += 1
                else:
                    flag1 = False
            minus123 = 0
            for i in range(len(buylist)-1):
                minus123 += Factory.slovar[buylist[i]].sell[key]
                Factory.slovar[buylist[i]].sell[key] = 0
                Factory.slovar[buylist[len(buylist)]].sell[key] -= self.usage[key]*self.num_workers - minus123 #сдвинуть надо эту хуйню на 1 таб назад







                while flag2:
                    minimal123 = min(pricedict, key=pricedict.get)
                    for k, v in pricedict.items():
                        if v == minimal123:
                            buylist[k] = minimal123
                            pricedict.pop(k)
                            cnt += 1
                sum123 = 0
                for key1 in buylist:
                    sum123 += Factory.slovar[key1].sell[key]
                if sum123 >= self.usage[key]*self.num_workers:
                    sumcube = 0
                    for ab in buylist:
                        sumcube += buylist[ab]**3
                    for ab in buylist:
                        self.buyingcoef[ab] = (buylist[ab]**3)/sumcube

    def facbuy(self):
        """
        УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
        УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
        УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
        УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
        УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
        УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
        покупаем у самого дешёвого
        если не хватает - у второго самого дешёвого и так далее
        :return:
        """
        for key in self.usage:
            cnt = 0
            pricedict = self.good.prices.copy()
            buylist = {}
            flag1 = True
            while flag1:
                while cnt <5:
                    minimal123 = min(pricedict.values())
                    for k, v in pricedict.items():
                        if v == minimal123:
                            buylist[k] = minimal123
                            pricedict.pop(k)
                sum123 = 0
                for key1 in buylist:
                    sum123 += Factory.slovar[key1].sell[key]
                if sum123 >= self.usage[key]*self.num_workers:
                    sumcube = 0
                    for ab in buylist:
                        sumcube += buylist[ab]**3
                    for ab in buylist:
                        self.buyingcoef[ab] = (buylist[ab]**3)/sumcube

    def prodtoserf(self):
        """
               УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
               УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
               УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
               УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
               УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
               УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET"""
        for i in self.sell:
            self.workers.inventory[i] += 1

    def serf_winter(self):
        """
                       УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
                       УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
                       УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
                       УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
                       УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET
                       УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET УСТАРЕЛО OUTDATED VERALTET"""
        if 'Serf' in self.location.pops:
            sumoffood = 0
            for i in self.location.pops['Serf'].cons:
                sumoffood += self.location.pops['Serf'].inventory[i]
            print('Serf_Food, ', self.location.name ,sumoffood)
            if sumoffood < 300:
                for i in self.location.pops['Serf'].cons:
                    if i in self.sell:
                        self.location.pops['Serf'].inventory[i] += self.sell[i]
                        self.sell[i] = 0
            print(self.location.pops['Serf'].inventory, ', inventory of serfs in', self.location.name)

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
            self.effectiveness['Fertilizer'] = 1
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
        if self.fullnum == self.workers.num:
            self.coef = 0
            self.notfull = 0
            print('factory in ',self.location.name,' is FULL')
        else:
            self.coef = (self.gehalt ** 3) / self.location.gehsum[self.work_type.name]
            self.notfull = 1

    def create(self):
        """производство товаров

        по сути просто смотрится, каковы условия работы (есть ли деньги платить людям, хватает ли ресурсов на производство
        есть ли бустеры, нужно ли вообще что-либо из закупочных ресурсов или всё достаём из земли и так далее и тому подобное)
        а потом в соответствии с этими условиями тратится всё, что нужно/есть и производится товар. а деньги (зарплата) выплачиваются
        попу
        """

        whatisdone = {}
        if len(self.buy) != 0:
            if self.money >= self.workers.num * self.gehalt:
                keysell = random.choice(list(self.buy.keys()))
                if self.buy[keysell] >= self.workers.num * self.usage[keysell]:
                    for key in self.buy:
                        self.buy[key] -= self.workers.num * self.usage[key]
                    for key in self.sell:
                        whatisdone[key] = self.workers.num * self.effectiveness[key] * (1 + self.bonuses[key])
                    for key in self.booster:
                        if self.booster[key] >= self.workers.num * self.boosterusage[key]:
                            self.booster[key] -= self.workers.num * self.boosterusage[key]
                            for key1 in self.sell:
                                whatisdone[key1] *= self.boosterbonus[key]
                    for key1 in self.sell:
                        self.sell[key1] += whatisdone[key1]
                self.money -= self.workers.num * self.gehalt
                self.workers.money += self.workers.num * self.gehalt
            else:
                if self.money >0:
                    keysell = random.choice(list(self.buy.keys()))
                    if self.buy[keysell] >= self.usage[keysell] * self.money/self.gehalt:
                        for key in self.buy:
                            self.buy[key] -= self.usage[key] * self.money/self.gehalt
                        for key in self.sell:
                            whatisdone[key] = self.effectiveness[key] * (1 + self.bonuses[key]) * self.money/self.gehalt
                        for key in self.booster:
                            if self.booster[key] >= self.boosterusage[key] * self.money/self.gehalt:
                                self.booster[key] -= self.boosterusage[key] * self.money/self.gehalt
                                for key1 in self.sell:
                                    whatisdone[key1] *= self.boosterbonus[key]
                        for key1 in self.sell:
                            self.sell[key1] += whatisdone[key1]
                    self.workers.money += self.money
                    self.money -= self.money
        else:
            if self.money >= self.workers.num * self.gehalt:
                self.money -= self.workers.num * self.gehalt
                self.workers.money += self.workers.num * self.gehalt
                for key in self.sell:
                    whatisdone[key] = self.workers.num * self.effectiveness[key] * (1 + self.bonuses[key])
                for key in self.booster:
                    if self.booster[key] >= self.workers.num * self.boosterusage[key]:
                        self.booster[key] -= self.workers.num * self.boosterusage[key]
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
                    self.workers.money += self.money
                    self.money -= self.money
        self.after_creation = self.sell.copy()
        if self.money < 0:
            print('<0 CREATE')

    def factbuy(self):
        """покупка необходимых ресурсов для производства

        погляди этот же процесс описан для попов - popbuy
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
            print('Pricedict is ', pricedict)
            flag1 = True
            if self.buy[i] < self.workers.num * self.usage[i] and self.money != 0:
                while flag1:
                    minpr = min(pricedict, key=pricedict.get)
                    if minpr.sell[i] >= self.workers.num * self.usage[i]:
                        if self.money >= self.workers.num * self.usage[i]:
                            minpr.money += pricedict[minpr] * self.workers.num * self.usage[i]
                            self.money -= pricedict[minpr] * self.workers.num * self.usage[i]
                            self.buy[i] += self.workers.num * self.usage[i]
                            minpr.sell[i] -= self.workers.num * self.usage[i]
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
                    if self.workers.num * self.usage[i] <= self.buy[i]:
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
        for i in self.booster:
            if self.good.name == 'Fish':
                print('FISHBUYBOOST')
            pricedict = goods.Goods.gddict[i].prices.copy()
            for j in pricedict:
                pricedict[j] = pricedict[j] * (
                            1 + roadcoef * np.sqrt((j.location.area[0][0] - self.location.area[0][0]) ** 2 +
                                                   (j.location.area[0][1] - self.location.area[0][1]) ** 2))
            flag1 = True
            if self.booster[i] < self.workers.num * self.boosterusage[i] and self.money != 0:
                while flag1:
                    minpr = min(pricedict, key=pricedict.get)
                    if minpr.sell[i] >= self.workers.num * self.boosterusage[i]:
                        if self.money >= self.workers.num * self.boosterusage[i]:
                            minpr.money += pricedict[minpr] * self.workers.num * self.boosterusage[i]
                            self.money -= pricedict[minpr] * self.workers.num * self.boosterusage[i]
                            self.booster[i] += self.workers.num * self.boosterusage[i]
                            minpr.sell[i] -= self.workers.num * self.boosterusage[i]
                        else:
                            minpr.money += self.money
                            self.booster[i] += self.money / pricedict[minpr]
                            minpr.sell[i] -= self.money / pricedict[minpr]
                            self.money -= self.money
                    else:
                        if self.money >= pricedict[minpr] * minpr.sell[i]:
                            minpr.money += pricedict[minpr] * minpr.sell[i]
                            self.money -= pricedict[minpr] * minpr.sell[i]
                            self.booster[i] += minpr.sell[i]
                            minpr.sell[i] -= minpr.sell[i]
                        else:
                            minpr.money += self.money
                            self.booster[i] += self.money / pricedict[minpr]
                            minpr.sell[i] -= self.money / pricedict[minpr]
                            self.money -= self.money
                    if self.workers.num * self.boosterusage[i] <= self.booster[i]:
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