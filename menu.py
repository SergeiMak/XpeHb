import pygame as pg

def chosen(which_but):
	print(which_but)


def main():
	pg.init()
	Dlina = 600
	
	scmenu = pg.display.set_mode((Dlina, Dlina))
	# background_menu = pg.Surface((Dlmatr, Dlmatr))
	# background_menu.fill((0, 0, 150))
	
	menuwindow = pg.Surface(
		(Dlina, Dlina))  # инициализируем информационное окно (появл. при нажатии на город)
	menuwindow.fill((190, 210, 40))
	menuwindow_rect = menuwindow.get_rect(topleft=(50, 50))
	
	buttons_h = 200
	buttons_v = 50
	buttons_dict = {}
	
	but_start_new = pg.Surface((buttons_h, buttons_v))  # кнопка для политической карты
	but_load = pg.Surface((buttons_h, buttons_v))  # для ресурсной
	but_exit = pg.Surface((buttons_h, buttons_v))  # для показателя времени
	but_options = pg.Surface((buttons_h, buttons_v))
	
	buttons_dict[but_start_new.get_rect(topleft=(50, 50))] = 'but_start_new'
	buttons_dict[but_load.get_rect(topleft=(50, 50))] = 'but_load'
	buttons_dict[but_exit.get_rect(topleft=(50, 50))] = 'but_exit'
	buttons_dict[but_options.get_rect(topleft=(50, 50))] = 'but_options'
	
	
	but_start_new.fill((100, 100, 20))
	but_load.fill((100, 100, 20))
	but_exit.fill((100, 100, 20))
	but_options.fill((100, 100, 20))
	
	# обрамление кнопок чёрными границами
	# pg.draw.rect(but_polit, (0, 0, 0), (0, 0, 100, 30), 2)
	# pg.draw.rect(but_resource, (0, 0, 0), (0, 0, 100, 30), 2)
	# pg.draw.rect(but_time, (0, 0, 0), (0, 0, 150, 30), 2)
	# pg.draw.rect(but_trade, (0, 0, 0), (0, 0, 100, 30), 2)
	
	f1 = pg.font.Font(None, 20)
	
	text1 = f1.render('Сгенерировать новую карту', 0, (0, 0, 0))  # кнопочки и другой текст
	but_start_new.blit(text1, (20, 5))
	text2 = f1.render('Загрузить', 0, (0, 0, 0))
	but_load.blit(text2, (20, 5))
	text3 = f1.render('Выйти', 0, (0, 0, 0))
	but_exit.blit(text3, (20, 5))
	text4 = f1.render('Настройки', 0, (0, 0, 0))
	but_options.blit(text4, (10, 5))
	menuwindow.blit(but_start_new, (150, 100))
	menuwindow.blit(but_load, (250, 100))
	menuwindow.blit(but_options, (350, 100))
	menuwindow.blit(but_exit, (450, 100))
	
	
	scmenu.blit(menuwindow, (0, 0))
	
	pg.display.update()
	
	while 1:
	
	
		
		keys = pg.key.get_pressed()
		pressed = pg.mouse.get_pressed()
		pos = pg.mouse.get_pos()
		if pressed[0]:
			xa, ya = pos
		for but in buttons_dict:
			if pg.Rect.collidepoint(but, pos):
				chosen(buttons_dict[but])
		
		pg.time.delay(delay = 10)
		pg.display.update()


if __name__ == "__main__":
    main()