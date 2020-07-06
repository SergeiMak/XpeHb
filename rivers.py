class River:
    Settl_number = 0   # количество поселений в мире
    arry = []           # список с прямоугольниками городов. чтоб можно было на них наводить и нажимать на карте
    slovar = dict()            # словарь всех рек мира
    places = {}


    def __init__(self,mm, name,start,direction,rivlist):
        self.rivlist = rivlist
        self.start = start
        self.direction = direction  # -1 - Север, 2 - Восток, 1 - Юг, -2 - Запад (1 - право, -1 - лево)

        River.slovar[self] = self
        River.initialise_river(self,mm)


    def initialise_river(self,mm):
        ko1 = int(((1-self.direction)*(1 + self.direction)/(-3))*(self.direction/abs(self.direction)))
        ko2 = int((((2 - self.direction) * (2 + self.direction) / (3)) * (self.direction / abs(self.direction))))
        #print(ko1,ko2)
        mm[self.start[0]:self.start[0]+ko1*self.rivlist+ko2,self.start[1]:self.start[1]+ko2*self.rivlist+ko1] = 0
        #print(self.start[0],self.start[0]+ko1*self.rivlist,self.start[1],self.start[1]+ko2*self.rivlist)

        
    def cycle_river(self,objekt,start):
        for i1 in objekt:
            if isinstance(i1, list):
                River.cycle_river(self,i1)
            else:
                znak = i1/abs(i1)
                for j1 in range(abs(i1)):
                    print()
                
                

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
        


    def count_attractiveness(self,gm,mm):
        dist = 10
        for coord in River.places:
            mult = 1
            resour = 0
            for i in range(dist):
                for j in range(dist):
                    resour += gm[coord[0]+i-dist//2,coord[1]+j-dist//2]
                    if mm[coord[0]+i-dist//2,coord[1]+j-dist//2] == 5:
                        mult = 0
                    
            River.places[coord] = resour*mult
        print(River.places)







