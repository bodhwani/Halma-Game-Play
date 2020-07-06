class Plate():


    PLATE_NONE = 0
    PLATE_WHITE = 1
    PLATE_BLACK = 2

    PIECE_NONE = 0
    PIECE_WHITE = 1
    PIECE_BLACK = 2
 
    O_NONE = 0
    O_SELECT = 1
    O_MOVED = 2

    def __init__(self, gotti=0, row=0, col=0):


        if((row == 0 or row == 1) and (col <5)):
            self.plate = 2
        elif (row>1 and row < 5 and row + col < 6):
            self.plate = 2
        elif (row == 15 or row == 14) and (col>10):
            self.plate = 1
        elif( row < 14 and row >10 and row + col >24):
            self.plate = 1
        else:
            self.plate = 0

        self.gotti = gotti
        self.row = row
        self.col = col
        self.loc = (row, col)



    def __str__(self):
        # print("Entered into Plate:__str__ \n ")
        return str(self.loc[0]) + "," +  str(self.loc[1])

    def __repr__(self):
        # print("Entered into Plate:__str__ \n")
        return str(self.loc[0]) + "," + str(self.loc[1])


