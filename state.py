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

        State.statedict[self.name] = self

