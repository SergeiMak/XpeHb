import class_and_agent as caa
import numpy as np
import strata
import settlement
import pygame as pg
import goods
import pops
import factory
import state
import culture
import religion as religion
import maps as map
from camera import draw,politrisov




def main():
    Dlina = 500                                     # сколько пикселей экран
    Dlmatr = 1000                                   # сколько пикселей карта
    rasst = 100                                     # хуйня ебаная ненужная
    changed = False                                 # надо чтоб проверять, сдвинулась ли карта, чтоб лишний раз не перерисовывать


    mm = map.createMyMap(1,Dlmatr)                  # хуярим основную карту с биомами
    politicalMap = map.createMyMap(2,Dlmatr)      # политическую карту
    ironMap = map.createMyMap(3,Dlmatr)              # карту с железом
    grainMap = map.createMyMap(4,Dlmatr)            # карту с зерном

    state1 = state.State('Pidronija',(100,0,0))     # тестовое государство 1
    state2 = state.State('Lochonija',(0,0,100))     # 2

    serf, worker, soldier,schoolers = strata.Existing_Strat()     # назначаем страты населения
    pakistani, indian = culture.exist_cult()
    jewish,sunni = religion.exist_rel()

    male_age = np.zeros(75,dtype=np.uint16 )
    male_age[21] = 100
    female_age = np.asarray(male_age)

    bolvan = pops.Pops(15,male_age,female_age,serf,pakistani,sunni,100,1.00,False)     # болванчик для того, чтоб создать город (он привязывается к населению)
                                                        # но такое у меня чувство, что я эту механику уберу

    city = settlement.Settlement(state1,(50,60),mm,'Govnovodsk',bolvan,schoolers)     # тестовые города
    town = settlement.Settlement(state1,(60,70),mm,'Pidrozhopsk',bolvan,schoolers)
    city1 = settlement.Settlement(state1,(55,60),mm,'Muchosransk',bolvan,schoolers)
    town1 = settlement.Settlement(state1,(65, 70), mm, 'Jobozadsk',bolvan,schoolers)
    settlement.Settlement(state1,(50,65), mm,'Gorojobsk',bolvan,schoolers)
    settlement.Settlement(state1, (70, 70), mm, 'Zernochujsk', bolvan,schoolers)

    grain, fertilizer, fish, whool, fabric, iron = goods.existing_goods()     # назначаем производимые товары



    pops.Pops(settlement.Settlement.slovar['Zernochujsk'], male_age.copy(),female_age.copy(), serf,pakistani,sunni, 100,1)      # назначаем попы - pop - экземпляр "единицы" населения
    pops.Pops(settlement.Settlement.slovar['Govnovodsk'],male_age.copy(),female_age.copy(),serf,pakistani,sunni,100,1)
    pops.Pops(settlement.Settlement.slovar['Pidrozhopsk'],male_age.copy(),female_age.copy(),serf,pakistani,sunni,100,1)
    pops.Pops(settlement.Settlement.slovar['Muchosransk'], male_age.copy(),female_age.copy(),serf,pakistani,sunni, 100, 1)
    pops.Pops(settlement.Settlement.slovar['Jobozadsk'], male_age.copy(),female_age.copy(),serf,pakistani,sunni, 100, 1)
    pops.Pops(settlement.Settlement.slovar['Gorojobsk'],male_age.copy(),female_age.copy(),worker,pakistani,sunni,100,1)
    factory.Factory(settlement.Settlement.slovar['Zernochujsk'], serf, grain, 200, 1, 1000, 0,True)     # назначаем заводы
    factory.Factory(settlement.Settlement.slovar['Govnovodsk'],serf,grain,200,1,1000,0,True)
    factory.Factory(settlement.Settlement.slovar['Pidrozhopsk'], serf, fertilizer, 100, 1, 1000)
    factory.Factory(settlement.Settlement.slovar['Muchosransk'],serf,fish,200,1,1000,0,True)
    factory.Factory(settlement.Settlement.slovar['Jobozadsk'], serf, fertilizer, 100, 1, 1000)
    factory.Factory(settlement.Settlement.slovar['Gorojobsk'],worker,iron,100,1,1000)

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
            if ironMap[i,j] > 20:
                ironbackground.set_at((i, j), (ironMap[i,j], 0,255 - ironMap[i,j]))
                imm[i,j] = ironMap[i,j]


    bg = pg.Surface((Dlmatr, Dlmatr))
    bg.fill((0, 0, 150))
    for i in range(Dlmatr):
        for j in range(Dlmatr):
            for k in state.State.statenumberdict:
                if politicalMap[i, j] == k:
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
    monthmap = 0
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
                    draw(xe,xg,ye,yg,rasst,pribl,Dlina,mm,bg)
                    sur = bg

        if xt//100 - weekdistribution > 0:
            """распределение по работе попов"""
            print('distribution')
            weekdistribution += 1
            for i in settlement.Settlement.slovar:     # по каждому городу в общем словаре городов
                iter_for_pops = list(settlement.Settlement.slovar[i].pops)         # этот лист ввёл ибо добавляются новые попы в процессе
                for j in iter_for_pops:     # для каждого попа в этом городе
                    print(settlement.Settlement.slovar[i].name,settlement.Settlement.slovar[i].pops[j].total_num)
                    if settlement.Settlement.slovar[i].pops[j].unemployed == 1:     # нужно чтобы отделить попы заводские от безработных
                        if settlement.Settlement.slovar[i].pops[j].num != 0:            # ежели есть кто из работяг в попе
                            settlement.Settlement.summakubow(settlement.Settlement.slovar[i],settlement.Settlement.slovar[i].pops[j])     # считаем нормировку для коэффициентов распределения попов по заводам
                            for k in settlement.Settlement.slovar[i].factories:             # распределяем по этим заводам, которые все находятся в этом городе
                                if k.work_type == settlement.Settlement.slovar[i].pops[j].strata:     # проверка, подходит ли завод типу попа. ибо священники на заводах не въёбывают
                                    factory.Factory.coef(settlement.Settlement.slovar[i].factories[k])     # считаем коэффициенты
                                pops.Pops.facsearch(settlement.Settlement.slovar[i].pops[j])     # непосредственно распределяем население попа в соответствии с коэффициентами


        if (xt-25)//100 - weekbuying > 0:
            """покупка всего и вся"""
            print('buying')
            weekbuying += 1
            treck = {}
            trecksell = {}
            print(fertilizer.prices.values())
            for i in settlement.Settlement.slovar:                       # по всем городам
                for j in settlement.Settlement.slovar[i].factories:     # и заводам в этих городах
                    factory.Factory.factbuy(j)                       # завод покупает нужные ресурсы
                    factory.Factory.factboostbuy(j)                  # и бустеры (типа удобрения для С/Х)
                    if j.location.name == 'Pidrozhopsk':
                        print('DEBUG PIDRO FAC', j.money,j.sell)
                    if j.location.name == 'Jobozadsk':
                        print('DEBUG JOBO FAC', j.money,j.sell)
                for j in settlement.Settlement.slovar[i].pops:     # теперь для попов
                    pops.Pops.popbuy(j)                    # покупают жрачку и т.д.


        if (xt-30)//100 - weekpricechanging > 0:
            """корректировка цен"""
            print('price')
            weekpricechanging += 1
            for i in settlement.Settlement.slovar:
                for j in settlement.Settlement.slovar[i].factories:
                    if j.type:           # отдаю деньги и жратву крестьянам.
                        factory.Factory.givefoodmoney(j)
                    if 1 in j.price_changed.values():
                        factory.Factory.pricechangeagain(j)
                    elif 2 in j.price_changed.values():
                        factory.Factory.pricechangeagain(j)
                    else:
                        factory.Factory.pricechange(j)


        if (xt-50)//100 - weekproduction > 0:
            """производство"""
            print('production')
            weekproduction += 1
            #print(grain.prices.values())
            for i in settlement.Settlement.slovar:
                for j in settlement.Settlement.slovar[i].factories:
                    if settlement.Settlement.slovar[i].factories[j].good.name == 'Grain':
                        #print('GRAIN',settlement.Settlement.slovar[i].factories[j].sell, settlement.Settlement.slovar[i].factories[j].money)
                        print()
                    factory.Factory.create(settlement.Settlement.slovar[i].factories[j])



        if (xt-75)//100 - weekconsumption > 0:
            """потребление"""
            print('consumption')
            weekconsumption += 1
            for i in settlement.Settlement.slovar:
                for j in settlement.Settlement.slovar[i].pops:
                    if j.num != 0:
                        pops.Pops.consume_food(settlement.Settlement.slovar[i].pops[j])

        if (xt-95)//100 - weekcorrections > 0:
            """корректировка населения. смерть-рождение"""
            print('corrections')
            weekcorrections += 1
            for i in settlement.Settlement.slovar:
                iter_for_pops = list(settlement.Settlement.slovar[i].pops) # этот лист ввёл ибо удаляются пустые попы в процессе
                for j in iter_for_pops:
                    pops.Pops.popchange(settlement.Settlement.slovar[i].pops[j])
                    if settlement.Settlement.slovar[i].pops[j].total_num == 0:                            # удаляем пустые попы. чтоб память не жрали
                        settlement.Settlement.slovar[i].pops[j].location.state.money += settlement.Settlement.slovar[i].pops[j].money           # перемещаем их деньги и инвентарь в казну
                        for key in settlement.Settlement.slovar[i].pops[j].inventory:                     # а удалять у самих попов смысла нет - удаляем поп полностью
                            if key in settlement.Settlement.slovar[i].pops[j].location.state.inventory:
                                settlement.Settlement.slovar[i].pops[j].location.state.inventory[key] += settlement.Settlement.slovar[i].pops[j].inventory[key]
                            else:
                                settlement.Settlement.slovar[i].pops[j].location.state.inventory[key] = settlement.Settlement.slovar[i].pops[j].inventory[key]
                        del settlement.Settlement.slovar[i].pops[j]
                settlement.Settlement.stlpopul(settlement.Settlement.slovar[i])
                settlement.Settlement.city_growth(settlement.Settlement.slovar[i],mm,background)

        #if xt//200 - monthmap > 0:


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
                    draw(xe, xg, ye, yg, rasst, pribl, Dlina, mm, bg)
                elif mapmode == 1:
                    draw(xe, xg, ye, yg, rasst, pribl, Dlina, mm, bg)
                    politrisov(xe,xg,ye,yg,rasst,pribl,Dlina,politicalMap,pbg)
                elif mapmode == 2:
                    draw(xe, xg, ye, yg, rasst, pribl, Dlina, imm, bg)
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
        for q in settlement.Settlement.slovar:
            if pg.Rect.collidepoint(settlement.Settlement.arry[q1][0],(pos[0]-xe,pos[1]-ye)):

                citytext = f1.render(settlement.Settlement.slovar[q].name, 0, (0, 0, 0))
                citytext1 = f1.render(str(settlement.Settlement.slovar[q].population),0,(0,0,0))

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


        pg.time.delay(1)
        if not pause:
            xt += 1                                          # счётчик времени


if __name__ == "__main__":
    main()
