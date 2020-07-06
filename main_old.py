import class_and_agent
import numpy as np
import strata
import settlement
import pygame as pg
import goods
import pops
import factory
import state
import culture
import religion
import rivers
import maps as map
from camera import draw, politrisov

"""
def risov(xe,xg,ye,yg,rasst,pribl,DlinaX,DlinaY,mm,bg):
	
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
	
	for i in range(-xe + xg - (DlinaX // (2 * pribl)),
				   -xe + xg + (DlinaX // (2 * pribl))):
		for j in range(-ye + yg - (DlinaY // (2 * pribl)),
					   -ye + yg + (DlinaY // (2 * pribl))):

			if mm[i, j] == 1:
				if bg.get_at(((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
											   (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl)) != (0,100,0):
					pg.draw.rect(bg, (0, 100, 0), ((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
											   (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl,
											   pribl, pribl))

			elif mm[i, j] == 2:
				if bg.get_at(((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
							  (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl)) != (50, 50, 50):
					pg.draw.rect(bg, (50, 50, 50), ((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
												   (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl,
												   pribl, pribl))
			elif mm[i, j] == 3:
				if bg.get_at(((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
							  (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl)) != (50, 50, 50):
					pg.draw.rect(bg, (50, 50, 50), ((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
												(j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl,
												pribl, pribl))
			elif mm[i, j] == 4:
				if bg.get_at(((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
							  (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl)) != (0, 0, 0):
					pg.draw.rect(bg, (0, 0, 0), ((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
											 (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl,
											 pribl, pribl))
			elif mm[i, j] == 5:
				if bg.get_at(((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
							  (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl)) != (120, 150, 0):
					pg.draw.rect(bg, (120, 150, 0), ((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
											   (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl,
											   pribl, pribl))
			elif mm[i, j] == 0:
				if bg.get_at(((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
							  (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl)) != (0, 0, 150):
					pg.draw.rect(bg, (0, 0, 150), ((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
											   (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl,
											   pribl, pribl))
			elif mm[i,j] >20:
				if bg.get_at(((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
							  (j - (-ye + yg - (DlinaY // (2 * pribl)))) * pribl)) != (mm[i,j], 0, 255 - mm[i,j]):
					pg.draw.rect(bg, (mm[i,j], 0, 255 - mm[i,j]), ((i - (-xe + xg - (DlinaX // (2 * pribl)))) * pribl,
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
	политическая карта
	pm = np.zeros((Dlmatr,Dlmatr) ,dtype=np.uint8)
	pm[30:100, 40:100] = 1
	pm[430:500, 440:500] = 2
	return pm

def ironmm(Dlmatr):
	карта с залежами железа
	rm = np.zeros((Dlmatr,Dlmatr),dtype=np.uint8)
	rm[52,62] = 15
	rm[54, 61] = 120
	rm[56, 63] = 210
	rm[52, 66] = 73
	rm[50, 62] = 117
	return rm

def grainmm(Dlmatr):
	
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
	#DlinaX = 1300                                     # сколько пикселей экран
	#DlinaY = 600
	Dlina = 600
	Dlmatr = 1000                                   # сколько пикселей карта
	rasst = 100                                     # хуйня ебаная ненужная
	changed = False                                 # надо чтоб проверять, сдвинулась ли карта, чтоб лишний раз не перерисовывать
	mm = map.createMyMap(1, Dlmatr)  # хуярим основную карту с биомами
	politicalMap = map.createMyMap(2, Dlmatr)  # политическую карту
	ironMap = map.createMyMap(3, Dlmatr)  # карту с железом
	grainMap = map.createMyMap(4, Dlmatr)  # карту с зерном

	state1 = state.State('Pidronija',(100,0,0))     # тестовое государство 1
	state2 = state.State('Lochonija',(0,0,100))     # 2

	serf, worker, soldier,schoolers,enterpreneurs = strata.Existing_Strat(state1)     # назначаем страты населения
	pakistani, indian = culture.exist_cult()
	jewish,sunni = religion.exist_rel()

	# male_age = np.zeros(75, dtype=np.uint16)
	# male_age[21] = 100
	# female_age = np.asarray(male_age)         # потом гуглануть, копирование это или присвоение. я так уже несколько раз проёбывался

	male_age = np.array((0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,100,0,0,0,0,0,0,0,0,
								  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
								  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0), dtype=np.uint16)
	female_age = np.array((0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,100,0,0,0,0,0,0,0,0,
								  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
								  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0), dtype=np.uint16)

	#bolvan = pops.Pops(15,male_age,female_age,serf,pakistani,sunni,100,1,0,False)     # болванчик для того, чтоб создать город (он привязывается к населению)
														# но такое у меня чувство, что я эту механику уберу

	city = settlement.Settlement(state1,(32,48),mm,'Gasovodsk')     # тестовые города
	town = settlement.Settlement(state1,(62,62),mm,'Gorod1')
	city1 = settlement.Settlement(state1,(52,50),mm,'Gorod2')
	town1 = settlement.Settlement(state1,(65, 70), mm, 'Gorod3')
	settlement.Settlement(state1,(50,65), mm,'Gorny')
	settlement.Settlement(state1, (52, 62), mm, 'Zernograd')


	grain, fertilizer, fish, whool, fabric, iron, instruments = goods.existing_goods()     # назначаем производимые товары



	pops.Pops(settlement.Settlement.slovar['Zernograd'], male_age.copy(),female_age.copy(), serf,pakistani,sunni, 100,1)      # назначаем попы - pop - экземпляр "единицы" населения
	pops.Pops(settlement.Settlement.slovar['Gasovodsk'],male_age.copy(),female_age.copy(),serf,pakistani,sunni,100,1)
	pops.Pops(settlement.Settlement.slovar['Gorod1'],male_age.copy(),female_age.copy(),serf,pakistani,sunni,100,1)
	pops.Pops(settlement.Settlement.slovar['Gorod2'], male_age.copy(),female_age.copy(),serf,pakistani,sunni, 100, 1)
	pops.Pops(settlement.Settlement.slovar['Gorod3'], male_age.copy(),female_age.copy(),worker,pakistani,sunni, 100, 1)
	pops.Pops(settlement.Settlement.slovar['Gorny'],male_age.copy(),female_age.copy(),worker,pakistani,sunni,100,1)
	factory.Factory(settlement.Settlement.slovar['Zernograd'], serf, grain, 200, 1, 1000, 0,True)     # назначаем заводы
	factory.Factory(settlement.Settlement.slovar['Gasovodsk'],serf,grain,200,1,1000,0,True)
	factory.Factory(settlement.Settlement.slovar['Gorod1'], serf, fertilizer, 1000, 1, 1000)
	factory.Factory(settlement.Settlement.slovar['Gorod2'],serf,fish,200,1,1000,0,True)
	factory.Factory(settlement.Settlement.slovar['Gorod3'], worker, instruments, 1000, 1, 1000)
	factory.Factory(settlement.Settlement.slovar['Gorny'],worker,iron,1000,1,1000,resource_map=ironMap)

	pg.init()

	# sc = pg.display.set_mode((DlinaX, DlinaY))
	sc = pg.display.set_mode((Dlina, Dlina))
	background = pg.Surface((Dlmatr, Dlmatr))
	background.fill((0, 0, 150))
	politbg = pg.Surface((Dlmatr, Dlmatr),flags=pg.SRCALPHA)
	pbg = pg.Surface((Dlmatr, Dlmatr), flags=pg.SRCALPHA)
	pbg.set_alpha(100)

	# info_window = pg.Surface((DlinaX-100,DlinaY-100))

	# окно для различной информации
	info_window = pg.Surface((Dlina - 100, Dlina - 100))
	info_window.fill((190,210,40))
	infowind_rect = info_window.get_rect(topleft=(50, 50))

	# верхняя полоска интерфейса
	UI_window = pg.Surface((Dlina,60))
	UI_window.fill((100,100,20))


	for i in range(Dlmatr):
		for j in range(Dlmatr):
			if mm[i, j] == 1:
				background.set_at((i, j), (0, 90, 0))
			elif mm[i, j] == 2:
				background.set_at((i, j), (50, 50, 50))
			elif mm[i, j] == 3:
				background.set_at((i, j), (0, 50, 0))
			elif mm[i, j] == 4:
				background.set_at((i, j), (0, 0, 0))
			elif mm[i, j] == 5:
				background.set_at((i, j), (120, 150, 0))


	ironbackground = pg.Surface.copy(background)
	imm = np.array(mm, copy=True)

	for i in range(Dlmatr):
		for j in range(Dlmatr):
			if ironMap[i, j] > 20:
				ironbackground.set_at((i, j), (ironMap[i, j], 0, 255 - ironMap[i, j]))
				imm[i, j] = ironMap[i, j]


	bg = pg.Surface((Dlmatr, Dlmatr))
	bg.fill((0, 0, 150))
	for i in range(Dlmatr):
		for j in range(Dlmatr):
			for k in state.State.statenumberdict:
				if politicalMap[i, j] == k:
					politbg.set_at((i, j), state.State.statenumberdict[k].colour)

	politbg.set_alpha(100)

	rivers.River.count_places(1,mm)
	rivers.River.count_attractiveness(1,grainMap,mm)

	xb = 0
	yb = 0

	sc.blit(background, (xb, yb))

	pg.display.update()


	xe, ye = xb, yb
	xg, yg = 0, 0
	sur = background
	pribl = 1
	f1 = pg.font.Font(None, 20)
	
	"""время делаем следующим образом:
	1 день - это 100 прогонов (т.е delta xt = 100)
	тогда 700 прогонов - 1 неделя
	3 000 прогонов - 1 месяц
	36 000 прогонов - 1 год
	"""
	oneday = 100
	oneweek = 700
	onemonth = 3000
	oneyear = 36000
	
	
	weekdays = ('Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье')
	months = ('Января','Февраля','Марта','Апреля','Мая','Июня','Июля','Августа','Сентября','Октября','Ноября','Декабря')

	currentday = 1
	currentweekday = 1
	currentmonth = 1
	currentyear = 1800
	
	xt = 0






	but_polit = pg.Surface((100,30))    # кнопка для политической карты
	but_resource = pg.Surface((100,30))    # для ресурсной
	but_time = pg.Surface((150, 30))    # для показателя времени
	but_trade = pg.Surface((100, 30))
	
	
	but_pause = pg.Surface((30, 30))    # для паузы
	but_go = pg.Surface((30, 30))    # для различных скоростей
	but_gogo = pg.Surface((30, 30))
	but_gogogo = pg.Surface((30, 30))


	UI_window.fill((100,100,20))
	but_time.fill((100,100,20))
	but_polit.fill((100, 100, 20))
	but_resource.fill((100, 100, 20))
	but_trade.fill((100, 100, 20))

	but_pause.fill((200,20,20))
	but_go.fill((20,200,20))
	but_gogo.fill((20,200,20))
	but_gogogo.fill((20,200,20))

	# обрамление кнопок чёрными границами
	pg.draw.rect(but_polit, (0, 0, 0), (0, 0, 100, 30), 2)
	pg.draw.rect(but_resource, (0, 0, 0), (0, 0, 100, 30), 2)
	pg.draw.rect(but_time,(0,0,0),(0,0,150,30),2)
	pg.draw.rect(but_trade, (0, 0, 0), (0, 0, 100, 30), 2)

	pg.draw.rect(but_pause, (0, 0, 0), (0, 0, 30, 30), 2)
	pg.draw.line(but_pause, (200,200,200), [10, 5], [10, 25], 3)
	pg.draw.line(but_pause, (200, 200, 200), [20, 5], [20, 25], 3)

	# а тут до кучи рисование стрелочек для кнопок скорости течения времени
	pg.draw.rect(but_go, (0, 0, 0), (0, 0, 30, 30), 2)
	pg.draw.lines(but_go, (200, 200, 200), True, [[10, 5], [10, 25], [20, 15]], 3)
	pg.draw.rect(but_gogo, (0, 0, 0), (0, 0, 30, 30), 2)
	pg.draw.lines(but_gogo, (200, 200, 200), True, [[5, 5], [5, 25], [15, 15]], 3)
	pg.draw.lines(but_gogo, (200, 200, 200), True, [[15, 5], [15, 25], [25, 15]], 3)
	pg.draw.rect(but_gogogo, (0, 0, 0), (0, 0, 30, 30), 2)
	pg.draw.lines(but_gogogo, (200, 20, 20), True, [[10, 5], [10, 25], [20, 15]], 6)

	text1 = f1.render(str(xt // 10), 0, (0, 0, 0))  # кнопочки и другой текст
	UI_window.blit(text1, (10, 5))
	text2 = f1.render('Политика',0,(0,0,0))
	but_polit.blit(text2,(20,5))
	text3 = f1.render('Ресурсы',0,(0,0,0))
	but_resource.blit(text3,(10,5))
	text4 = f1.render('Торговля', 0, (0, 0, 0))
	but_trade.blit(text4, (10, 5))
	UI_window.blit(but_polit, (150, 0))
	UI_window.blit(but_resource, (250, 0))
	UI_window.blit(but_trade, (350, 0))
	
	UI_window.blit(but_pause, (0, 30))
	UI_window.blit(but_go, (30, 30))
	UI_window.blit(but_gogo, (60, 30))
	UI_window.blit(but_gogogo, (90, 30))

	sc.blit(UI_window, (0, 0))

	# размещаю кнопки на экране, чтобы потом можно было на них нажимать (ниже в самом начале цикла while 1)
	but_polit_rect = but_polit.get_rect(topleft=(150, 0))
	but_resource_rect = but_resource.get_rect(topleft=(250, 0))
	but_time_rect = but_time.get_rect(topleft=(0, 0))
	but_trade_rect = but_trade.get_rect(topleft=(350, 0))

	but_pause_rect = but_pause.get_rect(topleft=(0, 30))
	but_go_rect = but_go.get_rect(topleft=(30, 30))
	but_gogo_rect = but_gogo.get_rect(topleft=(60, 30))
	but_gogogo_rect = but_gogogo.get_rect(topleft=(90, 30))




	weekdistribution = 0                 # все эти хуйни недельные - это для распределения нагрузки в течение дня/недели
	weekproduction = 0                   # и так далее. тип утром распределились на работу, днём произвели товар, вечером потрах... скорректировали население
	weekconsumption = 0
	weekbuying = 0
	weekpricechanging = 0
	weekcorrections = 0
	monthmap = 0
	mapmode = 0
	pause = False
	delay = 1
	city_window_opened = False
	pop_window_opened = False
	fact_window_opened = False
	trade_window_opened = False


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
					if pg.Rect.collidepoint(but_polit_rect, pos[0], pos[1]):
						if mapmode != 1:
							mapmode = 1
						else:
							mapmode = 0
					elif pg.Rect.collidepoint(but_resource_rect, pos[0], pos[1]):
						if mapmode != 2:
							mapmode = 2
						else:
							mapmode = 0

					elif pg.Rect.collidepoint(but_pause_rect, pos[0], pos[1]):
						if not pause:
							pause = True
						else:
							pause = False
							# speed = 1

					elif pg.Rect.collidepoint(but_go_rect, pos[0], pos[1]):
						pause = False
						delay = 20


					elif pg.Rect.collidepoint(but_gogo_rect, pos[0], pos[1]):
						pause = False
						delay = 10

					elif pg.Rect.collidepoint(but_gogogo_rect, pos[0], pos[1]):
						pause = False
						delay = 1
					
					elif pg.Rect.collidepoint(but_trade_rect, pos[0], pos[1]):
						trade_window_opened = True

				if i.button == 3:
					xg,yg = i.pos[0], i.pos[1]
					print(pos,xe,ye)
					pribl = pribl*10
					# bg = pg.Surface((DlinaX, DlinaY))
					# risov(xe,xg,ye,yg,rasst,pribl,DlinaX,DlinaY,mm,bg)
					bg = pg.Surface((Dlina, Dlina))
					draw(xe, xg, ye, yg, rasst, pribl, Dlina, mm, bg)
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
			for i in settlement.Settlement.slovar:     # по каждому городу в общем словаре городов
				iter_for_pops = list(settlement.Settlement.slovar[i].pops)         # этот лист ввёл ибо добавляются новые попы в процессе
				settlement.Settlement.if_not_full(settlement.Settlement.slovar[i])
				for j in iter_for_pops:      # для каждого попа в этом городе
					if settlement.Settlement.slovar[i].pops[j].unemployed == 1:     # нужно чтобы отделить попы заводские от безработных
						if settlement.Settlement.slovar[i].pops[j].num != 0:            # ежели есть кто из работяг в попе
							settlement.Settlement.summakubow(settlement.Settlement.slovar[i],settlement.Settlement.slovar[i].pops[j])     # считаем нормировку для коэффициентов распределения попов по заводам
							for k in settlement.Settlement.slovar[i].factories:             # распределяем по этим заводам, которые все находятся в этом городе
								if k.work_type == settlement.Settlement.slovar[i].pops[j].strata:     # проверка, подходит ли завод типу попа. ибо священники на заводах не въёбывают
									factory.Factory.coef(settlement.Settlement.slovar[i].factories[k])     # считаем коэффициенты
								pops.Pops.facsearch(settlement.Settlement.slovar[i].pops[j])     # непосредственно распределяем население попа в соответствии с коэффициентами
			for fc in factory.Factory.slovar.values():
				print(fc.num_workers,fc.good.name, fc.location.name)

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
			for i in settlement.Settlement.slovar:                       # по всем городам
				for j in settlement.Settlement.slovar[i].factories:     # и заводам в этих городах
					factory.Factory.factbuy(j)                       # завод покупает нужные ресурсы
					factory.Factory.factboostbuy(j)                  # и бустеры (типа удобрения для С/Х)
					factory.Factory.popbuy(j)                       # и жратву своим рабочим и тд
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
						factory.Factory.wage_change(j)
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
			for i in settlement.Settlement.slovar:
				for j in settlement.Settlement.slovar[i].factories:
					factory.Factory.create(settlement.Settlement.slovar[i].factories[j],grainMap)



		if (xt-75)//100 - weekconsumption > 0:
			"""потребление"""
			print('consumption')
			weekconsumption += 1
			
			"""здесь может появиться ошибка потребления чего-либо, поскольку потреблять могут "копии" """
			
			settl_copy = settlement.Settlement.slovar.copy()
			for i in settl_copy:
				for j in settlement.Settlement.slovar[i].factories:
					if j.num_workers != 0:
						factory.Factory.consume_food(j)
				for j in settlement.Settlement.slovar[i].pops:
					if j.num != 0:
						pops.Pops.consume_food(settlement.Settlement.slovar[i].pops[j])
						pops.Pops.emigration(j, j.location.state, mm,grain)

		if (xt-95)//100 - weekcorrections > 0:
			"""корректировка населения. смерть-рождение"""
			print('corrections')
			weekcorrections += 1
			# rivers.River.count_attractiveness(1, grainMap, mm)
			for i in settlement.Settlement.slovar:
				iter_for_pops = list(settlement.Settlement.slovar[i].pops) # этот лист ввёл ибо удаляются пустые попы в процессе
				for j in iter_for_pops:
					if not settlement.Settlement.slovar[i].pops[j].unemployed:
						pops.Pops.popchange(settlement.Settlement.slovar[i].pops[j])

						if settlement.Settlement.slovar[i].pops[j].total_num == 0:                            # удаляем пустые попы. чтоб память не жрали
							settlement.Settlement.slovar[i].pops[j].location.state.money += settlement.Settlement.slovar[i].pops[j].money           # перемещаем их деньги и инвентарь в казну
							for key in settlement.Settlement.slovar[i].pops[j].inventory:                     # а удалять у самих попов смысла нет - удаляем поп полностью
								if key in settlement.Settlement.slovar[i].pops[j].location.state.inventory:
									settlement.Settlement.slovar[i].pops[j].location.state.inventory[key] += settlement.Settlement.slovar[i].pops[j].inventory[key]
								else:
									settlement.Settlement.slovar[i].pops[j].location.state.inventory[key] = settlement.Settlement.slovar[i].pops[j].inventory[key]
							del settlement.Settlement.slovar[i].pops[j]
				iter_for_pops = list(settlement.Settlement.slovar[i].pops)
				for j in iter_for_pops:
					if settlement.Settlement.slovar[i].pops[j].unemployed:
						pops.Pops.popchange(settlement.Settlement.slovar[i].pops[j])

						if settlement.Settlement.slovar[i].pops[j].total_num == 0:  # удаляем пустые попы. чтоб память не жрали
							settlement.Settlement.slovar[i].pops[j].location.state.money += settlement.Settlement.slovar[i].pops[
								j].money  # перемещаем их деньги и инвентарь в казну
							for key in settlement.Settlement.slovar[i].pops[
								j].inventory:  # а удалять у самих попов смысла нет - удаляем поп полностью
								if key in settlement.Settlement.slovar[i].pops[j].location.state.inventory:
									settlement.Settlement.slovar[i].pops[j].location.state.inventory[key] += \
									settlement.Settlement.slovar[i].pops[j].inventory[key]
								else:
									settlement.Settlement.slovar[i].pops[j].location.state.inventory[key] = \
									settlement.Settlement.slovar[i].pops[j].inventory[key]
							del settlement.Settlement.slovar[i].pops[j]
				settlement.Settlement.stlpopul(settlement.Settlement.slovar[i])
				settlement.Settlement.city_growth(settlement.Settlement.slovar[i],mm,background,grainMap)
			sui = 0
			for i in settlement.Settlement.slovar:
				for j in settlement.Settlement.slovar[i].pops:
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
					# risov(xe, xg, ye, yg, rasst, pribl, DlinaX,DlinaY, mm, bg)
					draw(xe, xg, ye, yg, rasst, pribl, Dlina, mm, bg)
				elif mapmode == 1:
					# risov(xe, xg, ye, yg, rasst, pribl, DlinaX,DlinaY, mm, bg)
					# politrisov(xe,xg,ye,yg,rasst,pribl,DlinaX,DlinaY,pm,pbg)
					draw(xe, xg, ye, yg, rasst, pribl, Dlina, mm, bg)
					politrisov(xe, xg, ye, yg, rasst, pribl, Dlina, politicalMap, pbg)
				elif mapmode == 2:
					# risov(xe, xg, ye, yg, rasst, pribl, DlinaX,DlinaY, imm, bg)
					draw(xe, xg, ye, yg, rasst, pribl, Dlina, imm, bg)
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
				
				
		if xt == oneday:

			if currentweekday == 7:
				currentweekday = 1
				
			else:
				currentweekday += 1
			
			
			if currentday == 30:
				currentday = 1
				if currentmonth == 12:
					currentmonth = 1
					currentyear += 1
				else:
					currentmonth += 1
			else:
				currentday += 1
			xt = 0
		
		for st in state.State.statedict:
			"""запихнуть 7 массивов в 1 - ГОТОВО"""
			not_all_factories_used = True
			not_all_pops_fed = True
			not_all_settl_calculated = True
			fact_counter_100 = 0
			pop_counter_100 = 0
			settl_counter_100 = 0
			while not_all_factories_used:
				if (len(st.factories[currentweekday-1]) - 1) >= xt+fact_counter_100*oneday :
					short_factory = st.factories[currentweekday - 1][xt + fact_counter_100 * oneday]
					factory.Factory.factbuy(short_factory)  # завод покупает нужные ресурсы
					factory.Factory.factboostbuy(short_factory)  # и бустеры (типа удобрения для С/Х)
					factory.Factory.popbuy(short_factory)  # и жратву своим рабочим и тд
					factory.Factory.create(short_factory, grainMap)
					
					factory.Factory.pricechange(short_factory)
					
					if short_factory.type:           # отдаю деньги и жратву крестьянам.
						factory.Factory.givefoodmoney(short_factory)
						# factory.Factory.wage_change(short_factory)        почему-то изначально этот метод стоял под таким if
					factory.Factory.wage_change(short_factory)
					if short_factory.num_workers != 0:
						factory.Factory.consume_food(short_factory)
					
					fact_counter_100 += 1
				else:
					not_all_factories_used = False
			
			
			while not_all_pops_fed:
				if (len(st.pops_for_opt[currentweekday - 1]) - 1) >= xt + pop_counter_100 * oneday:
					short_pop = st.pops_for_opt[currentweekday - 1][xt + pop_counter_100 * oneday]
					pops.Pops.popbuy(short_pop)  # покупают жрачку и т.д.
					pops.Pops.consume_food(short_pop)
					pops.Pops.emigration(short_pop, st, mm, grain)

					
					
					pop_counter_100 += 1
				else:
					not_all_pops_fed = False
					
			"""
			ПРОБЛЕМА С ПРОИЗВОДИТЕЛЬНОСТЬЮ ПРИ ИЗМЕНЕНИИ ЧИСЛЕННОСТИ НАСЕЛЕНИЯ МОЖЕТ БЫТЬ СВЯЗАНА С МЕТОДОМ CITY_GROWTH
			И РОСТОМ ГОРОДОВ/ПАШЕН, А НЕ С ПЕРЕСЧЁТОМ НАСЕЛЕНИЯ
			"""
			
			"""
			по идее здесь закладываются многие "неточности", например коэффициенты для заводов и нормировка в целом
			будут рассчитываться в разные моменты времени и не всегда будут согласовываться
			(скорее всего сейчас уберу этот пиздец. да, убираю уже)
			"""
			
			while not_all_settl_calculated:
				if (len(st.settlements_for_opt[currentweekday - 1]) - 1) >= xt + settl_counter_100 * oneday:
					short_settl = st.settlements_for_opt[currentweekday - 1][xt + settl_counter_100 * oneday]
					settlement.Settlement.if_not_full(short_settl)
					settlement.Settlement.summakubow(short_settl)  # считаем нормировку для коэффициентов распределения попов по заводам
					for pop_in_city_counter in short_settl.pops:  # для каждого попа в этом городе
						pops.Pops.facsearch(pop_in_city_counter)  # непосредственно распределяем население попа в соответствии с коэффициентами
					settlement.Settlement.stlpopul(short_settl)
					settlement.Settlement.city_growth(short_settl, mm, background, grainMap)
					settl_counter_100 += 1
				else:
					not_all_settl_calculated = False
					
			not_all_pops_bred = True
			pop_counter_3000 = 0
			while not_all_pops_bred:
				if (len(st.pops_for_breeding) - 1) >= xt + pop_counter_3000 * onemonth:
					short_pop_bred = st.pops_for_breeding[xt + pop_counter_3000 * onemonth]
					pops.Pops.popchange(short_pop_bred)
					if short_pop_bred.total_num == 0:  # удаляем пустые попы. чтоб память не жрали
						short_pop_bred.location.state.money += short_pop_bred.money  # перемещаем их деньги и инвентарь в казну
						for key in short_pop_bred.inventory:  # а удалять у самих попов смысла нет - удаляем поп полностью
							if key in short_pop_bred.location.state.inventory:
								short_pop_bred.location.state.inventory[key] += short_pop_bred.inventory[key]
							else:
								short_pop_bred.location.state.inventory[key] = short_pop_bred.inventory[key]
						del short_pop_bred
						"""
						НУЖНО ЛИ УДАЛЯТЬ ПОП ИЗ ВСЕХ СЛОВАРЕЙ И СПИСКОВ?
						"""
				
					
				else:
					not_all_pops_bred = False
				
				
		
		day_week_month_year = str(currentday) + ' ' + months[currentmonth-1] + ' ' + str(currentyear) + 'г.'
		dweek = weekdays[currentweekday-1]
		text1 = f1.render(day_week_month_year, 0, (0, 0, 0))  # кнопочки и другой текст
		but_time.fill((100, 100, 20))
		pg.draw.rect(but_time, (0, 0, 0), (0, 0, 150, 30), 2)
		but_time.blit(text1, (10, 4))
		text1 = f1.render(dweek, 0, (0, 0, 0))
		but_time.blit(text1, (10, 16))
		UI_window.blit(but_time,(0,0))
		sc.blit(UI_window,(0,0))


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
						pwo_w_money,pwo_eff_list1 = pops.Pops.countmoney(pwo_pop)
						pwo_eff_list = {}
						for j in pwo_eff_list1:
							pwo_eff_list[j] = f1.render(j.good.name + ' ЗП/Запасы: ' + str(j.gehalt) + '/' + str(pwo_eff_list1[j]), 0, (0, 0, 0))
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
			text_city = f1.render('Население: ' + str(settlement_to_show.population),0,(0,0,0))
			sc.blit(text_city, (200, 60))
			text_city = f1.render('Заводы:',0,(0,0,0))
			sc.blit(text_city,(60,100))

			# сделать тут кнопку, чтоб показывать детали про попы: численность, инвентарь, деньги, безработица
			# то же самое сделать с заводами: число рабочих, инвентарь, деньги, основные поставщики, динамика цен, динамика другого
			# запрогать хотя бы минимально государства
			# уже не здесь, но в целом сделать окно с общей информацией по всем городам ГОСУДАРСТВА, а в ней уже сделать кнопку для
			# каждого отдельного города (в ЭТО окно)

			fic_cnt = 0
			for j in factories_in_city:
				text_city = f1.render(factories_in_city[j][0] + ' Рабочие: ' + str(factories_in_city[j][1])+'/'+
																				   str(factories_in_city[j][2])+
									  ' Деньги: '+str(factories_in_city[j][3])+ ' Деньги рабочих: '+ str(factories_in_city[j][4])+
									  ' Зарплаты: '+str(factories_in_city[j][5]),0,(0,0,0))
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

			text_city = f1.render(pwo_pop.strata.name + ' ' + pwo_pop.culture.name + ' ' +  pwo_pop.religion.name, 0, (0, 0, 0))
			# сделать пересчёт всех заводов, чтобы видеть, сколько денег имеет именно этот поп
			info_window.blit(text_city, (10, 10))
			
			text_city = f1.render('Население: ' + str(pwo_pop.total_num) + ' Рабочее население: ' + str(pwo_pop.num) , 0, (0, 0, 0))
			info_window.blit(text_city, (10, 50))

			text_city = f1.render('Деньги: ' + str(pwo_w_money) + ' Деньги безработных: ' + str(pwo_pop.money), 0,
								  (0, 0, 0))
			info_window.blit(text_city, (10, 30))
			
			text_city = f1.render('Потребляют: ', 0, (0, 0, 0))
			info_window.blit(text_city, (190, 10))


			"""info_window рисование непосредственно на самом info_window"""


			i123 = 0
			for i in pop_cons:
				info_window.blit(pop_cons[i],(270+i123*100, 10))
				i123 += 1

			i123 = 0
			for i in pwo_eff_list:
				info_window.blit(pwo_eff_list[i], (270, 70+i123*20))
				i123 += 1

			sc.blit(info_window, (50, 50))


			if pressed[0] and not pg.Rect.collidepoint(infowind_rect,pos[0],pos[1]):
				pop_window_opened = False



		elif fact_window_opened:
			info_window.fill((190, 210, 40))
			


			text_city = f1.render(fwo_fact.good.name + ' Рабочие: ' + str(fwo_fact.num_workers) + '/' +
								  str(fwo_fact.fullnum) +
								  ' Деньги: ' + str(fwo_fact.money) + ' Деньги Рабочих: ' + str(
				fwo_fact.workers_money) +
								  ' Зарплаты: ' + str(fwo_fact.gehalt), 0, (0, 0, 0))
			info_window.blit(text_city, (60, 50))


			i123 = 0
			for i in fact_pop_cons:
				info_window.blit(fact_pop_cons[i], (60 + i123 * 200, 70))
				i123 += 1

			pg.draw.line(info_window, (0, 0, 0), (60 , 80),
						 (60, 310), 2)
			pg.draw.line(info_window, (0, 0, 0), (60, 300),
						 (300, 300), 2)
			
			for ij in range(len(fwo_fact.prices_history)-1):
				pg.draw.line(info_window, (200, 0, 0), (60 + ij*10, 300-int(fwo_fact.prices_history[ij]*200)),
							 (60+(ij+1)*10, 300-int(fwo_fact.prices_history[ij+1]*200)), 2)
				price_text = f1.render(str(round(fwo_fact.prices_history[ij+1],2)), 0, (0, 0, 0))
				info_window.blit(price_text,(60+(ij+1)*10, 300-int(fwo_fact.prices_history[ij+1]*200)-20))
			sc.blit(info_window, (50, 50))

			if pressed[0] and not pg.Rect.collidepoint(infowind_rect,pos[0],pos[1]):
				fact_window_opened = False

		elif trade_window_opened:
			info_window.fill((190, 210, 40))

			sc.blit(info_window, (50, 50))

			if pressed[0] and not pg.Rect.collidepoint(infowind_rect, pos[0], pos[1]):
				trade_window_opened = False
		
		# тут надо поменять местами условие клика и условие наведения на поселение. нужно проверять второе при условии, что есть первое
		# или пока нет. там есть код на указание информации о городе при наведении, и там нужно каждый раз проверять всё
		q1 = 0
		for q in settlement.Settlement.slovar:
			if pg.Rect.collidepoint(settlement.Settlement.arry[q1][0],(pos[0]-xe,pos[1]-ye)):
				if pressed[0]:
					city_window_opened = True
					settlement_to_show = settlement.Settlement.slovar[q]
					factories_in_city = {}
					factories_button = {}
					counter = 0
					for j in settlement.Settlement.slovar[q].factories:
						factories_in_city[j] = (j.good.name,j.num_workers,j.fullnum, j.money, j.workers_money, j.gehalt, j.inventory, j.sell)
						factories_button[j] = pg.Rect(160, 100 + 20 * counter, 100, 20)
						counter+=1


					pops_in_city = settlement.Settlement.slovar[q].pops.copy()
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


		pg.time.delay(delay)
		if not pause:
			xt += 1                                          # счётчик времени


if __name__ == "__main__":
	main()
