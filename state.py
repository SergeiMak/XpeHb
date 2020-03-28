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
        self.settlements = {}                # какие в нём есть города
        self.laws = {'Female_emans':False,'Children_labour':True}            # законы. пока что эмансипация женщин и детский труд
        State.statenumberdict[self.number] = self
        self.serf_land_right_per_capita = 0.1         # сколько десятков соток (квадратных километров) земли позволено иметь крестьянину
                                                    # если 0 - то сколько угодно. ограничение по владению землёй в случае крепостничество
                                                    # получается, если есть хозяин завода и у него стоит чё-то типа флага "помещик"

        State.statedict[self.name] = self
        self.money = 0
        self.inventory = {}

