import class_and_agent as caa
import numpy as np
import strata as stra
import settlement as stl
import pygame as pg
import goods as gds
import pops as po
import factory as fct
import state


def risov(xe,xg,ye,yg,rasst,pribl,Dlina,mm,bg):
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
            elif mm[i,j] >20:
                if bg.get_at(((i - (-xe + xg - (Dlina // (2 * pribl)))) * pribl,
                              (j - (-ye + yg - (Dlina // (2 * pribl)))) * pribl)) != (mm[i,j], 0, 255 - mm[i,j]):
                    pg.draw.rect(bg, (mm[i,j], 0, 255 - mm[i,j]), ((i - (-xe + xg - (Dlina // (2 * pribl)))) * pribl,
                                               (j - (-ye + yg - (Dlina // (2 * pribl)))) * pribl,
                                               pribl, pribl))


def politrisov(xe,xg,ye,yg,rasst,pribl,Dlina,pm,pbg):
    """то же, что и risov, только для политической карты"""
    for i in range(-xe + xg - (Dlina // (2 * pribl)),
                   -xe + xg + (Dlina // (2 * pribl))):
        for j in range(-ye + yg - (Dlina // (2 * pribl)),
                       -ye + yg + (Dlina // (2 * pribl))):

            for k in state.State.statenumberdict:
                if pm[i, j] == k:
                    if pbg.get_at(((i - (-xe + xg - (Dlina // (2 * pribl)))) * pribl,
                                  (j - (-ye + yg - (Dlina // (2 * pribl)))) * pribl)) != state.State.statenumberdict[k].colour:

                        pg.draw.rect(pbg,state.State.statenumberdict[k].colour,
                                     ((i - (-xe + xg - (Dlina // (2 * pribl)))) * pribl,
                                                   (j - (-ye + yg - (Dlina // (2 * pribl)))) * pribl,
                                                   pribl, pribl))
                elif pm[i, j] == 0:
                        pg.draw.rect(pbg,(0,0,0),
                                     ((i - (-xe + xg - (Dlina // (2 * pribl)))) * pribl,
                                                   (j - (-ye + yg - (Dlina // (2 * pribl)))) * pribl,
                                                   pribl, pribl),1)


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
    pm = np.zeros((Dlmatr,Dlmatr) ,dtype=np.uint8)
    pm[30:100, 40:100] = 1
    pm[430:500, 440:500] = 2
    return pm

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
    gm = np.zeros((Dlmatr,Dlmatr),dtype=np.uint8)
    for i in range(len(gm)):
        for j in range(len(gm)):
            gm[i,j] = np.random.randint(0,255)
    return gm

def main():
    Dlina = 500                                     # сколько пикселей экран
    Dlmatr = 1000                                   # сколько пикселей карта
    rasst = 100                                     # хуйня ебаная ненужная
    changed = False                                 # надо чтоб проверять, сдвинулась ли карта, чтоб лишний раз не перерисовывать
    mm = mapmatrix(Dlmatr)                          # хуярим основную карту с биомами
    pm = politmm(Dlmatr)     # политическую карту
    im = ironmm(Dlmatr)     # карту с железом
    gm = grainmm(Dlmatr)     # карту с зерном

    state1 = state.State('Pidronija',(100,0,0))     # тестовое государство 1
    state2 = state.State('Lochonija',(0,0,100))     # 2

    serf, worker, soldier,schoolers = stra.Existing_Strat()     # назначаем страты населения

    bolvan = po.Pops(15,100,serf,1,100,1.00,False)     # болванчик для того, чтоб создать город (он привязывается к населению)
                                                        # но такое у меня чувство, что я эту механику уберу

    city = stl.Settlement(state1,(50,60),mm,'Govnovodsk',bolvan,schoolers)     # тестовые города
    town = stl.Settlement(state1,(60,70),mm,'Pidrozhopsk',bolvan,schoolers)
    city1 = stl.Settlement(state1,(55,60),mm,'Muchosransk',bolvan,schoolers)
    town1 = stl.Settlement(state1,(65, 70), mm, 'Jobozadsk',bolvan,schoolers)
    stl.Settlement(state1,(50,65), mm,'Gorojobsk',bolvan,schoolers)
    stl.Settlement(state1, (70, 70), mm, 'Zernochujsk', bolvan,schoolers)

    grain, fertilizer, fish, whool, fabric, iron = gds.existing_goods()     # назначаем производимые товары

    po.Pops(stl.Settlement.slovar['Zernochujsk'], 100, serf, 1, 100, 1)      # назначаем попы - pop - экземпляр "единицы" населения
    po.Pops(stl.Settlement.slovar['Govnovodsk'],100,serf,1,100,1)           #serf1 = worker1 = serf2 = worker2 =
    po.Pops(stl.Settlement.slovar['Pidrozhopsk'],100,serf,1,100,1)
    po.Pops(stl.Settlement.slovar['Muchosransk'], 100,serf, 1, 100, 1)
    po.Pops(stl.Settlement.slovar['Jobozadsk'], 100,serf,1, 100, 1)
    po.Pops(stl.Settlement.slovar['Gorojobsk'],100,worker,1,100,1)
    fct.Factory(stl.Settlement.slovar['Zernochujsk'], serf, grain, 200, 1, 1000, 0, 1)     # назначаем заводы
    fct.Factory(stl.Settlement.slovar['Govnovodsk'],serf,grain,200,1,1000,0,1)                      #fac1 = fertilfac1 = fac2 = fertilfac2 =
    fct.Factory(stl.Settlement.slovar['Pidrozhopsk'], serf, fertilizer, 100, 1, 1000)
    fct.Factory(stl.Settlement.slovar['Muchosransk'],serf,fish,200,1,1000,0,1)
    fct.Factory(stl.Settlement.slovar['Jobozadsk'], serf, fertilizer, 100, 1, 1000)
    fct.Factory(stl.Settlement.slovar['Gorojobsk'],worker,iron,100,1,1000)

    pg.init()

    sc = pg.display.set_mode((Dlina, Dlina))

    background = pg.Surface((Dlmatr, Dlmatr))
    background.fill((0, 0, 150))
    politbg = pg.Surface((Dlmatr, Dlmatr),flags=pg.SRCALPHA)
    pbg = pg.Surface((Dlmatr, Dlmatr), flags=pg.SRCALPHA)
    pbg.set_alpha(100)


    for i in range(Dlmatr):
        for j in range(Dlmatr):
            if mm[i, j] == 1:
                background.set_at((i, j), (0, 90, 0))
            elif mm[i, j] == 2:
                background.set_at((i, j), (150, 150, 150))
            elif mm[i, j] == 3:
                background.set_at((i, j), (50, 50, 50))
            elif mm[i, j] == 4:
                background.set_at((i, j), (0, 0, 0))


    ironbackground = pg.Surface.copy(background)
    imm = np.array(mm, copy=True)

    for i in range(Dlmatr):
        for j in range(Dlmatr):
            if im[i,j] > 20:
                ironbackground.set_at((i, j), (im[i,j], 0,255 - im[i,j]))
                imm[i,j] = im[i,j]


    bg = pg.Surface((Dlmatr, Dlmatr))
    bg.fill((0, 0, 150))
    for i in range(Dlmatr):
        for j in range(Dlmatr):
            for k in state.State.statenumberdict:
                if pm[i, j] == k:
                    politbg.set_at((i, j), state.State.statenumberdict[k].colour)

    politbg.set_alpha(100)

    xb = 0
    yb = 0

    sc.blit(background, (xb, yb))

    pg.display.update()


    xe, ye = xb, yb
    xg, yg = 0, 0
    sur = background
    pribl = 1
    f1 = pg.font.Font(None, 26)
    xt = 0
    but1 = pg.Rect(50,0,50,30)
    but2 = pg.Rect(150, 0, 50, 30)
    weekdistribution = 0                 # все эти хуйни недельные - это для распределения нагрузки в течение дня/недели
    weekproduction = 0                   # и так далее. тип утром распределились на работу, днём произвели товар, вечером потрах... скорректировали население
    weekconsumption = 0
    weekbuying = 0
    weekpricechanging = 0
    weekcorrections = 0
    mapmode = 0
    pause = False

    while 1:
        """всё хуярится через вайл"""
        #print('СДЕЛАТЬ МИГРАЦИЮ И ПОИСК НОВОЙ РАБОТЫ, А ПОТОМ ЦЕНООБРАЗОВАНИЕ И БЛЯ ЕЩЁ ЧТО-ТО')

        #print('НЕ ПОКУПКА УСИЛИТЕЛЯ, ЕСЛИ КОНЕЧНАЯ ЦЕНА ПРОДУКТА СЛИШКОМ НИЗКАЯ')
        for i in pg.event.get():
            """обрабатывается нажатие клавиш клавиатуры с pygame"""
            if i.type == pg.QUIT:
                exit()
            elif i.type == pg.KEYUP:
                if i.key == pg.K_BACKSPACE:
                    pribl = pribl//10
                    if pribl == 1:
                        sur = background

            elif i.type == pg.MOUSEBUTTONUP:
                if i.button == 1:
                    if pg.Rect.collidepoint(but1, pos):
                        if mapmode != 1:
                            mapmode = 1
                        else:
                            mapmode = 0
                    if pg.Rect.collidepoint(but2,pos):
                        if mapmode != 2:
                            mapmode = 2
                        else:
                            mapmode = 0


                if i.button == 3:
                    xg,yg = i.pos[0], i.pos[1]
                    print(pos,xe,ye)
                    pribl = pribl*10
                    bg = pg.Surface((Dlina, Dlina))
                    risov(xe,xg,ye,yg,rasst,pribl,Dlina,mm,bg)
                    sur = bg

        if xt//100 - weekdistribution > 0:
            """распределение по работе попов"""
            print('distribution')
            weekdistribution += 1
            for i in stl.Settlement.slovar:     # по каждому городу в общем словаре городов
                for j in stl.Settlement.slovar[i].pops:     # для каждого попа в этом городе
                    if stl.Settlement.slovar[i].pops[j].unemployed == 1:     # была тема, стала костылём, но хз пока, стоит ли убирать
                        if stl.Settlement.slovar[i].pops[j].num != 0:            # ежели есть кто из работяг в попе
                            stl.Settlement.summakubow(stl.Settlement.slovar[i],j)     # считаем нормировку для коэффициентов распределения попов по заводам
                            for k in stl.Settlement.slovar[i].factories:             # распределяем по этим заводам, которые все находятся в этом городе
                                if k.work_type == j.strata:     # проверка, подходит ли завод типу попа. ибо священники на заводах не въёбывают
                                    fct.Factory.coef(stl.Settlement.slovar[i].factories[k])     # считаем коэффициенты
                                po.Pops.facsearch(j)     # непосредственно распределяем население попа в соответствии с коэффициентами


        if (xt-25)//100 - weekbuying > 0:
            """покупка всего и вся"""
            print('production')
            weekbuying += 1
            treck = {}
            trecksell = {}
            for i in stl.Settlement.slovar:                       # по всем городам
                for j in stl.Settlement.slovar[i].factories:     # и заводам в этих городах
                    fct.Factory.factbuy(j)                       # завод покупает нужные ресурсы
                    fct.Factory.factboostbuy(j)                  # и бустеры (типа удобрения для С/Х)
                    if stl.Settlement.slovar[i].factories[j].type == 1:     # эта херня на попозже. чтоб учесть, что крестьяне работают на себя а не барина
                        #fct.Factory.serf_winter(stl.Settlement.slovar[i].factories[j])
                        print()
                for j in stl.Settlement.slovar[i].pops:     # теперь для попов
                    po.Pops.popbuy(j)                    # покупают жрачку и т.д.


        if (xt-30)//100 - weekpricechanging > 0:
            """корректировка цен"""
            print('price')
            weekpricechanging += 1
            for i in stl.Settlement.slovar:
                for j in stl.Settlement.slovar[i].factories:
                    if 1 in j.price_changed.values():
                        fct.Factory.pricechangeagain(j)
                    elif 2 in j.price_changed.values():
                        fct.Factory.pricechangeagain(j)
                    else:
                        fct.Factory.pricechange(j)


        if (xt-50)//100 - weekproduction > 0:
            """производство"""
            print('production')
            weekproduction += 1
            print(grain.prices.values())
            for i in stl.Settlement.slovar:
                for j in stl.Settlement.slovar[i].factories:
                    if stl.Settlement.slovar[i].factories[j].good.name == 'Grain':
                        print('GRAIN',stl.Settlement.slovar[i].factories[j].sell, stl.Settlement.slovar[i].factories[j].money)
                    fct.Factory.create(stl.Settlement.slovar[i].factories[j])



        if (xt-75)//100 - weekconsumption > 0:
            """потребление"""
            print('consumption')
            weekconsumption += 1
            for i in stl.Settlement.slovar:
                for j in stl.Settlement.slovar[i].pops:
                    if j.num != 0:
                        po.Pops.consume_food(stl.Settlement.slovar[i].pops[j])

        if (xt-95)//100 - weekcorrections > 0:
            """корректировка населения. смерть-рождение"""
            print('corrections')
            weekcorrections += 1
            for i in stl.Settlement.slovar:
                for j in stl.Settlement.slovar[i].pops:
                    po.Pops.popchange(j)
                stl.Settlement.stlpopul(stl.Settlement.slovar[i])

        keys = pg.key.get_pressed()          # при нажатии на кнопку меняется координата исходного полотна - сдвиг карты
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
                if mapmode == 0:
                    risov(xe, xg, ye, yg, rasst, pribl, Dlina, mm, bg)
                elif mapmode == 1:
                    risov(xe, xg, ye, yg, rasst, pribl, Dlina, mm, bg)
                    politrisov(xe,xg,ye,yg,rasst,pribl,Dlina,pm,pbg)
                elif mapmode == 2:
                    risov(xe, xg, ye, yg, rasst, pribl, Dlina, imm, bg)
                changed = False

        pressed = pg.mouse.get_pressed()
        pos = pg.mouse.get_pos()
        if pressed[0]:
            xa,ya = pos
            xe = xe + (xa - xg)
            ye = ye + (ya - yg)




        if pribl > 1:
            sc.blit(sur, (0,0))
            if mapmode == 1:
                sc.blit(pbg,(0,0))
            #elif mapmode == 2:

        else:
            sc.blit(sur, (xe,ye))
            if mapmode == 1:
                sc.blit(politbg, (xe,ye))
            elif mapmode == 2:
                sc.blit(ironbackground, (xe,ye))

        text1 = f1.render(str(xt//10), 0, (0, 0, 0))                                 # кнопочки и другой текст
        sc.blit(text1,(0,0))
        text2 = f1.render('Political',0,(0,0,0))
        sc.blit(text2,(50,0))
        text3 = f1.render('Resource',0,(0,0,0))
        sc.blit(text3,(150,0))
        q1 = 0
        for q in stl.Settlement.slovar:
            if pg.Rect.collidepoint(stl.Settlement.arry[q1][0],(pos[0]-xe,pos[1]-ye)):

                citytext = f1.render(stl.Settlement.slovar[q].name, 0, (0, 0, 0))
                citytext1 = f1.render(str(stl.Settlement.slovar[q].population),0,(0,0,0))

                if (pos[1]-50) < 0:
                    minus = -1
                else:
                    minus = 1
                sc.blit(citytext, (pos[0],pos[1]-50*minus))
                sc.blit(citytext1,(pos[0],pos[1]-30*minus))
            q1 += 1

        pg.display.update()
        if pressed[0]:
            xg, yg = pos


        pg.time.delay(5)
        if not pause:
            xt += 1                                          # счётчик времени


if __name__ == "__main__":
    main()
