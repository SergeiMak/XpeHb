import numpy as np
import rivers
import pygame as pg
from random import randint
import generators

# Необходимо описать что за параметры функций, чтобы было понятно, что происходит 
# Нужны нормально комментарии к коду

def mapmatrix(Dlmatr):
    """определяем карту
    1 - земля
    0 - вода
    2 - город
    3 - лес
    4 - тоже хуйня
    5 - пашня
    """
    mm = np.zeros((Dlmatr,Dlmatr),dtype=np.uint8)
    # mm[30:100, 40:100] = 1
    # mm[30:50, 60:65] = 1
    # mm[45:50, 65:100] = 1
    # mm[30:50, 60:65] = 1
    # mm[430:500, 440:500] = 1
    # mm[430:450, 460:465] = 0
    # mm[445:450, 465:500] = 0
    # mm[430:450, 460:465] = 0
    # mm[450:455, 470:480] = 2
    # mm[60:90, 40:60] = 1
    # mm[475, 450:475] = 4
    # mm[455:475, 475] = 4
    #rivers.River(mm,"i",(30,50),2,20)                                # тут хуёво генерил реки. очень хуёво. теперь новый генератор
    #rivers.River(mm, "i", (50, 50), 1, 40)
    #rivers.River(mm, "i", (50, 60), 2, 40)
    #print(mm[30:50,49:51])

    return mm

def politmm(Dlmatr):
    """политическая карта"""
    politicalMap = np.zeros((Dlmatr,Dlmatr) ,dtype=np.uint8)
    politicalMap[30:100, 40:100] = 1
    politicalMap[430:500, 440:500] = 2
    return politicalMap

def ironmm(Dlmatr):
    """карта с залежами железа"""
    rm = np.zeros((Dlmatr,Dlmatr),dtype=np.uint8)
    rm[52,62] = 15
    rm[54, 61] = 120
    rm[56, 63] = 210
    rm[52, 66] = 73
    rm[50, 62] = 117
    return rm

def grainmm(Dlmatr,mm):
    """
    карта с залежами питательных веществ для выращивания зерна

    Планы: сделать нормальное распределение и занулить в морях-горах и т.д. и в принципе разное распределение на разной местности
    :param Dlmatr:
    :return:
    """
    land_list = []
    grainMap = np.zeros((Dlmatr,Dlmatr),dtype=np.uint16)
    # for i in range(len(grainMap)):
    #     for j in range(len(grainMap)):
    #         grainMap[i,j] = np.random.randint(0,255)
    generators.generateland(land_list, grainMap,mm,(100,100),10000,False,True,False,True)
    
    return grainMap

def forestmm(Dlmatr,mm,background):
    """
    карта с залежами питательных веществ для выращивания зерна

    Планы: сделать нормальное распределение и занулить в морях-горах и т.д. и в принципе разное распределение на разной местности
    :param Dlmatr:
    :return:
    """
    forestMap = np.zeros((Dlmatr,Dlmatr),dtype=np.uint16)
    generators.generateforest(forestMap,mm,background,(100,100),9000)
    point = (100,100)
    generators.generateriver(mm,background,point,1000,False,True,False,True)

    
    """скорее всего ещё придётся переделывать отрисовку. там же необходимо будет учесть рисование лесов"""
    
    return forestMap

def createMyMap(nameOfMap,Dlmatr,mm):
    if nameOfMap == 1: return mapmatrix(Dlmatr)
    if nameOfMap == 2: return politmm(Dlmatr)
    if nameOfMap == 3: return ironmm(Dlmatr)
    if nameOfMap == 4: return grainmm(Dlmatr,mm)
    return 0