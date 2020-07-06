import numpy as np
import pygame as pg
from random import randint


def risov(xe,xg,ye,yg,pribl,Dlina,mm,bg):

    for i in range(-xe + xg - (Dlina // (2 * pribl)),
                   -xe + xg + (Dlina // (2 * pribl))):
        for j in range(-ye + yg - (Dlina // (2 * pribl)),
                       -ye + yg + (Dlina // (2 * pribl))):

            if mm[i, j] == 1:
                if bg.get_at(((i - (-xe + xg - (Dlina // (2 * pribl)))) * pribl,
                                               (j - (-ye + yg - (Dlina // (2 * pribl)))) * pribl)) != (0,100,0):
                    pg.draw.rect(bg, (0, 100, 0), ((i - (-xe + xg - (Dlina // (2 * pribl)))) * pribl,
                                               (j - (-ye + yg - (Dlina // (2 * pribl)))) * pribl,
                                               pribl, pribl))

            elif mm[i, j] == 2:
                if bg.get_at(((i - (-xe + xg - (Dlina // (2 * pribl)))) * pribl,
                              (j - (-ye + yg - (Dlina // (2 * pribl)))) * pribl)) != (150, 150, 150):
                    pg.draw.rect(bg, (150, 150, 150), ((i - (-xe + xg - (Dlina // (2 * pribl)))) * pribl,
                                                   (j - (-ye + yg - (Dlina // (2 * pribl)))) * pribl,
                                                   pribl, pribl))
            elif mm[i, j] == 3:
                if bg.get_at(((i - (-xe + xg - (Dlina // (2 * pribl)))) * pribl,
                              (j - (-ye + yg - (Dlina // (2 * pribl)))) * pribl)) != (50, 50, 50):
                    pg.draw.rect(bg, (50, 50, 50), ((i - (-xe + xg - (Dlina // (2 * pribl)))) * pribl,
                                                (j - (-ye + yg - (Dlina // (2 * pribl)))) * pribl,
                                                pribl, pribl))
            elif mm[i, j] == 4:
                if bg.get_at(((i - (-xe + xg - (Dlina // (2 * pribl)))) * pribl,
                              (j - (-ye + yg - (Dlina // (2 * pribl)))) * pribl)) != (0, 0, 0):
                    pg.draw.rect(bg, (0, 0, 0), ((i - (-xe + xg - (Dlina // (2 * pribl)))) * pribl,
                                             (j - (-ye + yg - (Dlina // (2 * pribl)))) * pribl,
                                             pribl, pribl))
            elif mm[i, j] == 0:
                if bg.get_at(((i - (-xe + xg - (Dlina // (2 * pribl)))) * pribl,
                              (j - (-ye + yg - (Dlina // (2 * pribl)))) * pribl)) != (0, 0, 150):
                    pg.draw.rect(bg, (0, 0, 150), ((i - (-xe + xg - (Dlina // (2 * pribl)))) * pribl,
                                               (j - (-ye + yg - (Dlina // (2 * pribl)))) * pribl,
                                               pribl, pribl))



def backspace(pribl,background,i):
    if i.key == pg.K_BACKSPACE:
        pribl = pribl // 10
        if pribl == 1:
            sur = background



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