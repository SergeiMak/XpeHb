import numpy as np
import pygame as pg
"""
Планы: сделать регулирование количества земли на крестьянина
"""

class State:
    number = 0               # количество государств
    statedict = {}               # словарь с государствами по названиям
    statenumberdict = {}             # по номерам
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour             # цвет на карте
        State.number += 1
        self.number = State.number
        self.strats = {}
        self.settlements = []                # какие в нём есть города
        self.factories = ([],[],[],[],[],[],[])
        self.pops_for_opt = ([], [], [], [], [], [], [])
        self.settlements_for_opt = ([], [], [], [], [], [], [])
        self.pops_for_breeding = []
        # self.factories_tuesday = []
        # self.factories_wednesday = []
        # self.factories_thursday = []
        # self.factories_friday = []
        # self.factories_saturday = []
        # self.factories_sunday = []
        self.last_added_factory_day = 1
        self.last_added_pops_day = 1
        self.last_added_settl_day = 1
        self.laws = {'Female_emans':False,'Children_labour':True}            # законы. пока что эмансипация женщин и детский труд
        State.statenumberdict[self.number] = self
        self.subsidise_new_settlements = 0
        self.serf_land_right_per_capita = 0.1         # сколько десятков соток (квадратных километров) земли позволено иметь крестьянину
                                                    # если 0 - то сколько угодно. ограничение по владению землёй в случае крепостничества
                                                    # получается, если есть хозяин завода и у него стоит чё-то типа флага "помещик"

        State.statedict[self] = self.name
        self.money = 0
        self.inventory = {}

