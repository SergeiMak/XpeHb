import class_and_agent
import numpy as np
import strata
from settlement import Settlement
import pygame as pg
import goods
from pops import Pops
from factory import Factory
import state
import culture
import religion
import rivers
import maps as map
from camera import draw,politrisov

"""
def risov(xe,xg,ye,yg,rasst,pribl,DlinaX,DlinaY,biomMap,bg):
    
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
    :param biomMap:      матрица с картой
    :param bg:      полотно, на котором рисуем приближение
    :return:
    
    for i in range(-xe + xg - (DlinaX // (2 * pribl)),
                   -xe + xg + (DlinaX // (2 * pribl))):
        for j in range(-ye + yg - (DlinaY // (2 * pribl)),
                       -ye + yg + (DlinaY // (2 * pribl))):

            if biomMap[i, j] == 1:
                if bg.get_at(((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
                                               (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl)) != (0,100,0):
                    pg.draw.rect(bg, (0, 100, 0), ((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
                                               (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl,
                                               pribl, pribl))

            elif biomMap[i, j] == 2:
                if bg.get_at(((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
                              (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl)) != (50, 50, 50):
                    pg.draw.rect(bg, (50, 50, 50), ((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
                                                   (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl,
                                                   pribl, pribl))
            elif biomMap[i, j] == 3:
                if bg.get_at(((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
                              (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl)) != (50, 50, 50):
                    pg.draw.rect(bg, (50, 50, 50), ((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
                                                (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl,
                                                pribl, pribl))
            elif biomMap[i, j] == 4:
                if bg.get_at(((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
                              (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl)) != (0, 0, 0):
                    pg.draw.rect(bg, (0, 0, 0), ((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
                                             (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl,
                                             pribl, pribl))
            elif biomMap[i, j] == 5:
                if bg.get_at(((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
                              (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl)) != (120, 150, 0):
                    pg.draw.rect(bg, (120, 150, 0), ((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
                                               (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl,
                                               pribl, pribl))
            elif biomMap[i, j] == 0:
                if bg.get_at(((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
                              (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl)) != (0, 0, 150):
                    pg.draw.rect(bg, (0, 0, 150), ((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
                                               (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl,
                                               pribl, pribl))
            elif biomMap[i,j] >20:
                if bg.get_at(((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
                              (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl)) != (biomMap[i,j], 0, 255 - biomMap[i,j]):
                    pg.draw.rect(bg, (biomMap[i,j], 0, 255 - biomMap[i,j]), ((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
                                               (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl,
                                               pribl, pribl))


def politrisov(xe,xg,ye,yg,rasst,pribl,DlinaX,DlinaY,pm,pbg):
    то же, что и risov, только для политической карты
    for i in range(-xe + xg - (DlinaX // (2 * pribl)),
                   -xe + xg + (DlinaX // (2 * pribl))):
        for j in range(-ye + yg - (DlinaY // (2 * pribl)),
                       -ye + yg + (DlinaY // (2 * pribl))):

            for k in state.State.statenumberdict:
                if pm[i, j] == k:
                    if pbg.get_at(((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
                                  (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl)) != state.State.statenumberdict[k].colour:

                        pg.draw.rect(pbg,state.State.statenumberdict[k].colour,
                                     ((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
                                                   (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl,
                                                   pribl, pribl))
                elif pm[i, j] == 0:
                        pg.draw.rect(pbg,(0,0,0),
                                     ((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
                                                   (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl,
                                                   pribl, pribl),1)


def mapmatrix(Dlmatr):
    определяем карту
    biomMap = np.zeros((Dlmatr,Dlmatr),dtype=np.uint8)
    biomMap[30:100, 40:100] = 1
    biomMap[30:50, 60:65] = 0
    biomMap[45:50, 65:100] = 0
    biomMap[30:50, 60:65] = 0
    biomMap[430:500, 440:500] = 1
    biomMap[430:450, 460:465] = 0
    biomMap[445:450, 465:500] = 0
    biomMap[430:450, 460:465] = 0
    biomMap[450:455, 470:480] = 2
    biomMap[470:480, 440:450] = 3
    biomMap[475, 450:475] = 4
    biomMap[455:475, 475] = 4
    return biomMap

def politbiomMap(Dlmatr):
    политическая карта
    pm = np.zeros((Dlmatr,Dlmatr) ,dtype=np.uint8)
    pm[30:100, 40:100] = 1
    pm[430:500, 440:500] = 2
    return pm

def ironbiomMap(Dlmatr):
    карта с залежами железа
    rm = np.zeros((Dlmatr,Dlmatr),dtype=np.uint8)
    rm[52,62] = 15
    rm[54, 61] = 120
    rm[56, 63] = 210
    rm[52, 66] = 73
    rm[50, 62] = 117
    return rm

def grainbiomMap(Dlmatr):
    
    карта с залежами питательных веществ для выращивания зерна

    Планы: сделать нормальное распределение и занулить в морях-горах и т.д. и в принципе разное распределение на разной местности
    :param Dlmatr:
    :return:
    
    gm = np.zeros((Dlmatr,Dlmatr),dtype=np.uint8)
    for i in range(len(gm)):
        for j in range(len(gm)):
            gm[i,j] = np.random.randint(0,255)
    return gm
"""
def main():
    # сколько пикселей экран
    #DlinaX = 1300                                     
    #DlinaY = 600
    Dlina = 600
    # сколько пикселей карта
    Dlmatr = 1000
    # хуйня ебаная ненужная
    rasst = 100            
    # надо чтоб проверять, сдвинулась ли карта, чтоб лишний раз не перерисовывать
    changed = False        
    # хуярим основную карту с биомами
    biomMap = map.createMyMap(1, Dlmatr)  
    # политическую карту
    politicalMap = map.createMyMap(2, Dlmatr)
    # карту с железом
    ironMap = map.createMyMap(3, Dlmatr) 
    # карту с зерном
    grainMap = map.createMyMap(4, Dlmatr)  

    # тестовое государство 1
    state1 = state.State('Pidronija',(100,0,0))     
    # 2
    state2 = state.State('Lochonija',(0,0,100))     
     # назначаем страты населения
    serf, worker, soldier,schoolers = strata.Existing_Strat()    
    pakistani, indian = culture.exist_cult()
    jewish,sunni = religion.exist_rel()

    # задание распределения между возрастами
    male_age = np.zeros(75, dtype=np.uint16)
    male_age[21] = 100
    female_age = np.asarray(male_age, copy = True)  

    
    # болванчик для того, чтоб создать город (он привязывается к населению)
    # но такое у меня чувство, что я эту механику уберу
    bolvan = Pops(15,male_age,female_age,serf,pakistani,sunni,100,1,0,False)     

    # тестовые города
    city = Settlement(state1,(50,60),biomMap,'Gasovodsk',bolvan,schoolers)     
    town = Settlement(state1,(60,70),biomMap,'Gorod1',bolvan,schoolers)
    city1 = Settlement(state1,(55,60),biomMap,'Gorod2',bolvan,schoolers)
    town1 = Settlement(state1,(65, 70), biomMap, 'Gorod3',bolvan,schoolers)
    Settlement(state1,(50,65), biomMap,'Gorny',bolvan,schoolers)
    Settlement(state1, (70, 70), biomMap, 'Zernograd', bolvan,schoolers)

    # назначаем производимые товары
    grain, fertilizer, fish, whool, fabric, iron = goods.existing_goods()   


    # назначаем попы - pop - экземпляр "единицы" населения
    Pops(Settlement.cities['Zernograd'], male_age.copy(),female_age.copy(), serf,pakistani,sunni, 100,1)   
    Pops(Settlement.cities['Gasovodsk'],male_age.copy(),female_age.copy(),serf,pakistani,sunni,100,1)
    Pops(Settlement.cities['Gorod1'],male_age.copy(),female_age.copy(),serf,pakistani,sunni,100,1)
    Pops(Settlement.cities['Gorod2'], male_age.copy(),female_age.copy(),serf,pakistani,sunni, 100, 1)
    Pops(Settlement.cities['Gorod3'], male_age.copy(),female_age.copy(),serf,pakistani,sunni, 100, 1)
    Pops(Settlement.cities['Gorny'],male_age.copy(),female_age.copy(),worker,pakistani,sunni,100,1)
    # назначаем заводы
    Factory(Settlement.cities['Zernograd'], serf, grain, 200, 1, 1000, 0,True)     
    Factory(Settlement.cities['Gasovodsk'],serf,grain,200,1,1000,0,True)
    Factory(Settlement.cities['Gorod1'], serf, fertilizer, 1000, 1, 1000)
    Factory(Settlement.cities['Gorod2'],serf,fish,200,1,1000,0,True)
    Factory(Settlement.cities['Gorod3'], serf, fertilizer, 1000, 1, 1000)
    Factory(Settlement.cities['Gorny'],worker,iron,1000,1,1000)

    # Инициализация pygame
    pg.init()

    # sc = pg.display.set_mode((DlinaX, DlinaY))
    sc = pg.display.set_mode((Dlina, Dlina))
    background = pg.Surface((Dlmatr, Dlmatr))
    background.fill((0, 0, 150))
    politbg = pg.Surface((Dlmatr, Dlmatr),flags=pg.SRCALPHA)
    pbg = pg.Surface((Dlmatr, Dlmatr), flags=pg.SRCALPHA)
    pbg.set_alpha(100)

    # info_window = pg.Surface((DlinaX-100,DlinaY-100))
    info_window = pg.Surface((Dlina - 100, Dlina - 100))
    info_window.fill((190,210,40))
    infowind_rect = info_window.get_rect()


    for i in range(Dlmatr):
        for j in range(Dlmatr):
            if biomMap[i, j] == 1:
                background.set_at((i, j), (0, 90, 0))
            elif biomMap[i, j] == 2:
                background.set_at((i, j), (50, 50, 50))
            elif biomMap[i, j] == 3:
                background.set_at((i, j), (50, 50, 50))
            elif biomMap[i, j] == 4:
                background.set_at((i, j), (0, 0, 0))
            elif biomMap[i, j] == 5:
                background.set_at((i, j), (120, 150, 0))


    ironbackground = pg.Surface.copy(background)
    ibiomMap = np.array(biomMap, copy=True)

    for i in range(Dlmatr):
        for j in range(Dlmatr):
            if ironMap[i, j] > 20:
                ironbackground.set_at((i, j), (ironMap[i, j], 0, 255 - ironMap[i, j]))
                ibiomMap[i, j] = ironMap[i, j]


    bg = pg.Surface((Dlmatr, Dlmatr))
    bg.fill((0, 0, 150))
    for i in range(Dlmatr):
        for j in range(Dlmatr):
            for k in state.State.statenumberdict:
                if politicalMap[i, j] == k:
                    politbg.set_at((i, j), state.State.statenumberdict[k].colour)

    politbg.set_alpha(100)

    rivers.River.count_places(1,biomMap)
    rivers.River.count_attractiveness(1,grainMap)

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
    city_window_opened = False
    pop_window_opened = False
    fact_window_opened = False


    while 1:
        """всё хуярится через вайл"""
        #print('СДЕЛАТЬ МИГРАЦИЮ И ПОИСК НОВОЙ РАБОТЫ, А ПОТОМ ЦЕНООБРАЗОВАНИЕ И БЛЯ ЕЩЁ ЧТО-ТО')

        #print('НЕ ПОКУПКА УСИЛИТЕЛЯ, ЕСЛИ КОНЕЧНАЯ ЦЕНА ПРОДУКТА СЛИШКОМ НИЗКАЯ')
        for i in pg.event.get(): # зачем стоит for? может ли приходить больше ивентов чем один, если стоит while?
            """обрабатывается нажатие клавиш клавиатуры с pygame"""
            # Переписать через свитч и вынести в отдельный класс (например Game, где будут висеть обработчики)
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
                    # bg = pg.Surface((DlinaX, DlinaY))
                    # risov(xe,xg,ye,yg,rasst,pribl,DlinaX,DlinaY,biomMap,bg)
                    bg = pg.Surface((Dlina, Dlina))
                    draw(xe, xg, ye, yg, rasst, pribl, Dlina, biomMap, bg)
                    sur = bg


        """что если в каждом поселении сделать 1 поп на класс (с разделением на возраст) и его части отправлять на разные типы
        работы (религия? культура? можно попытаться тоже процентно делать), а деньги сохранять либо в отдельных массивах, либо прямо на заводе, т.е. деньги рабочих хранятся только на заводе
        и тратятся только соответственно с потребностями в количестве доли той части рабочих, которые работают именно там"""
        """
        можно ещё сделать разные типы оплаты труда (в зависимости от социальной политики государства/предприятия)
        например сдельная оплата, оплата по дням, оплата за месяц (т.е. при отсутствии работы, зарплата всё равно будет
        платиться)
        """

        """
        нужно сделать пересчёт процентов рабочих разных рабочих при изменении численности населения. и распределить
        убывание рабочих по заводам при смерти в соответствии с процентами
        """


        if xt//100 - weekdistribution > 0:
            """распределение по работе попов"""
            print('distribution')
            weekdistribution += 1
            for city_index in Settlement.cities:     # по каждому городу в общем словаре городов
                iter_for_pops = list(Settlement.cities[city_index].pops)         # этот лист ввёл ибо добавляются новые попы в процессе
                Settlement.if_not_full(Settlement.cities[city_index])
                for pop_index in iter_for_pops:      # для каждого попа в этом городе
                    if Settlement.cities[i].pops[pop_index].unemployed == 1:     # нужно чтобы отделить попы заводские от безработных
                        if Settlement.cities[i].pops[pop_index].num != 0:            # ежели есть кто из работяг в попе
                            Settlement.subiomMapakubow(Settlement.cities[i],Settlement.cities[i].pops[pop_index])     # считаем нормировку для коэффициентов распределения попов по заводам
                            for factory_index in Settlement.cities[i].factories:             # распределяем по этим заводам, которые все находятся в этом городе
                                if k.work_type == Settlement.cities[i].pops[pop_index].strata:     # проверка, подходит ли завод типу попа. ибо священники на заводах не въёбывают
                                    Factory.coef(Settlement.cities[i].factories[factory_index])     # считаем коэффициенты
                                Pops.facsearch(Settlement.cities[i].pops[pop_index])     # непосредственно распределяем население попа в соответствии с коэффициентами

        #######################################
        """ if xt == 1000:
            sui = 1
            faq = [0]
            #faq = np.array([0], dtype=np.uint16)
            for i1 in range(1000000000):
                #np.append(faq,10)
                faq.append(10)
                if i1//1000000 - sui == 0:
                    print(i1)
                    sui += 1

        if xt == 2000:
            for i1 in range(1000000000):
                faq[i1] = faq[i1]*2"""
        ########################################



        if (xt-25)//100 - weekbuying > 0:
            """покупка всего и вся"""
            print('buying')
            weekbuying += 1
            treck = {}
            trecksell = {}
            for i in Settlement.cities:                       # по всем городам
                for j in Settlement.cities[i].factories:     # и заводам в этих городах
                    Factory.factbuy(j)                       # завод покупает нужные ресурсы
                    Factory.factboostbuy(j)                  # и бустеры (типа удобрения для С/Х)
                    Factory.popbuy(j)                       # и жратву своим рабочим и тд
                for j in Settlement.cities[i].pops:     # теперь для попов
                    Pops.popbuy(j)                    # покупают жрачку и т.д.


        if (xt-30)//100 - weekpricechanging > 0:
            """корректировка цен"""
            print('price')
            weekpricechanging += 1
            for i in Settlement.cities:
                for j in Settlement.cities[i].factories:
                    if j.type:           # отдаю деньги и жратву крестьянам.
                        Factory.givefoodmoney(j)
                        Factory.wage_change(j)
                    if 1 in j.price_changed.values():
                        Factory.pricechangeagain(j)
                    elif 2 in j.price_changed.values():
                        Factory.pricechangeagain(j)
                    else:
                        Factory.pricechange(j)


        if (xt-50)//100 - weekproduction > 0:
            """производство"""
            print('production')
            weekproduction += 1
            for i in Settlement.cities:
                for j in Settlement.cities[i].factories:
                    Factory.create(Settlement.cities[i].factories[j],grainMap)



        if (xt-75)//100 - weekconsumption > 0:
            """потребление"""
            print('consumption')
            weekconsumption += 1
            for i in Settlement.cities:
                for j in Settlement.cities[i].factories:
                    if j.num_workers != 0:
                        Factory.consume_food(j)
                for j in Settlement.cities[i].pops:
                    if j.num != 0:
                        Pops.consume_food(Settlement.cities[i].pops[j])

        if (xt-95)//100 - weekcorrections > 0:
            """корректировка населения. смерть-рождение"""
            print('corrections')
            weekcorrections += 1
            for i in Settlement.cities:
                iter_for_pops = list(Settlement.cities[i].pops) # этот лист ввёл ибо удаляются пустые попы в процессе
                for j in iter_for_pops:
                    if not Settlement.cities[i].pops[j].unemployed:
                        Pops.popchange(Settlement.cities[i].pops[j])

                        if Settlement.cities[i].pops[j].total_num == 0:                            # удаляем пустые попы. чтоб память не жрали
                            Settlement.cities[i].pops[j].location.state.money += Settlement.cities[i].pops[j].money           # перемещаем их деньги и инвентарь в казну
                            for key in Settlement.cities[i].pops[j].inventory:                     # а удалять у самих попов смысла нет - удаляем поп полностью
                                if key in Settlement.cities[i].pops[j].location.state.inventory:
                                    Settlement.cities[i].pops[j].location.state.inventory[key] += Settlement.cities[i].pops[j].inventory[key]
                                else:
                                    Settlement.cities[i].pops[j].location.state.inventory[key] = Settlement.cities[i].pops[j].inventory[key]
                            del Settlement.cities[i].pops[j]
                iter_for_pops = list(Settlement.cities[i].pops)
                for j in iter_for_pops:
                    if Settlement.cities[i].pops[j].unemployed:
                        Pops.popchange(Settlement.cities[i].pops[j])

                        if Settlement.cities[i].pops[j].total_num == 0:  # удаляем пустые попы. чтоб память не жрали
                            Settlement.cities[i].pops[j].location.state.money += Settlement.cities[i].pops[
                                j].money  # перемещаем их деньги и инвентарь в казну
                            for key in Settlement.cities[i].pops[
                                j].inventory:  # а удалять у самих попов смысла нет - удаляем поп полностью
                                if key in Settlement.cities[i].pops[j].location.state.inventory:
                                    Settlement.cities[i].pops[j].location.state.inventory[key] += \
                                    Settlement.cities[i].pops[j].inventory[key]
                                else:
                                    Settlement.cities[i].pops[j].location.state.inventory[key] = \
                                    Settlement.cities[i].pops[j].inventory[key]
                            del Settlement.cities[i].pops[j]
                Settlement.stlpopul(Settlement.cities[i])
                Settlement.city_growth(Settlement.cities[i],biomMap,background,grainMap)
            sui = 0
            for i in Settlement.cities:
                for j in Settlement.cities[i].pops:
                    sui += j.male_age[10]




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
                    # risov(xe, xg, ye, yg, rasst, pribl, DlinaX,DlinaY, biomMap, bg)
                    draw(xe, xg, ye, yg, rasst, pribl, Dlina, biomMap, bg)
                elif mapmode == 1:
                    # risov(xe, xg, ye, yg, rasst, pribl, DlinaX,DlinaY, biomMap, bg)
                    # politrisov(xe,xg,ye,yg,rasst,pribl,DlinaX,DlinaY,pm,pbg)
                    draw(xe, xg, ye, yg, rasst, pribl, Dlina, biomMap, bg)
                    politrisov(xe, xg, ye, yg, rasst, pribl, Dlina, politicalMap, pbg)
                elif mapmode == 2:
                    # risov(xe, xg, ye, yg, rasst, pribl, DlinaX,DlinaY, ibiomMap, bg)
                    draw(xe, xg, ye, yg, rasst, pribl, Dlina, ibiomMap, bg)
                changed = False

        pressed = pg.mouse.get_pressed()
        pos = pg.mouse.get_pos()
        if pressed[0]:
            xa,ya = pos
            # xe = xe + (xa - xg)
            # ye = ye + (ya - yg)

        ## существует проблема обновления карты в приближённом состоянии в реальном времени


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


        if pressed[0]:
            if city_window_opened:
                for i in pops_button:
                    if pg.Rect.collidepoint(pops_button[i], pos):
                        pop_window_opened = True
                        pwo_pop = i
                        city_window_opened = False
                        pop_cons = {}
                        for j in pwo_pop.strata.cons:
                            pop_cons[j] = f1.render(j + ': ' + str(pwo_pop.strata.cons[j]), 0, (0, 0, 0))  #
                for i in factories_button:
                    if pg.Rect.collidepoint(factories_button[i], pos):
                        fact_window_opened = True
                        city_window_opened = False
                        fact_pop_cons = {}
                        fwo_fact = i
                        for j in factories_in_city[i][6]:
                            fact_pop_cons[j] = f1.render(j + ': ' + str(factories_in_city[i][6][j]), 0, (0, 0, 0))  #


        if city_window_opened:
            info_window.fill((190,210,40))
            male_age_city = np.array(
                (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), dtype=np.uint16)
            female_age_city = np.array(
                (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), dtype=np.uint16)
            for j in pops_in_city:
                for k in range(len(j.male_age)):
                    male_age_city[k] += j.male_age[k]
                    female_age_city[k] += j.female_age[k]
            for j in range(len(male_age_city)):
                pg.draw.line(info_window, (100, 100, 250), (200 - male_age_city[j], 300 - 2 * j),
                             (200, 300 - 2 * j), 2)
                pg.draw.line(info_window,(250,100,100),(200, 300 - 2 * j),(200 + female_age_city[j], 300 - 2 * j),2)
            sc.blit(info_window,(50,50))
            text_city_name = f1.render(settlement_to_show.name,0,(0,0,0))
            sc.blit(text_city_name,(60,60))
            text_city = f1.render('Population: ' + str(settlement_to_show.population),0,(0,0,0))
            sc.blit(text_city, (200, 60))
            text_city = f1.render('Factories:',0,(0,0,0))
            sc.blit(text_city,(60,100))

            # сделать тут кнопку, чтоб показывать детали про попы: численность, инвентарь, деньги, безработица
            # то же самое сделать с заводами: число рабочих, инвентарь, деньги, основные поставщики, динамика цен, динамика другого
            # запрогать хотя бы минимально государства
            # уже не здесь, но в целом сделать окно с общей информацией по всем городам ГОСУДАРСТВА, а в ней уже сделать кнопку для
            # каждого отдельного города (в ЭТО окно)

            fic_cnt = 0
            for j in factories_in_city:
                text_city = f1.render(factories_in_city[j][0] + ' Workers: ' + str(factories_in_city[j][1])+'/'+
                                                                                   str(factories_in_city[j][2])+
                                      ' Money: '+str(factories_in_city[j][3])+ ' W_Money: '+ str(factories_in_city[j][4])+
                                      ' Wage: '+str(factories_in_city[j][5]),0,(0,0,0))
                sc.blit(text_city,(160+fic_cnt*100,100))
                fic_cnt+=1
            #j.good.name, j.num_workers, j.fullnum, j.money, j.workers_money, j.gehalt, j.inventory, j.sell

            # пишем, какие есть попы (страта, культура, религия)
            for j in range(len(pops_array)):
                for ij in range(len(pops_array[j])):
                    sc.blit(pops_array[j][ij], (360+ij*100, 60 + 20*j))

            # надо сделать массив с кнопками - на каждый поп по кнопке с определёнными координатами и т.д.
            # но это при создании окна с информацией




            if pressed[0] and not pg.Rect.collidepoint(infowind_rect,pos[0],pos[1]):
                city_window_opened = False



        elif pop_window_opened:
            info_window.fill((190, 210, 40))
            for j in range(len(pwo_pop.male_age)):
                pg.draw.line(info_window, (100, 100, 250), (200 - pwo_pop.male_age[j], 300 - 2 * j),
                             (200, 300 - 2 * j), 2)
                pg.draw.line(info_window,(250,100,100),(200, 300 - 2 * j),(200 + pwo_pop.female_age[j], 300 - 2 * j),2)
            sc.blit(info_window, (50, 50))
            text_city = f1.render(pwo_pop.strata.name + ' ' + pwo_pop.culture.name + ' ' +  pwo_pop.religion.name, 0, (0, 0, 0))
            # сделать пересчёт всех заводов, чтобы видеть, сколько денег имеет именно этот поп
            sc.blit(text_city, (200, 60))
            text_city = f1.render('Cons: ', 0, (0, 0, 0))
            sc.blit(text_city, (400, 60))


            i123 = 0
            for i in pop_cons:
                sc.blit(pop_cons[i],(460+i123*100, 60))
                i123 += 1




            if pressed[0] and not pg.Rect.collidepoint(infowind_rect,pos[0],pos[1]):
                pop_window_opened = False



        elif fact_window_opened:
            info_window.fill((190, 210, 40))
            sc.blit(info_window, (50, 50))


            text_city = f1.render(fwo_fact.good.name + ' Workers: ' + str(fwo_fact.num_workers) + '/' +
                                  str(fwo_fact.fullnum) +
                                  ' Money: ' + str(fwo_fact.money) + ' W_Money: ' + str(
                fwo_fact.workers_money) +
                                  ' Wage: ' + str(fwo_fact.gehalt), 0, (0, 0, 0))
            sc.blit(text_city, (160, 50))


            i123 = 0
            for i in fact_pop_cons:
                sc.blit(fact_pop_cons[i], (160 + i123 * 100, 60))
                i123 += 1

            if pressed[0] and not pg.Rect.collidepoint(infowind_rect,pos[0],pos[1]):
                fact_window_opened = False





        q1 = 0
        for q in Settlement.cities:
            if pg.Rect.collidepoint(Settlement.arry[q1][0],(pos[0]-xe,pos[1]-ye)):
                if pressed[0]:
                    city_window_opened = True
                    settlement_to_show = Settlement.cities[q]
                    factories_in_city = {}
                    factories_button = {}
                    counter = 0
                    for j in Settlement.cities[q].factories:
                        factories_in_city[j] = (j.good.name,j.num_workers,j.fullnum, j.money, j.workers_money, j.gehalt, j.inventory, j.sell)
                        factories_button[j] = pg.Rect(160, 100 + 20 * counter, 100, 20)
                        counter+=1


                    pops_in_city = Settlement.cities[q].pops.copy()
                    pops_array = []
                    pops_button = {}

                    counter = 0
                    for key in pops_in_city:    # делаем массив с данными о попах в этом поселении
                        pops_array.append([])
                        pops_array[counter].append(f1.render(key.strata.name,0, (0, 0, 0)))
                        pops_array[counter].append(f1.render(key.culture.name,0, (0, 0, 0)))
                        pops_array[counter].append(f1.render(key.religion.name,0, (0, 0, 0)))
                        pops_button[key] = pg.Rect(360,50+20*counter,100,20)
                        counter +=1

                    counter_f = 0



                citytext = f1.render(Settlement.cities[q].name, 0, (0, 0, 0))
                citytext1 = f1.render(str(Settlement.cities[q].population),0,(0,0,0))

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


        pg.time.delay(10)
        if not pause:
            xt += 1                                          # счётчик времени


if __name__ == "__main__":
    main()
