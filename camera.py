import numpy as np
import pygame as pg
import state
from random import randint

# Необходимо описать что за параметры функций, чтобы было понятно, что происходит 
# Нужны нормально комментарии к коду

def draw(xe,xg,ye,yg,rasst,pribl,Dlina,mm,bg):
    """
    Функция нужна для перерисовки того, что выводится непосредственно на экран при приближении. ибо столько
    пикселей сразу рисовать - это охуеть можно. короч оптимизация, все дела.
    :param xe:      координата, ответственная за положение карты на экране (по сути координата левого верхнего угла
                            основного полотна - полотна без приближения
    :param xg:      координата места, куда щёлкнули правой кнопкой мыши для приближения
    :param ye:
    :param yg:
    :param rasst:   хотел ввести параметр, чтоб рисовало часть полотна за экраном (типа для плавности и скорости)
                            но потом понял, что это всё хуйня
    :param pribl:   по идее для ещё большего приближения, но там чё-то как-то багает, а единичное приближение меня как-то
                            пока вплоне устраивает
    :param Dlina:   длина массива с картой (т.е. количество пикселей на основном полотне. в каждом пикселе свой "биом"
                            и по идее пиксель должен соответствовать ~1км
    :param mm:      матрица с картой
    :param bg:      полотно, на котором рисуем приближение
    :return:
    """
    somerange = (Dlina // (2 * pribl))
    for i in range(-xe + xg - somerange,
                   -xe + xg + somerange):
        for j in range(-ye + yg - somerange,
                       -ye + yg + somerange):
            swithcer ={0: (0,0,150), 
                       1: (0,100,0), 
                       2: (150,150,150),
                       3: (50,50,50),
                       4: (0,0,0),
                       5: (120, 150, 0),
                       }
            sw = swithcer[mm[i,j]]
            if bg.get_at(((i - (-xe + xg - somerange)) * pribl,
                              (j - (-ye + yg - somerange)) * pribl)) != sw:
                    pg.draw.rect(bg, sw, ((i - (-xe + xg - somerange)) * pribl,
                                               (j - (-ye + yg - somerange)) * pribl,
                                               pribl, pribl))



def politrisov(xe,xg,ye,yg,rasst,pribl,Dlina,politicalMap,pbg):
    """то же, что и risov, только для политической карты"""
    for i in range(-xe + xg - (Dlina // (2 * pribl)),
                   -xe + xg + (Dlina // (2 * pribl))):
        for j in range(-ye + yg - (Dlina // (2 * pribl)),
                       -ye + yg + (Dlina // (2 * pribl))):

            for k in state.State.statenumberdict:
                if politicalMap[i, j] == k:
                    if pbg.get_at(((i - (-xe + xg - (Dlina // (2 * pribl)))) * pribl,
                                  (j - (-ye + yg - (Dlina // (2 * pribl)))) * pribl)) != state.State.statenumberdict[k].colour:

                        pg.draw.rect(pbg,state.State.statenumberdict[k].colour,
                                     ((i - (-xe + xg - (Dlina // (2 * pribl)))) * pribl,
                                                   (j - (-ye + yg - (Dlina // (2 * pribl)))) * pribl,
                                                   pribl, pribl))
                elif politicalMap[i, j] == 0:
                        pg.draw.rect(pbg,(0,0,0),
                                     ((i - (-xe + xg - (Dlina // (2 * pribl)))) * pribl,
                                                   (j - (-ye + yg - (Dlina // (2 * pribl)))) * pribl,
                                                   pribl, pribl),1)

def backspace(pribl,background,i):
    if i.key == pg.K_BACKSPACE:
        pribl = pribl // 10
        if pribl == 1:
            sur = background


# Хуево, не должен там стаять сразу if , потому что нету return в случае, когда if не срабатывает
def pribliz(i,xe,ye,Dlina,mm,pribl):
    if i.button == 3:
        xg, yg = i.pos[0], i.pos[1]
        pribl = pribl * 10
        bg = pg.Surface((Dlina, Dlina))
        risov(xe, xg, ye, yg, pribl, Dlina, mm, bg)
        sur = bg
        return pribl, sur

# Зачем передается changed?
def bewegung(keys,xe,ye,pribl,xg,yg,Dlina,mm,bg,changed):
    if keys[pg.K_LEFT]:
        xe += 10
        changed = True
    if keys[pg.K_RIGHT]:
        xe -= 10
        changed = True
    if keys[pg.K_UP]:
        ye += 10
        changed = True
    if keys[pg.K_DOWN]:
        ye -= 10
        changed = True
    if changed:
        if pribl > 1:
            risov(xe, xg, ye, yg, pribl, Dlina, mm, bg)
            changed = False

