import pygame as pg
from random import choice
from random import randint
import numpy as np

def generateforest(forestMap,mm,background,point,size):
    """
    принцип генерации прост. берём изначальную точку point, смотрим на её соседние точки, проверяем, не использовали ли
    мы их прежде. если нет, то смотрим рядом со случайной соседней точкой точки, которые мы уже брали и где есть занчение
    на одной из карт (grainMap, forestMap и подобное). Если такие есть, то ограничиваем случайную генерацию ресурса
    
    :param forestMap:
    :param mm:
    :param background:
    :param point:
    :param size:
    :return:
    """
    
    
    if mm[point[0],point[1]] != 1:
        for i in range(len(mm)):
            for j in range(len(mm)):
                if mm[i,j] == 1:
                    point = (i,j)
    forest_list = [point]
    forest_deleted = []
    for i in range(size):
        ch = choice(forest_list)
        #mm[ch[0],ch[1]] = 3
        
        if mm[ch[0]+1,ch[1]] == 1 and (ch[0]+1,ch[1]) not in forest_list:
            forest_list.append((ch[0]+1,ch[1]))
        if mm[ch[0]-1,ch[1]] == 1 and (ch[0]-1,ch[1]) not in forest_list:
            forest_list.append((ch[0]-1,ch[1]))
        if mm[ch[0],ch[1]+1] == 1 and (ch[0],ch[1]+1) not in forest_list:
            forest_list.append((ch[0],ch[1]+1))
        if mm[ch[0],ch[1]-1] == 1 and (ch[0],ch[1]-1) not in forest_list:
            forest_list.append((ch[0],ch[1]-1))
        forest_deleted.append(ch)

        f1 = 0
        f2 = 0
        f3 = 0
        f4 = 0
        tot = 0
        if (ch[0] + 1, ch[1]) in forest_deleted:
            f1 = forestMap[(ch[0] + 1, ch[1])]
            tot += 1
            if (ch[0] + 1, ch[1]) in forest_list:
                index1 = forest_list.index((ch[0] + 1, ch[1]))
                del forest_list[index1]
        if (ch[0] - 1, ch[1]) in forest_deleted:
            f2 = forestMap[(ch[0] - 1, ch[1])]
            tot += 1
            if (ch[0] - 1, ch[1]) in forest_list:
                index1 = forest_list.index((ch[0] - 1, ch[1]))
                del forest_list[index1]
        if (ch[0], ch[1] + 1) in forest_deleted:
            f3 = forestMap[(ch[0], ch[1] + 1)]
            tot += 1
            if (ch[0], ch[1] + 1) in forest_list:
                index1 = forest_list.index((ch[0], ch[1] + 1))
                del forest_list[index1]
        if (ch[0], ch[1] - 1) in forest_deleted:
            f4 = forestMap[(ch[0], ch[1] - 1)]
            tot += 1
            if (ch[0], ch[1] - 1) in forest_list:
                index1 = forest_list.index((ch[0], ch[1] - 1))
                del forest_list[index1]
        
        if len(forest_list) == 5:
            tot = 1
            f1 = 99
            f2 = 0
            f3 = 0
            f4 = 0
            
        # print(forest_list, forest_deleted, tot, f1, f2, f3, f4)
        # print(ch)
        if tot == 0:
            break
        average = (f1+f2+f3+f4)//tot
        if average <= 20:
            rand0 = 0
        else:
            rand0 = average - 20
        if average >= 80:
            rand100 = 100
        else:
            rand100 = average + 20
        quality = np.random.randint(rand0, rand100)
        forestMap[ch[0],ch[1]] = quality
        background.set_at(ch, (0, int(90 - (quality*50)//100), 0))
        index1 = forest_list.index(ch)
        
        del forest_list[index1]

        if not forest_list:
            break
        
        """
        НАДО ЕЩЁ ТОГДА СДЕЛАТЬ КОЭФФИЦИЕНТЫ КЛЕТКАМ ПАШЕН ПО ПРОЦЕНТУ ЛЕСНОГО ПОКРОВА ПРИ ПРОИЗВОДСТВЕ ПШЕНИЦЫ
        """
        
def generateriver1(mm,background,point,size):
    river_list = []
    pikes = [point]
    for i in range(size):
        river_list = []
        for pike in pikes:
            
            if mm[pike[0] + 1, pike[1]] != 0 and mm[pike[0] + 2, pike[1]] != 0 and mm[pike[0] + 1, pike[1]+1] != 0 and mm[pike[0] + 1, pike[1]-1] != 0:
                river_list.append((pike[0] + 1, pike[1]))
            if mm[pike[0] - 1, pike[1]] != 0 and  mm[pike[0] - 2, pike[1]] != 0 and  mm[pike[0] - 1, pike[1]+1] != 0 and  mm[pike[0] - 1, pike[1] - 1] != 0:
                river_list.append((pike[0] - 1, pike[1]))
            if mm[pike[0], pike[1] + 1] != 0 and mm[pike[0], pike[1] + 2] != 0 and mm[pike[0]+1, pike[1] + 1] != 0 and mm[pike[0]-1, pike[1] + 1] != 0:
                river_list.append((pike[0], pike[1] + 1))
            if mm[pike[0], pike[1] - 1] != 0 and mm[pike[0], pike[1] - 2] != 0 and mm[pike[0]+1, pike[1] - 1] != 0 and mm[pike[0]-1, pike[1] - 1] != 0:
                river_list.append((pike[0], pike[1] - 1))
            
            """
            if mm[pike[0] + 1, pike[1]] != 0:
                river_list.append((pike[0] + 1, pike[1]))
            if mm[pike[0] - 1, pike[1]] != 0:
                river_list.append((pike[0] - 1, pike[1]))
            if mm[pike[0], pike[1] + 1] != 0:
                river_list.append((pike[0], pike[1] + 1))
            if mm[pike[0], pike[1] - 1] != 0:
                river_list.append((pike[0], pike[1] - 1))
            """

            # if mm[ch[0] + 1, ch[1]] != 0:
            #     river_list.append((ch[0] + 1, ch[1]))
            # if mm[ch[0] - 1, ch[1]] != 0:
            #     river_list.append((ch[0] - 1, ch[1]))
            # if mm[ch[0], ch[1] + 1] != 0:
            #     river_list.append((ch[0], ch[1] + 1))
            # if mm[ch[0], ch[1] - 1] != 0:
            #     river_list.append((ch[0], ch[1] - 1))
            # river_deleted.append(ch)
        if not river_list:
            break
        ch = choice(river_list)
        mm[ch[0],ch[1]] = 0
        pikes.append(ch)
        print(randint(1,20))
        if randint(1,20) > 18:
            index1 = river_list.index(ch)
            del river_list[index1]
            if not river_list:
                break
            ch1 = choice(river_list)
            mm[ch[0], ch[1]] = 0
            pikes.append(ch)
            background.set_at(ch1, (50, 50, 200))
        if (ch[0] + 1, ch[1]) in pikes:
            index1 = pikes.index((ch[0] + 1, ch[1]))
            del pikes[index1]
        if (ch[0] - 1, ch[1]) in pikes:

            index1 = pikes.index((ch[0] - 1, ch[1]))
            del pikes[index1]
        if (ch[0], ch[1] + 1) in pikes:

            index1 = pikes.index((ch[0], ch[1] + 1))
            del pikes[index1]
        if (ch[0], ch[1] - 1) in pikes:

            index1 = pikes.index((ch[0], ch[1] - 1))
            del pikes[index1]
    

        background.set_at(ch, (50, 50, 200))


def generateriver2(mm, background, point, size, directionup,directiondown, directionleft,directionright):
    river_list = []
    if mm[point[0],point[1]] != 1:
        for i in range(len(mm)):
            for j in range(len(mm)):
                if mm[i,j] == 1:
                    point = (i,j)

    pikes = [point]
    for i in range(size):
        river_list = []
        for pike in pikes:
            
            if mm[pike[0] + 1, pike[1]] != 0 and mm[pike[0] + 2, pike[1]] != 0 and mm[pike[0] + 1, pike[1] + 1] != 0 and \
                    mm[pike[0] + 1, pike[1] - 1] != 0:
                river_list.append((pike[0] + 1, pike[1]))
                if directionright:
                    river_list.append((pike[0] + 1, pike[1]))
            if mm[pike[0] - 1, pike[1]] != 0 and mm[pike[0] - 2, pike[1]] != 0 and mm[pike[0] - 1, pike[1] + 1] != 0 and \
                    mm[pike[0] - 1, pike[1] - 1] != 0:
                river_list.append((pike[0] - 1, pike[1]))
                if directionleft:
                    river_list.append((pike[0] - 1, pike[1]))
            if mm[pike[0], pike[1] + 1] != 0 and mm[pike[0], pike[1] + 2] != 0 and mm[pike[0] + 1, pike[1] + 1] != 0 and \
                    mm[pike[0] - 1, pike[1] + 1] != 0:
                river_list.append((pike[0], pike[1] + 1))
                if directiondown:
                    river_list.append((pike[0], pike[1] + 1))
            if mm[pike[0], pike[1] - 1] != 0 and mm[pike[0], pike[1] - 2] != 0 and mm[pike[0] + 1, pike[1] - 1] != 0 and \
                    mm[pike[0] - 1, pike[1] - 1] != 0:
                river_list.append((pike[0], pike[1] - 1))
                if directionup:
                    river_list.append((pike[0], pike[1] - 1))
            
            """
            if mm[pike[0] + 1, pike[1]] != 0:
                river_list.append((pike[0] + 1, pike[1]))
            if mm[pike[0] - 1, pike[1]] != 0:
                river_list.append((pike[0] - 1, pike[1]))
            if mm[pike[0], pike[1] + 1] != 0:
                river_list.append((pike[0], pike[1] + 1))
            if mm[pike[0], pike[1] - 1] != 0:
                river_list.append((pike[0], pike[1] - 1))
            """
            
            # if mm[ch[0] + 1, ch[1]] != 0:
            #     river_list.append((ch[0] + 1, ch[1]))
            # if mm[ch[0] - 1, ch[1]] != 0:
            #     river_list.append((ch[0] - 1, ch[1]))
            # if mm[ch[0], ch[1] + 1] != 0:
            #     river_list.append((ch[0], ch[1] + 1))
            # if mm[ch[0], ch[1] - 1] != 0:
            #     river_list.append((ch[0], ch[1] - 1))
            # river_deleted.append(ch)
        if not river_list:
            break
        ch = choice(river_list)
        mm[ch[0], ch[1]] = 0
        pikes.append(ch)
        print(randint(1, 20))
        if randint(1, 20) > 18:
            index1 = river_list.index(ch)
            del river_list[index1]
            if not river_list:
                break
            ch1 = choice(river_list)
            mm[ch[0], ch[1]] = 0
            pikes.append(ch)
            background.set_at(ch1, (50, 50, 200))
        if (ch[0] + 1, ch[1]) in pikes:
            index1 = pikes.index((ch[0] + 1, ch[1]))
            del pikes[index1]
        if (ch[0] - 1, ch[1]) in pikes:
            index1 = pikes.index((ch[0] - 1, ch[1]))
            del pikes[index1]
        if (ch[0], ch[1] + 1) in pikes:
            index1 = pikes.index((ch[0], ch[1] + 1))
            del pikes[index1]
        if (ch[0], ch[1] - 1) in pikes:
            index1 = pikes.index((ch[0], ch[1] - 1))
            del pikes[index1]
        
        background.set_at(ch, (50, 50, 200))
    mm[point[0], point[1]] = 0
    background.set_at(point, (50, 50, 200))

def generateland(land_list, grainMap, mm, point, size, directionup,directiondown, directionleft,directionright):

    land_list = [point]
    land_deleted = []
    for i in range(size):
        ch = choice(land_list)
        mm[ch[0],ch[1]] = 1
        
        if mm[ch[0] + 1, ch[1]] == 0 and (ch[0] + 1, ch[1]) not in land_list:
            land_list.append((ch[0] + 1, ch[1]))
            if directionright:
                for k in range(2):
                    land_list.append((ch[0] + 1, ch[1]))
        if mm[ch[0] - 1, ch[1]] == 0 and (ch[0] - 1, ch[1]) not in land_list:
            land_list.append((ch[0] - 1, ch[1]))
            if directionleft:
                for k in range(2):
                    land_list.append((ch[0] - 1, ch[1]))
        if mm[ch[0], ch[1] + 1] == 0 and (ch[0], ch[1] + 1) not in land_list:
            land_list.append((ch[0], ch[1] + 1))
            if directiondown:
                for k in range(2):
                    land_list.append((ch[0], ch[1] + 1))
        if mm[ch[0], ch[1] - 1] == 0 and (ch[0], ch[1] - 1) not in land_list:
            land_list.append((ch[0], ch[1] - 1))
            if directionup:
                for k in range(2):
                    land_list.append((ch[0], ch[1] - 1))
        land_deleted.append(ch)
        
        f1 = 0
        f2 = 0
        f3 = 0
        f4 = 0
        tot = 0
        if (ch[0] + 1, ch[1]) in land_deleted:
            f1 = grainMap[(ch[0] + 1, ch[1])]
            tot += 1
            for d in range(1):
                while (ch[0] + 1, ch[1]) in land_list:
                    index1 = land_list.index((ch[0] + 1, ch[1]))
                    del land_list[index1]
        if (ch[0] - 1, ch[1]) in land_deleted:
            f2 = grainMap[(ch[0] - 1, ch[1])]
            tot += 1
            for d in range(1):
                while (ch[0] - 1, ch[1]) in land_list:
                    index1 = land_list.index((ch[0] - 1, ch[1]))
                    del land_list[index1]
        if (ch[0], ch[1] + 1) in land_deleted:
            f3 = grainMap[(ch[0], ch[1] + 1)]
            tot += 1
            for d in range(1):
                while (ch[0], ch[1] + 1) in land_list:
                    index1 = land_list.index((ch[0], ch[1] + 1))
                    del land_list[index1]
        if (ch[0], ch[1] - 1) in land_deleted:
            f4 = grainMap[(ch[0], ch[1] - 1)]
            tot += 1
            for d in range(1):
                while (ch[0], ch[1] - 1) in land_list:
                    index1 = land_list.index((ch[0], ch[1] - 1))
                    del land_list[index1]
        
        if i == 0:
            tot = 1
            f1 = 99
            f2 = 0
            f3 = 0
            f4 = 0
            print(land_list)
        # print(tot,f1,f2,f3,f4)
        if tot == 0 or tot > 4:
            print(tot, f1,f2,f3,f4,i)
            print(land_list)
        average = (f1 + f2 + f3 + f4) // tot
        # print(average)
        if average <= 20:
            rand0 = 0
        else:
            rand0 = average - 20
        if average >= 80:
            rand100 = 100
        else:
            rand100 = average + 20
        quality = np.random.randint(rand0, rand100)
        grainMap[ch[0], ch[1]] = quality
        # background.set_at(ch, (0, int(90 - (quality * 50) // 100), 0))
        index1 = land_list.index(ch)
        
        del land_list[index1]
    # rand_border1 = choice(land_list)
    # rand_border2 = rand_border1.copy()
    # for i in land_list:
    #     if i[0] < rand_border1[0]:
    #         rand_border1[0] = i[0]
    #     if i[1] < rand_border1[1]:
    #         rand_border1[1] = i[1]
    #
    #     if i[0] > rand_border2[0]:
    #         rand_border2[0] = i[0]
    #     if i[1] > rand_border2[1]:
    #         rand_border2[1] = i[1]
    
    # for i in range(rand_border1[0],rand_border2[0]):
    #     for j in range(rand_border1[1],rand_border2[1]):
    #         if mm[i,j] == 0:
    lan_del = land_deleted.copy()
    for i in lan_del:
        if (i[0] + 1, i[1]) not in land_deleted and mm[i[0] + 1, i[1]] == 0:
            new_point1 = i[0] +1
            new_point2 = i[1]
            filling_gaps_in_land(new_point1,new_point2,land_deleted,mm,grainMap)
        if (i[0] - 1, i[1]) not in land_deleted:
            new_point1 = i[0] - 1
            new_point2 = i[1]
            filling_gaps_in_land(new_point1, new_point2, land_deleted, mm, grainMap)
        if (i[0], i[1] + 1) not in land_deleted:
            new_point1 = i[0]
            new_point2 = i[1] + 1
            filling_gaps_in_land(new_point1, new_point2, land_deleted, mm, grainMap)
        if (i[0], i[1] - 1) not in land_deleted:
            new_point1 = i[0]
            new_point2 = i[1] - 1
            filling_gaps_in_land(new_point1, new_point2, land_deleted, mm, grainMap)

def filling_gaps_in_land(new_point1,new_point2, land_deleted, mm, grainMap):
    if (new_point1 + 1, new_point2) in land_deleted and (new_point1 - 1, new_point2) in land_deleted and \
            (new_point1, new_point2 + 1) in land_deleted and (new_point1, new_point2 - 1) in land_deleted:
        mm[new_point1, new_point2] = 1
        average = (grainMap[new_point1 + 1, new_point2] + grainMap[new_point1 - 1, new_point2] + grainMap[
            new_point1, new_point2 + 1] + grainMap[new_point1, new_point2 - 1]) // 4
        # print(average)
        if average <= 20:
            rand0 = 0
        else:
            rand0 = average - 20
        if average >= 80:
            rand100 = 100
        else:
            rand100 = average + 20
        quality = np.random.randint(rand0, rand100)
        grainMap[new_point1, new_point2] = quality
        land_deleted.append((new_point1, new_point2))

def generateriver(mm, background, point, size, directionup, directiondown, directionleft, directionright):
    river_list = []
    # if mm[point[0], point[1]] != 1:
    #     for i in range(len(mm)):
    #         for j in range(len(mm)):
    #             if mm[i, j] == 1:
    #                 point = (i, j)
    
    pike = point
    mm[point[0], point[1]] = 0
    background.set_at(point, (50, 50, 200))
    for i in range(size):
        river_list = []
        print(pike)
        if mm[pike[0] + 1, pike[1]] != 0 and mm[pike[0] + 2, pike[1]] != 0 and mm[pike[0] + 1, pike[1] + 1] != 0 and \
                mm[pike[0] + 1, pike[1] - 1] != 0:
            river_list.append((pike[0] + 1, pike[1]))
            if directionright:
                for k in range(2):
                    river_list.append((pike[0] + 1, pike[1]))
        print(mm[pike[0] + 1, pike[1]] , mm[pike[0] + 2, pike[1]] , mm[pike[0] + 1, pike[1] + 1] ,
                mm[pike[0] + 1, pike[1] - 1])
        if mm[pike[0] - 1, pike[1]] != 0 and mm[pike[0] - 2, pike[1]] != 0 and mm[pike[0] - 1, pike[1] + 1] != 0 and \
                mm[pike[0] - 1, pike[1] - 1] != 0:
            river_list.append((pike[0] - 1, pike[1]))
            if directionleft:
                for k in range(2):
                    river_list.append((pike[0] - 1, pike[1]))
        print(mm[pike[0] - 1, pike[1]] , mm[pike[0] - 2, pike[1]] , mm[pike[0] - 1, pike[1] + 1] ,
                mm[pike[0] - 1, pike[1] - 1])
        if mm[pike[0], pike[1] + 1] != 0 and mm[pike[0], pike[1] + 2] != 0 and mm[pike[0] + 1, pike[1] + 1] != 0 and \
                mm[pike[0] - 1, pike[1] + 1] != 0:
            river_list.append((pike[0], pike[1] + 1))
            if directiondown:
                for k in range(2):
                    river_list.append((pike[0], pike[1] + 1))
        print(mm[pike[0], pike[1] + 1] , mm[pike[0], pike[1] + 2] , mm[pike[0] + 1, pike[1] + 1] ,
                mm[pike[0] - 1, pike[1] + 1])
        if mm[pike[0], pike[1] - 1] != 0 and mm[pike[0], pike[1] - 2] != 0 and mm[pike[0] + 1, pike[1] - 1] != 0 and \
                mm[pike[0] - 1, pike[1] - 1] != 0:
            river_list.append((pike[0], pike[1] - 1))
            if directionup:
                for k in range(2):
                    river_list.append((pike[0], pike[1] - 1))
        print(mm[pike[0], pike[1] - 1] , mm[pike[0], pike[1] - 2] , mm[pike[0] + 1, pike[1] - 1] ,
                mm[pike[0] - 1, pike[1] - 1])
        print(river_list)
        if not river_list:
            break
        ch = choice(river_list)
        mm[ch[0], ch[1]] = 0
        pike = ch
        print(pike)
        print(i)

        background.set_at(ch, (50, 50, 200))
        rand = randint(0,20)
        if rand > 18 and i != 0:
            if not river_list:
                break
            ch1 = choice(river_list)
            mm[ch1[0], ch1[1]] = 0
            pike = ch1
            background.set_at(ch1, (50, 50, 200))
            
            dup = choice((True,False))
            ddown = choice((True, False))
            dright = choice((True, False))
            dleft = choice((True, False))
            while dup == directionup and ddown == directiondown and dright == directionright and dleft == directionleft:
                dup = choice((True, False))
                ddown = choice((True, False))
                dright = choice((True, False))
                dleft = choice((True, False))
            print(ch1,size//2,size-i)
            generateriver(mm,background,ch1,size//2,dup,ddown,dleft,dright)
            generateriver(mm, background, ch1, size - i, directionup, directiondown, directionleft, directionright)

            break

