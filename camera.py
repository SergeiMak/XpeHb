import numpy as np
import pygame as pg
from random import randint

# Необходимо описать что за параметры функций, чтобы было понятно, что происходит 
# Нужны нормально комментарии к коду

def risov(xe,xg,ye,yg,pribl,Dlina,mm,bg):

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
                       }
            sw = swithcher[mu[i,j]]()
            if bg.get_at(((i - (-xe + xg - somerange)) * pribl,
                              (j - (-ye + yg - somerange)) * pribl)) != sw:
                    pg.draw.rect(bg, sw, ((i - (-xe + xg - somerange)) * pribl,
                                               (j - (-ye + yg - somerange)) * pribl,
                                               pribl, pribl))



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