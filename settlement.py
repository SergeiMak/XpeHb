import numpy as np
import pygame as pg
import pops
import random
#import state


class Settlement:
    Settl_number = 0   # количество поселений в мире
    arry = []           # список с прямоугольниками городов. чтоб можно было на них наводить и нажимать на карте
    slovar = dict()            # словарь всех городов мира


    def __init__(self,state, coordinates, mm, name, serfs,schoolers, facnum = 0, size=1):
        self.size = size           # размер города. город будет расти на карте мира. алгоритм уже придумал. руки просто не дошли написать
        mm[coordinates] = 2        # переписываем в координатах города биом основной карты, чтобы сменить биом на городской (и отрисовать это)
        self.area = []             # список с координатами точек города. нужно для его роста на карте
        self.area.append([coordinates[0],coordinates[1]])          # собсна добавляем первую точку
        self.name = name
        self.rectangle = pg.Rect((coordinates[0]-1,coordinates[1]-1),(3,3))            # прямоугольник города для глобальной карты
        self.factories = {}                # все заводы города
        self.facnum = facnum               # количество заводов в городе
        self.serfs_unemployed = serfs      # безработные крестьяне. для каждого завода создаётся свой поп. в него перераспределяются ЭТИ попы, когда находят работу
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
        self.state = state                         # принадлежность государству
        state.settlements[self] = self             # записываем в словарь городов этого государства


    def stlpopul(self):
        """перепись населения. т.е. суммарное население на данный момент"""
        self.population = 0
        for i in self.pops:
            self.population += i.total_num

    def summakubow(self, pop1):
        """подсчёт нормировки для распределения по заводам безработных. распределяются в соответствии с кубами зарплат"""
        sumcube = 0
        for w in self.factories:
            if w.work_type == pop1.strata:
                sumcube += self.factories[w].gehalt*self.factories[w].gehalt*self.factories[w].gehalt * self.factories[w].notfull
        self.gehsum[pop1.strata.name] = sumcube

    def display_inform(self):
        print('Number: {}. Name: {}'.format(self.number, self.name))


    def city_growth(self, mm):
        """пока не сделано"""
        if self.population > 5000*self.size:
            self.size  += 1
            newlands = []
            for i in range(len(self.area)):
                if mm[self.area[i][0]-1,self.area[i][1]] != 0 and mm[self.area[i][0]-1,self.area[i][1]] != 2:           # и надо будет позже ещё учесть горы и иные биомы
                    newlands.append((self.area[i][0]-1,self.area[i][1]))
                if mm[self.area[i][0]+1,self.area[i][1]] != 0 and mm[self.area[i][0]+1,self.area[i][1]] != 2:
                    newlands.append((self.area[i][0]+1,self.area[i][1]))
                if mm[self.area[i][0],self.area[i][1]-1] != 0 and mm[self.area[i][0],self.area[i][1]-1] != 2:
                    newlands.append((self.area[i][0],self.area[i][1]-1))
                if mm[self.area[i][0],self.area[i][1]+1] != 0 and mm[self.area[i][0],self.area[i][1]+1] != 2:
                    newlands.append((self.area[i][0],self.area[i][1]+1))
            randchoice = random.choice(newlands)
            print('City growing, coordinates',randchoice)
            mm[randchoice[0],randchoice[1]] = 2
            self.area.append([randchoice[0],randchoice[1]])
            """ОПОСЛЯ ЭТОГО НАДО ПРОВЕРИТЬ НАЛИЧИЕ ДРУГИХ ГОРОДОВ ПО СОСЕДСТВУ С 
            НОВОЙ КЛЕТКОЙ И ЕСЛИ ТАКОЙ ГОРОД ЕСТЬ, ТО ИХ НУЖНО СОЕДИНИТь"""



    def type_change(self, mm):
        """старый концепт, не уверен, что буду его делать. типа разделение города и села."""
        if self.size > 10:
            for i in len(self.area):
                mm[self.area[i]] = 3



