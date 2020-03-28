"""ПЛАНЫ: дошкольное образование (т.е. для детей) напрямую усиливает ассимиляцию
        сделать тупо какую-нибудь аппроксимирующую функцию типа нормального распределения
        сделать ограничение реализации каких-либо социальных институтов: они доступны если есть открытие или
        у какой-нибудь страны это уже реализовано (надо тогда запрогать что-то типа "великого посольства")"""
import goods
import strata
import numpy as np

class Pops:
    """надо будет сделать (что, впрочем, не сильно сложно) преобразователь типов данных и везде  его повставлять
            для того, чтоб меньше место занимали отдельные массивы и экземпляры. ибо их будет НУ ОЧЕНЬ БЛЯТЬ МНОГО
            собственно
            1. надо ввести периодическую проверку всех или некоторых списков (например численность
                популяции) на отсутствие там чисел больше 255. если таких чисел нет, то преобразовать список
                в dtype = np.uint8
            2. надо ввести функцию, которая будет просматривать при добавлении значений к элементам таких списков,
                больше ли итоговое значение чем 255. если да, то преобразовать список в dtype = np.uint16
                ПРОБЛЕМА - а не дохуя ли станет вычислительной нагрузки?


            Ввести показатель мигрантов. т.е. если каких-то чуваков ПОКА мало, то обращатся с ними как часть статистики
            более крупной группы местных (чтоб для пары человек дохуя вещей не просчитывать и не хранить). потом, когда их станет приличное количество
            то уже можно создать им отдельный поп

            ПРОБЛЕМА многих попов - на каждом заводе будут свои мелкие подгруппы попов - слишком много вычислений
            и много хранить данных          (с другой стороны, обычно на город не более 10 заводов. и то в очень крупных городах)
            ПРОБЛЕМА одного общего попа - как рассчитывать тогда распределение благ? то есть например
            одни рабочие производят микросхемы, а другие дилдаки. понятно, что микросхемщики должны быть богаты
            а дилдаковщики должны сосать хуи
    """

    """
    как только попам не будет хватать денег на их основные блага (низшие классы) или часть более дорогих благ (выше
    процент для более высоких классов) то они будут увольняться, если есть где-нибудь лучше работа (сделать анализаторы)
    причём если более хорошая работа есть в другом городе, то лишь наиболее сознательные должны переезжать, остальные же
    только если работа есть в ЭТОМ городе
    """


    def __init__(self, location, male_age,female_age, strata,culture,religion, money, unemployed=0,consciousness = 0, realnye = True):


        self.location = location                     # прописька есть? пройдёмте, гражданин
        self.strata = strata
        self.culture = culture
        self.religion = religion
        #self.unemployment = unemployment
        self.consciousness = consciousness
        self.unemployed = unemployed
        self.employment = {} # тут надо будет сопоставлять объект-завод списку с долей рабочих, их деньгами, едой и тд (или еду с деньгами на завод?)
        # делаю сначала только число рабочих, без процентов и др.
        self.inventory = {'Grain': 0, 'Fish':0}          # что у попа есть
        #self.cons = {'Grain': 1,'Fish':1}                    # что попу надо потреблять
        self.male_age = male_age
        """np.array((0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,num/1,0,0,0,0,0,0,0,0,
                                  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                                  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0), dtype=np.uint16)"""               # сколько кого по возрастам мужиков
        self.female_age = female_age                  # баб

        #self.dispers = dispers                               # хуйня пока не пригодилась
        self.money = money            # деньги БЕЗРАБОТНОЙ ЧАСТИ ЭТОГО ПОПА
        self.real = realnye
        if realnye:                                  # для болванчиков не работает
            #location.population += self.num
            location.serfs = self                  # связываем этот поп с городским попом безработных (пока что такая система, раньше была другая)
            location.pops[self] = self                 # записываем в словарь экземпляра поселения, что в нём есть этот поп
            Pops.popchange(self)
        self.migrate = 0
        self.hungry = 0
        #self.num = 0
        self.total_num = sum(self.male_age) + sum(self.female_age)                       # вестимо суммарно

    # тут надо будет переделать рождение с коэффициентами по богатству
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
        после этого того, кого меньше, умножаем на коэффициент воспроизводства.
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

        """
        ПРОБЛЕМА НЕ В ТИНАХ, А В ТОМ, ЧТО ПРИ НАБОРЕ НАРОДА НА ЗАПОЛНЕННЫЙ ЗАВОД ТВОРИТСЯ ПИЗДЕЦ. ПРИЧЁМ ПОХОДУ НАРОД ПРОХОДИТ НА ЗАВОД БЕЗ
        КОНКУРСА, ДАЖЕ ПЕРЕД НИМ (похоже что устарело, т.е. это проблема старой системы, не новой)
        """
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
            if koef_male > 100:
                self.male_age[0] = (koef_male * rozhdaemost) / 2
                self.female_age[0] = self.male_age[0]
            else:
                r1 = np.random.sample(koef_male)
                r2 = sum(r1 < 0.2)   # тут надобно задать какую-нить функцию для сравнения, чтоб учесть сколько кто рожает (в зависимости от положения, образования, законов и так далее)
                self.male_age[0] += r2/2    # пока забью хуй и поставлю 20% шанс в год - в среднем рожали 6 раз в жизнь - т.е. с 15 до 45 лет
                self.female_age[0] += r2/2
        else:
            if koef_female > 100:
                self.male_age[0] = (koef_female * rozhdaemost) / 2
                self.female_age[0] = self.male_age[0]
            else:
                r1 = np.random.sample(koef_female)
                r2 = sum(r1 < 0.2)   # тут надобно задать какую-нить функцию для сравнения, чтоб учесть сколько кто рожает (в зависимости от положения, образования, законов и так далее)
                self.male_age[0] += r2/2    # пока забью хуй и поставлю 20% шанс в год - в среднем рожали 6 раз в жизнь - т.е. с 15 до 45 лет
                self.female_age[0] += r2/2
        self.male_age[74] = 0   # чтоб жалких старикашек точно добить. а то они не умирают и устраивают баги
        self.female_age[74] = 0
        self.total_num = sum(self.male_age) + sum(self.female_age)
        """тут в зависимости от законов считаем, кто годится в рабочие, a перед тем выпускаем "в жизнь" из
         семейного гнёздышка новую рабочую силу, чтобы она могла распределиться на другую работу"""

        # if not self.unemployed:
        #     if self.location.state.laws['Children_labour']:
        #         Pops.teen_go(self,10)
        #     else:
        #         Pops.teen_go(self, 18)


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



    # не будет ли проблемы, что процент будет каждый раз отсчитываться от уменьшающегося числа рабочих? нужно распределять
    # их всех вместе
    def facsearch(self):
        """поиск работы"""
        komu_skolko = {}
        for q in self.location.factories:
            if q.work_type == self.strata:          # подходит ли завод к распределяемому попу? ЭТО ДЕЛАЕТСЯ УЖЕ ВО ВТОРОЙ РАЗ, ПЕРВЫЙ - В MAIN
                raznost = self.location.factories[q].fullnum - self.location.factories[q].num_workers             # сколько завод может принять рабочих
                #gotovo = self.num*self.location.factories[q].coef                 # сколько рабочих готово на НЕГО идти (в соответствии с коэффициентом)
                #for ikey in self.employment:
                prol_sum = sum(self.employment.values())    # считаем, сколько всего людей в попе уже работает
                gotovo = (self.num - prol_sum) * self.location.factories[q].coef
                """рассматриваем разные варианты: готов ли принять завод столько рабочих?
                перемещаются в поп завода, кстати, рабочие прямо с детьми и жёнами"""
                #shortname = self.location.factories[q].workers_dict
                not_found = True

                if self in self.location.factories[q].workers_dict:

                    if raznost >= gotovo:
                        #self.employment[self.location.factories[q]] += gotovo
                        komu_skolko[self.location.factories[q]] = gotovo

                    else:
                        komu_skolko[self.location.factories[q]] = raznost
                    not_found = False
                if not_found:
                    if raznost >= gotovo:
                        komu_skolko[self.location.factories[q]] = gotovo
                        self.location.factories[q].workers_dict[self] = True
                        self.employment[ self.location.factories[q]] = 0
                    else:
                        komu_skolko[self.location.factories[q]] = raznost
                        self.location.factories[q].workers_dict[self] = True
                        self.employment[self.location.factories[q]] = 0
        for q in komu_skolko:
            self.employment[q] += komu_skolko[q]

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
        obj = strata.Strata.strSlovar[self.strata]
        workers = sum(self.employment.values())

        bezdelniki = self.total_num * (1 - workers / self.num)
        quant123 = 0
        fooddict = obj.cons.copy()         # копируем словарь того, что поп в принципе может жрать
        notfound123 = True                   # вспомогательная штука для выхода из цикла вайл
        for i in obj.cons:                  # пересчитываем, что в инвентаре вообще есть пожрать
            if self.inventory[i] > 0:
                quant123 += 1
            else:
                fooddict.pop(i)                  # если чего-то нет, то мы удаляем это из скопированного словаря

        if quant123 == 0:                        # если нихуя нет пожрать, то дохнут
            for q in range(len(self.male_age)):
                self.male_age[q] -= int(0.05 * self.male_age[q] * (1 - workers / self.num))
                self.female_age[q] -= int(0.05 * self.female_age[q] * (1 - workers / self.num))

        else:
            while notfound123:   # распределяем жрачку по потреблению. чтоб съел либо 1 буханку хлеба, либо полбуханки и полпалки колбасы, либо треть одного, треть второго и треть третьего продукта
                fooddict, quant123, notfound123 = Pops.consume_exclude(self,fooddict,quant123,obj,bezdelniki)
                if quant123 == 0:
                    eaten = 0
                    for i in obj.cons:
                        if self.inventory[i] > 0:
                            eaten += self.inventory[i]/(bezdelniki * obj.cons[i])
                            self.inventory[i] = 0
                            self.die = min(self.hungry,1 - eaten)          # если какая-то часть населения дважды не ела, то она частично сдохнет и частично уебёт
                            #emigrate = 0
                            if self.die != 0:
                                for q in range(len(self.male_age)):
                                    self.male_age[q] -= int(self.die*self.male_age[q]*0.05*(1 - workers / self.num))
                                    self.female_age[q] -= int(self.die*self.female_age[q]*0.05*(1 - workers / self.num))
                                    #emigrate += self.die*(self.male_age[q] + self.female_age[q])* 0.95
                            self.emigrate = self.die * self.total_num * 0.95*(1 - workers / self.num)
                            self.hungry = 1 - eaten                             # но так-то можно сделать и трижды, и четырежды и т.д.

                            #Pops.migration(self)                               # тут тип если еда есть, но недостаточно
                                                                                # тогда эмиграция или ещё что. пока не продумал до конца



                elif notfound123 == False:                   # если нашли достаточно продуктов для потребления - стопаем цикл и жрём
                    for i in fooddict:
                        self.inventory[i] -= (bezdelniki * obj.cons[i])/quant123

    def consume_exclude(self,fooddict,quant123,obj,bezdelniki):
        """вспомогательная функция для исключения того, чего слишком мало для пожирания"""
        qu123 = quant123
        notfound123 = True
        for i in list(fooddict):
            if self.inventory[i] < (bezdelniki * obj.cons[i])/quant123:
                quant123 -= 1
                fooddict.pop(i)
        if qu123 == quant123:
            notfound123 = False
        return fooddict, quant123, notfound123

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

        roadcoef = 0.1
        obj = strata.Strata.strSlovar[self.strata]
        workers = sum(self.employment.values())

        bezdelniki = self.total_num * (1 - workers / self.num)
        for i in obj.cons:
            pricedict = goods.Goods.gddict[i].prices.copy()
            for j in pricedict:
                pricedict[j] = pricedict[j] * (1 + roadcoef * np.sqrt((j.location.area[0][0] - self.location.area[0][0])**2 +
                                                 (j.location.area[0][1] - self.location.area[0][1])**2))

            flag1 = True
            if self.inventory[i] < obj.cons[i] * bezdelniki and self.money > 0:
                while flag1:
                    minpr = min(pricedict, key=pricedict.get)
                    #buylist.append(minpr)
                    if minpr.sell[i] >= obj.cons[i]*bezdelniki:
                        if self.money >= pricedict[minpr]*obj.cons[i]*bezdelniki:
                            minpr.money += pricedict[minpr]*obj.cons[i]*bezdelniki
                            self.money -= pricedict[minpr]*obj.cons[i]*bezdelniki
                            self.inventory[i] += obj.cons[i]*bezdelniki
                            minpr.sell[i] -= obj.cons[i]*bezdelniki
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
                    if obj.cons[i]*bezdelniki <= self.inventory[i]:
                        flag1 = False
                    pricedict.pop(minpr)
                    if not pricedict:
                        flag1 = False
                    if self.money == 0:
                        flag1 = False


    def emigration(self):
        #analiser plus make for
        print('govno')

    """
    def teen_go(self,age):
        shortname = self.location.pops
        not_found = True
        #for workers_iter in self.location.workers_dict:
        if self.male_age[age] > 0 or self.female_age[age] > 0:
            for key in shortname:
                if self.culture == key.culture and self.religion == key.religion and self.strata == key.strata and key.unemployed == 1:
                    print('one same pop for factory YOUTH LEAVEWORK found in ', self.location.name)
                    key.money += self.money *(self.male_age[age]+self.female_age[age])/self.total_num
                    self.money -= self.money *(self.male_age[age]+self.female_age[age])/self.total_num
                    key.male_age[age-1] += self.male_age[age]
                    self.male_age[age] -= self.male_age[age]
                    key.female_age[age-1] += self.female_age[age]
                    self.female_age[age] -= self.female_age[age]
                    print('НЕРАБОТАЮЩЕЕ НАСЕЛЕНИЕ',key.male_age)
                    print(self.total_num)
                    print(self.num)
                    print(key==self)


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

                new_money = self.money *(self.male_age[age]+self.female_age[age])/self.total_num
                self.money -= self.money *(self.male_age[age]+self.female_age[age])/self.total_num
                m_age[age] = self.male_age[age]
                self.male_age[age] -= self.male_age[age]
                f_age[age] = self.female_age[age]
                self.female_age[age] -= self.female_age[age]

                Pops(self.location, m_age.copy(), f_age.copy(), self.strata, self.culture,
                          self.religion, new_money, 1)
    """

    def leavework_high_demands(self):
        #consciousness, compare money for food and gehalt, change verteilung if gehalt too low (should i?)
        print('govno')










    #def buying(self):



"""     def __init__(self, location, strata, num, culture, religion, literacy, unemployment, agr, consciousness, patriotism,
                 needs_v, goods_v, desire_v, polit_v, dispers, money, birth):

        self.num = num
        self.culture = culture
                self.religion = religion

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