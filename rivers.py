class River:
    Settl_number = 0   # количество поселений в мире
    arry = []           # список с прямоугольниками городов. чтоб можно было на них наводить и нажимать на карте
    slovar = dict()            # словарь всех рек мира
    places = {}


    def __init__(self,mm, name,start,direction,rivlist):
        self.rivlist = rivlist
        self.start = start
        self.direction = direction  # 1 - Север, 2 - Восток, 3 - Юг, 4 - Запад (1 - право, -1 - лево)

        River.slovar[self] = self



    def draw_river(self):
        for i in range(len(self.rivlist)):
            print("лучше потом подумать, как мерить расстояние, ибо сейчас лень с этим ебстись")

    def count_places(self,mm):
        for i in range(len(mm)):
            for j in range(len(mm)):
                if mm[i,j] == 1:
                    if mm[i - 1, j] == 0:
                        if (i - 1, j) not in River.places:
                            River.places[(i,j)] = 0
                            continue

                    if mm[i + 1, j] == 0:
                        if (i + 1, j) not in River.places:
                            River.places[(i, j)] = 0
                            continue
                    if mm[i, j - 1] == 0:
                        if (i, j - 1) not in River.places:
                            River.places[(i, j)] = 0
                            continue

                    if mm[i, j + 1] == 0:
                        if (i, j + 1) not in River.places:
                            River.places[(i, j)] = 0
                            continue


    def count_attractiveness(self,gm):
        dist = 10
        for coord in River.places:
            resour = 0
            for i in range(dist):
                for j in range(dist):
                    resour += gm[coord[0]+i-dist//2,coord[1]+j-dist//2]
            River.places[coord] = resour







