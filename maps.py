import numpy as np
import pygame as pg
from random import randint

# Необходимо описать что за параметры функций, чтобы было понятно, что происходит 
# Нужны нормально комментарии к коду

def mapmatrix(Dlmatr):
    """определяем карту"""
    mm = np.zeros((Dlmatr,Dlmatr),dtype=np.uint8)
    mm[30:100, 40:100] = 1
    mm[30:50, 60:65] = 0
    mm[45:50, 65:100] = 0
    mm[30:50, 60:65] = 0
    mm[430:500, 440:500] = 1
    mm[430:450, 460:465] = 0
    mm[445:450, 465:500] = 0
    mm[430:450, 460:465] = 0
    mm[450:455, 470:480] = 2
    mm[470:480, 440:450] = 3
    mm[475, 450:475] = 4
    mm[455:475, 475] = 4
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

def grainmm(Dlmatr):
    """
    карта с залежами питательных веществ для выращивания зерна

    Планы: сделать нормальное распределение и занулить в морях-горах и т.д. и в принципе разное распределение на разной местности
    :param Dlmatr:
    :return:
    """
    grainMap = np.zeros((Dlmatr,Dlmatr),dtype=np.uint8)
    for i in range(len(grainMap)):
        for j in range(len(grainMap)):
            grainMap[i,j] = np.random.randint(0,255)
    return grainMap

def createMyMap(nameOfMap,Dlmatr):
    if nameOfMap == 1: return mapmatrix(Dlmatr)
    if nameOfMap == 2: return politmm(Dlmatr)
    if nameOfMap == 3: return ironmm(Dlmatr)
    if nameOfMap == 4: return grainmm(Dlmatr)
    return 0