import numpy as np
import pygame as pg
"""
ПРОИЗВОДИМЫЕ В ИГРЕ ТОВАРЫ
планы:
сделать регулирование производительности, плодовитости зерна, рождаемости, и прочего-прочего-прочего - реиграбельность
надо бы сделать что-то типа конструктора всяких херовин. это было б прям вообще круто. тип плавучие в море ядерные станции и так далее
"""

class Goods:
    gddict = {}         # словарь всех товаров в игре
    def __init__(self, name):
        self.name = name
        self.prices = {}                         # словарь всех цен, выставляемых заводами на этот товар
        Goods.gddict[self.name] = self


    def howmany(self):
        print(1)




def existing_goods():
    """перепихиваем все эти товары в основной исполняемый файл игры"""
    grain = Goods('Grain')
    fish = Goods('Fish')
    fertilizer = Goods('Fertilizer')
    whool = Goods('Whool')
    fabric = Goods('Fabric')
    iron = Goods('Iron')
    return grain, fertilizer, fish, whool, fabric, iron