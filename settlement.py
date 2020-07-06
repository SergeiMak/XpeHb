import numpy as np
import pygame as pg
import pops
import strata
import random
import factory
#import state


class Settlement:
    Settl_number = 0   # количество поселений в мире
    arry = []           # список с прямоугольниками городов. чтоб можно было на них наводить и нажимать на карте
    slovar = dict()            # словарь всех городов мира


    def __init__(self,state, coordinates, mm, name, facnum = 0, size=1):
        self.size = size           # размер города. город будет расти на карте мира. алгоритм уже придумал. руки просто не дошли написать
        mm[coordinates] = 2        # переписываем в координатах города биом основной карты, чтобы сменить биом на городской (и отрисовать это)
        self.area = []             # список с координатами точек города. нужно для его роста на карте
        self.possible_area = []
        self.grain_fields = []                          ##### тут сделать всё uint16
        self.possible_grain_fields = []
        self.already_calculated = []
        self.area.append([coordinates[0],coordinates[1]])          # собсна добавляем первую точку
        Settlement.check_surroundings(self,(self.area[0][0],self.area[0][1]),mm,self.possible_area)
        Settlement.check_surroundings_city(self, (self.area[0][0], self.area[0][1]), mm, self.possible_grain_fields)
        self.name = name
        self.rectangle = pg.Rect((coordinates[0]-2,coordinates[1]-2),(5,5))            # прямоугольник города для глобальной карты
        self.factories = {}                # все заводы города
        self.facnum = facnum               # количество заводов в городе
        #self.serfs_unemployed = serfs      # безработные крестьяне. для каждого завода создаётся свой поп. в него перераспределяются ЭТИ попы, когда находят работу
        #self.schoolers = pops.Pops(self,0,schoolers,1,0,1)
        self.pops = {}                     # словарь всех попов этого города

        sumcube = 0                        # подсчёт нормировки для распределения по заводам безработных. распределяются в соответствии с кубами зарплат
        for w in self.factories:               # gehalt - зарплата
            sumcube += self.factories[w].gehalt*self.factories[w].gehalt*self.factories[w].gehalt
        self.gehsum = {'Serf':0,'Worker':0}            # надо было для пересчёта коэффициентов. уже не помню точно. зачем

        self.number = Settlement.Settl_number
        Settlement.Settl_number  += 1
        Settlement.arry.append([self.rectangle,self.number])
        Settlement.slovar[self.name] = self
        self.population = 0
        self.city = False
        self.state = state                         # принадлежность государству
        state.settlements.append(self)             # записываем в словарь городов этого государства
        

        state.settlements_for_opt[state.last_added_settl_day - 1].append(self)
        state.last_added_settl_day += 1
        if state.last_added_settl_day == 8:
            state.last_added_settl_day = 1


    def stlpopul(self):
        """перепись населения. т.е. суммарное население на данный момент"""
        self.population = 0
        for i in self.pops:
            self.population += i.total_num

    def summakubow(self):
        """подсчёт нормировки для распределения по заводам безработных. распределяются в соответствии с кубами зарплат"""
        sumcube = 0
        for strata1 in self.state.strats:
            for w in self.factories:
                if w.work_type.name == strata1.name:
                    sumcube += self.factories[w].gehalt*self.factories[w].gehalt*self.factories[w].gehalt * self.factories[w].notfull
            self.gehsum[strata1.name] = sumcube
        for w in self.factories:
            factory.Factory.coef(w)

    def if_not_full(self):
        for i in self.factories:
            if i.fullnum > i.num_workers:
                i.notfull = 1
            else:
                i.notfull = 0

    def display_inform(self):
        print('Number: {}. Name: {}'.format(self.number, self.name))

    def check_surroundings(self,coordinates,mm,possible_list):
        if mm[coordinates[0] - 1, coordinates[1]] != 0 and mm[coordinates[0] - 1, coordinates[1]] != 2 and mm[coordinates[0] - 1, coordinates[1]] != 5:
            if (coordinates[0] - 1, coordinates[1]) not in possible_list:
                possible_list.append((coordinates[0] - 1, coordinates[1]))

        if mm[coordinates[0] + 1, coordinates[1]] != 0 and mm[
            coordinates[0] + 1, coordinates[1]] != 2 and mm[
            coordinates[0] + 1, coordinates[1]] != 5:
            if (coordinates[0] + 1, coordinates[1]) not in possible_list:
                possible_list.append((coordinates[0] + 1, coordinates[1]))

        if mm[coordinates[0], coordinates[1] - 1] != 0 and mm[
            coordinates[0], coordinates[1] - 1] != 2 and mm[
            coordinates[0], coordinates[1] - 1] != 5:
            if (coordinates[0], coordinates[1] - 1) not in possible_list:
                possible_list.append((coordinates[0], coordinates[1] - 1))

        if mm[coordinates[0], coordinates[1] + 1] != 0 and mm[
            coordinates[0], coordinates[1] + 1] != 2 and mm[
            coordinates[0], coordinates[1] + 1] != 5:
            if (coordinates[0], coordinates[1] + 1) not in possible_list:
                possible_list.append((coordinates[0], coordinates[1] + 1))

    def check_surroundings_city(self,coordinates,mm,possible_list):
        if mm[coordinates[0] - 1, coordinates[1]] != 0 and mm[coordinates[0] - 1, coordinates[1]] != 2:
            if (coordinates[0] - 1, coordinates[1]) not in possible_list:
                possible_list.append((coordinates[0] - 1, coordinates[1]))

        if mm[coordinates[0] + 1, coordinates[1]] != 0 and mm[
            coordinates[0] + 1, coordinates[1]] != 2:
            if (coordinates[0] + 1, coordinates[1]) not in possible_list:
                possible_list.append((coordinates[0] + 1, coordinates[1]))

        if mm[coordinates[0], coordinates[1] - 1] != 0 and mm[
            coordinates[0], coordinates[1] - 1] != 2:
            if (coordinates[0], coordinates[1] - 1) not in possible_list:
                possible_list.append((coordinates[0], coordinates[1] - 1))

        if mm[coordinates[0], coordinates[1] + 1] != 0 and mm[
            coordinates[0], coordinates[1] + 1] != 2:
            if (coordinates[0], coordinates[1] + 1) not in possible_list:
                possible_list.append((coordinates[0], coordinates[1] + 1))


    def check_to_delete(self,coordinates,mm):
        """
        потом нужно будет для удаления потенциальных точек установки посевных полей. это сделаю тогда, когда дойдут руки
        до "соприкосновения территорий городов"
        :param coordinates:
        :param mm:
        :return:
        """
        if mm[coordinates[0] - 1, coordinates[1]] != 0 and mm[coordinates[0] - 1, coordinates[1]] != 2 and mm[coordinates[0] - 1, coordinates[1]] != 5:
            if (coordinates[0] - 1, coordinates[1]) not in self.possible_grain_fields:
                self.possible_grain_fields.append((coordinates[0] - 1, coordinates[1]))
            if (coordinates[0] - 1, coordinates[1]) not in self.possible_area:
                self.possible_area.append((coordinates[0] - 1, coordinates[1]))

        if mm[coordinates[0] + 1, coordinates[1]] != 0 and mm[
            coordinates[0] + 1, coordinates[1]] != 2 and mm[
            coordinates[0] + 1, coordinates[1]] != 5:
            if (coordinates[0] + 1, coordinates[1]) not in self.possible_grain_fields:
                self.possible_grain_fields.append((coordinates[0] + 1, coordinates[1]))
            if (coordinates[0] + 1, coordinates[1]) not in self.possible_area:
                self.possible_area.append((coordinates[0] + 1, coordinates[1]))

        if mm[coordinates[0], coordinates[1] - 1] != 0 and mm[
            coordinates[0], coordinates[1] - 1] != 2 and mm[
            coordinates[0], coordinates[1] - 1] != 5:
            if (coordinates[0], coordinates[1] - 1) not in self.possible_grain_fields:
                self.possible_grain_fields.append((coordinates[0], coordinates[1] - 1))
            if (coordinates[0], coordinates[1] - 1) not in self.possible_area:
                self.possible_area.append((coordinates[0], coordinates[1] - 1))

        if mm[coordinates[0], coordinates[1] + 1] != 0 and mm[
            coordinates[0], coordinates[1] + 1] != 2 and mm[
            coordinates[0], coordinates[1] + 1] != 5:
            if (coordinates[0], coordinates[1] + 1) not in self.possible_grain_fields:
                self.possible_grain_fields.append((coordinates[0], coordinates[1] + 1))
            if (coordinates[0], coordinates[1] + 1) not in self.possible_area:
                self.possible_area.append((coordinates[0], coordinates[1] + 1))


    def city_growth(self,mm,background,gm):
        if self.population > 5000*self.size:
            self.size  += 1
            if self.size > 3:
                self.city = True
            """newlands = []
            for i in range(len(self.area)):
                if mm[self.area[i][0]-1,self.area[i][1]] != 0 and mm[self.area[i][0]-1,self.area[i][1]] != 2:           # и надо будет позже ещё учесть горы и иные биомы
                    newlands.append((self.area[i][0]-1,self.area[i][1]))

                if mm[self.area[i][0]+1,self.area[i][1]] != 0 and mm[self.area[i][0]+1,self.area[i][1]] != 2:
                    newlands.append((self.area[i][0]+1,self.area[i][1]))

                if mm[self.area[i][0],self.area[i][1]-1] != 0 and mm[self.area[i][0],self.area[i][1]-1] != 2:
                    newlands.append((self.area[i][0],self.area[i][1]-1))

                if mm[self.area[i][0],self.area[i][1]+1] != 0 and mm[self.area[i][0],self.area[i][1]+1] != 2:
                    newlands.append((self.area[i][0],self.area[i][1]+1))"""
            if self.possible_area:
                randchoice = random.choice(self.possible_area)
                if mm[randchoice[0],randchoice[1]] == 5 and [randchoice[0],randchoice[1]] in self.grain_fields:
                    index123 = self.grain_fields.index([randchoice[0],randchoice[1]])
                    del self.grain_fields[index123]

                mm[randchoice[0],randchoice[1]] = 2
                self.area.append([randchoice[0],randchoice[1]])
                background.set_at((randchoice[0],randchoice[1]), (50, 50, 50))
                Settlement.check_surroundings_city(self, randchoice, mm, self.possible_area)
                index1 = self.possible_area.index(randchoice)
                del self.possible_area[index1]
            """ОПОСЛЯ ЭТОГО НАДО ПРОВЕРИТЬ НАЛИЧИЕ ДРУГИХ ГОРОДОВ ПО СОСЕДСТВУ С 
            НОВОЙ КЛЕТКОЙ И ЕСЛИ ТАКОЙ ГОРОД ЕСТЬ, ТО ИХ НУЖНО СОЕДИНИТь"""
        for i in self.factories:
            if i.good.name == 'Grain':
                if i.serf_average_effectiveness >= self.state.serf_land_right_per_capita and self.state.serf_land_right_per_capita:
                    if len(self.grain_fields) < i.num_workers*self.state.serf_land_right_per_capita:# тут надо очень внимательно смотреть на коэффициенты. переделать скорее всего
                        for diff in range(int(round(i.num_workers*self.state.serf_land_right_per_capita - len(self.grain_fields) + 0.5))): # округляем в бОльшую сторону
                            if self.possible_grain_fields:
                                res_max = -1
                                for res_gm in self.possible_grain_fields:
                                    if gm[res_gm] > res_max:
                                        resource_coord = res_gm
                                        res_max = gm[res_gm]

                                mm[resource_coord] = 5
                                self.grain_fields.append(resource_coord)
                                Settlement.check_surroundings(self,resource_coord,mm,self.possible_grain_fields)
                                background.set_at(resource_coord, (120, 150, 0))
                                index1 = self.possible_grain_fields.index(resource_coord)
                                del self.possible_grain_fields[index1]
                    elif self.grain_fields:
                        to_delete = int(
                            round(len(self.grain_fields) - i.num_workers * self.state.serf_land_right_per_capita))
                        for delete in range(to_delete):
                            res_min = 1000
                            for res_gm in self.grain_fields:
                                if gm[res_gm] < res_min:
                                    resource_coord = res_gm
                                    res_min = gm[res_gm]
                            mm[resource_coord] = 1
                            self.possible_grain_fields.append(resource_coord)
                            index1 = self.grain_fields.index(resource_coord)
                            del self.grain_fields[index1]
                            background.set_at(resource_coord, (0, 90, 0))

                else:
                    if len(self.grain_fields) < i.num_workers * i.serf_average_effectiveness:
                        for diff in range(int(round(i.num_workers * i.serf_average_effectiveness - len(
                                self.grain_fields) + 0.5))):  # округляем в бОльшую сторону
                            if self.possible_grain_fields:
                                res_max = -1
                                for res_gm in self.possible_grain_fields:
                                    if gm[res_gm] > res_max:
                                        resource_coord = res_gm
                                        res_max = gm[res_gm]

                                mm[resource_coord] = 5
                                self.grain_fields.append(resource_coord)
                                Settlement.check_surroundings(self, resource_coord, mm,self.possible_grain_fields)
                                background.set_at(resource_coord, (120, 150, 0))
                                index1 = self.possible_grain_fields.index(resource_coord)
                                del self.possible_grain_fields[index1]




