import sys
import time
import math
from plate import Plate

class Agent():

    def __init__(self, move_type, player, given_time, matrix_values, opponent):


        self.move_type = move_type

        if(player == "BLACK"):
            self.my_player = Plate.PIECE_BLACK


            self.a = 0
            self.b = 5

            self.greater_than = 0
            self.less_than = 5
        else:
            self.my_player = Plate.PIECE_WHITE

            self.a = 11
            self.b = 16

            self.greater_than = 25
            self.less_than = 30
        board_size = 16



        board_matrix = [[None] * board_size for _ in range(board_size)]
        c = 0

        for row in range(0,16):
            for col in range(0,16):
                
                if(matrix_values[row][col] == "B"):
                    element = Plate(2, row, col)
                elif(matrix_values[row][col] == "W"):
                    element = Plate(1, row, col)
                elif(matrix_values[row][col] == "0"):
                    element = Plate(0, row, col)

                board_matrix[row][col] = element


        self.board_size = board_size
        float_time = float(given_time)


        if(self.move_type == "GAME"):
            if(float_time >= 1000):
                self.given_time = 120.0
                self.playing_depth = 3
                
                
            elif(float_time < 1000 and float_time >= 15):
                self.given_time = 15.0
                self.playing_depth = 2
            elif(float_time > 10 and float_time < 15):
                self.given_time = float_time
                self.playing_depth = 2
                #..
            elif(float_time <= 10):

                self.given_time = float_time
                self.playing_depth = 1
            
        else:
            self.given_time = float_time
            self.playing_depth = 2


        self.board_matrix = board_matrix
        self.empty_list = []
        
        for col in range(self.a, self.b):
            for row in range(self.a, self.b):
                if((row + col <= self.less_than) and (row+col >= self.greater_than)):
                    if(self.board_matrix[row][col].gotti != self.my_player):
                        self.empty_list.append(self.board_matrix[row][col])
        

        self.all_moves = []
        
        self.moves_Array = []

        self.white_destination = []
        self.black_destination = []
        for row in range(16):
            for col in range(16):

                if((row == 0 or row == 1) and (col <5)):
                    self.white_destination.append(self.board_matrix[row][col])
                elif (row>1 and row < 5 and row + col < 6):
                    self.white_destination.append(self.board_matrix[row][col])
                elif (row == 15 or row == 14) and (col>10):
                    self.black_destination.append(self.board_matrix[row][col])
                elif( row < 14 and row >10 and row + col >24):
                    self.black_destination.append(self.board_matrix[row][col])
                else:
                    continue

        self.play_move()
      
    def algorithm_Min_Max(self, depth, maximizing_player, max_time_limit, alpha=float("-inf"),
                beta=float("inf"), max_boolean=True):
        if depth == 0 or time.time() > max_time_limit:
            return self.evaluation_function(maximizing_player), None
    
        move_best = None
        if max_boolean:

            wow_value = float("-inf")
            got_moves = self.findNextMoves(maximizing_player)
        else:

            wow_value = float("inf")
            got_moves = self.findNextMoves((Plate.PIECE_BLACK
                    if maximizing_player == Plate.PIECE_WHITE else Plate.PIECE_WHITE))
       
        for move in got_moves:
            for t_place in move["t_place"]:
                if time.time() > max_time_limit:

                    return wow_value, move_best
               
                gotti = move["f_place"].gotti
                move["f_place"].gotti = Plate.PIECE_NONE
                t_place.gotti = gotti

            
                val, _ = self.algorithm_Min_Max(depth - 1,
                    maximizing_player, max_time_limit, alpha, beta, not max_boolean)
              
                t_place.gotti = Plate.PIECE_NONE
                move["f_place"].gotti = gotti
               

                if max_boolean and val > wow_value:

                    wow_value = val
                    move_best = (move["f_place"].loc, t_place.loc)
                    alpha = max(alpha, val)


                if not max_boolean and val < wow_value:

                    wow_value = val

                    move_best = (move["f_place"].loc, t_place.loc)
                    beta = min(beta, val)


                if beta <= alpha:
                    return wow_value, move_best

        return wow_value, move_best

    def play_move(self):
        start_time = time.time()
        max_time_limit = time.time() + self.given_time

        _, found_move = self.algorithm_Min_Max(self.playing_depth,
            self.my_player, max_time_limit)
        end = time.time()
        move_from = self.board_matrix[found_move[0][0]][found_move[0][1]]  
        move_to = self.board_matrix[found_move[1][0]][found_move[1][1]]
        self.all_moves = self.backtrack_moves(plate = move_from, player = self.my_player)
        self.send_output(self.all_moves, move_from, move_to)
        end_time = time.time()


    def findNextMoves(self, player=1):

        got_moves, temp_to, temp_moves = [], [], []
        def findNextMoves_general(player):
            for col in range(16):
                for row in range(16):
                
                    curr_plate = self.board_matrix[row][col]

                    if curr_plate.gotti != player:
                        continue

                    move = {
                        "f_place": curr_plate,
                        "t_place": self.findPossibleMoves(curr_plate, player)
                    }

                    got_moves.append(move)
            return got_moves
        
        if(player == self.my_player):
            
            if(len(self.empty_list) < 19):

                for col in range(self.a, self.b):
                    for row in range(self.a, self.b):
                        if(row + col <= self.less_than) and (row+col >= self.greater_than):

                            curr_plate = self.board_matrix[row][col]

                            if curr_plate.gotti != player:
                                continue

                            move = {
                                "f_place": curr_plate,
                                "t_place": self.findPossibleMoves(curr_plate, player)
                            }
                            bc_valid_moves = []
                            placed_outside = []

                            temp_from = move["f_place"]

                            for t_place in move["t_place"]:
                                if(t_place.plate == 0):
                                    placed_outside.append(t_place)

                            if(len(placed_outside) > 0):
                                move["t_place"] = placed_outside
                                temp_moves.append(move)
                                continue

                            else:
                                for t_place in move["t_place"]:
                                    row_diff = int(t_place.row) - int(temp_from.row)
                                    col_diff = int(t_place.col) - int(temp_from.col)
                                    if(self.my_player == 1):
                                        row_diff = row_diff*-1
                                        col_diff = col_diff*-1

                                    if(  row_diff >= 0 and col_diff >= 0 ):
                                        bc_valid_moves.append(t_place)
                                    else:
                                        continue
                                move["t_place"] = bc_valid_moves
                            if(len(move["t_place"] ) > 0):
                                got_moves.append(move)
                if(len(temp_moves) > 0):
                    got_moves = temp_moves

            else:
                got_moves = findNextMoves_general(player)
        else:
            got_moves = findNextMoves_general(player)
        if(len(got_moves) == 0):

            got_moves = findNextMoves_general(player)
        
        return got_moves
        
    def send_output(self, final_moves, from_plate, to_plate):

        final_moves = [str(i) for i in final_moves]
        from_plate = str(from_plate)
        to_plate = str(to_plate)
        to_value_index = (final_moves.index(to_plate))
        from_value_index = final_moves.index(from_plate)

        final_moves_list = []

        for i in range(to_value_index, len(final_moves)):
            if(final_moves[i] == final_moves[i-1]):
                continue
            if(final_moves[i] in final_moves_list):
                dupicate_index = final_moves_list.index(final_moves[i])
                final_moves_list = final_moves_list[0:dupicate_index]
            final_moves_list.append(final_moves[i])
            if(final_moves[i] == from_plate):
                break


        file2 = open("/Users/geek_vinit/Documents/SEM1/Artificial Intelligence/Homework/HW2/CODE/output.txt","w")

        final_moves_list = (",".join(final_moves_list)).split(",")[::-1]
        if(len(final_moves_list) == 4):
            if(abs(int(final_moves_list[0]) - int(final_moves_list[2]))==1 or abs(int(final_moves_list[1]) - int(final_moves_list[3]))==1 ):
               
                file2.write("E " + final_moves_list[0] + "," + final_moves_list[1] + " " + final_moves_list[2] + "," + final_moves_list[3])
            else:
                for i in range(0,len(final_moves_list)-3,2):
                   
                    file2.write("J " + final_moves_list[i] + "," + final_moves_list[i+1] + " " + final_moves_list[i+2] + "," + final_moves_list[i+3])
        else:
            for i in range(0,len(final_moves_list)-3,2):
                   
                    file2.write("J " + final_moves_list[i] + "," + final_moves_list[i+1] + " " + final_moves_list[i+2] + "," + final_moves_list[i+3])
                    file2.write("\n")
        
        file2.close()
            

    def backtrack_moves(self, plate, player, got_moves=None, adj=True):


        if got_moves is None:

            got_moves = []

        row = plate.loc[0]
        col = plate.loc[1]
        valid_plates = [Plate.PLATE_NONE, Plate.PLATE_WHITE, Plate.PLATE_BLACK]
        if plate.plate != player:
            valid_plates.remove(player)  
        if plate.plate != Plate.PLATE_NONE and plate.plate != player:
            valid_plates.remove(Plate.PLATE_NONE)  
        for next_col in range(-1, 2):
            for next_row in range(-1, 2):

                new_row = row + next_row
                new_col = col + next_col
                
                if ((new_row == row and new_col == col) or
                    new_row < 0 or new_col < 0 or
                    new_row >= self.board_size or new_col >= self.board_size):

                    continue

                new_plate = self.board_matrix[new_row][new_col]
         
                if new_plate.plate not in valid_plates:

                    continue
                if new_plate.gotti == Plate.PIECE_NONE:

                    if adj:  

                        got_moves.append(new_plate)
                        got_moves.append(plate)

                    continue

                new_row = new_row + next_row

                new_col = new_col + next_col
     
                if (new_row < 0 or new_col < 0 or
                    new_row >= self.board_size or new_col >= self.board_size):
                    continue

                new_plate = self.board_matrix[new_row][new_col]

                if new_plate in got_moves or (new_plate.plate not in valid_plates):
                    continue
                if new_plate.gotti == Plate.PIECE_NONE:

                    got_moves.insert(0, plate)
                    got_moves.insert(0, new_plate)  

                    self.backtrack_moves(new_plate, player, got_moves, False)
        return got_moves

    
    def findPossibleMoves(self, plate, player, got_moves=None, adj=True):

        if got_moves is None:
            got_moves = []

        row = plate.loc[0]
        col = plate.loc[1]

        valid_plates = [Plate.PLATE_NONE, Plate.PLATE_WHITE, Plate.PLATE_BLACK]

        if plate.plate != player:
            valid_plates.remove(player)  

        if plate.plate != Plate.PLATE_NONE and plate.plate != player:
            valid_plates.remove(Plate.PLATE_NONE)  

        for next_col in range(-1, 2):
            for next_row in range(-1, 2):

                new_row = row + next_row
                new_col = col + next_col

                if ((new_row == row and new_col == col) or
                    new_row < 0 or new_col < 0 or
                    new_row >= self.board_size or new_col >= self.board_size):
                    continue

                new_plate = self.board_matrix[new_row][new_col]
                if new_plate.plate not in valid_plates:
                    continue

                if new_plate.gotti == Plate.PIECE_NONE:
                    if adj:  
                        got_moves.append(new_plate)
                    continue
                new_row = new_row + next_row
                new_col = new_col + next_col


                if (new_row < 0 or new_col < 0 or
                    new_row >= self.board_size or new_col >= self.board_size):
                    continue

                new_plate = self.board_matrix[new_row][new_col]
                if new_plate in got_moves or (new_plate.plate not in valid_plates):
                    continue

                if new_plate.gotti == Plate.PIECE_NONE:
                    got_moves.insert(0, new_plate)  
                    self.findPossibleMoves(new_plate, player, got_moves, False)

        return got_moves
        
    def evaluation_function(self, player):

        def eucledian_distance(p0, p1):
            temp = math.sqrt((p1[0] - p0[0])**2 + (p1[1] - p0[1])**2)
            return temp

        dist_value = 0
        for col in range(self.board_size):
            for row in range(self.board_size):
                plate = self.board_matrix[row][col]
                if plate.gotti == Plate.PIECE_WHITE:
                    distances = [eucledian_distance(plate.loc, g.loc) for g in
                                 self.white_destination if g.gotti != Plate.PIECE_WHITE]
                    dist_value -= max(distances) if len(distances) else -50
                elif plate.gotti == Plate.PIECE_BLACK:
                    distances = [eucledian_distance(plate.loc, g.loc) for g in
                                 self.black_destination if g.gotti != Plate.PIECE_BLACK]
                    dist_value += max(distances) if len(distances) else -50

        if player == Plate.PIECE_BLACK:

            dist_value *= -1

        return dist_value

def compute_matrix(inp):
    matrix_values_str = []
    temp_matrix_values  = []
    matrix_values = []
    for j in range(16):
        matrix_values_str.append(inp[j+3])
    for i in matrix_values_str:
        for x in i:
            if(x == "B"):
                temp_matrix_values.append("B")
            elif(x == "W"):
                temp_matrix_values.append("W")
            elif(x == "."):
                temp_matrix_values.append("0")

            else:
                pass
        matrix_values.append(temp_matrix_values)
        temp_matrix_values = []
    return matrix_values


def print_input(move_type, color, time_rem, matrix_values):
        print("---------------------- INPUT VALYES START----------------------")
        print("move_type",  move_type)
        print("color" , color)
        print( "time_rem",  time_rem)
        print( "matrix_values: \n ",matrix_values)
        print("---------------------- INPUT VALUES END----------------------")


if __name__ == "__main__":

    file1 = open("/Users/geek_vinit/Documents/SEM1/Artificial Intelligence/Homework/HW2 safety/CODE/input_1.txt","r")
    input_ = file1.readlines()
    file1.close()
    move_type = input_[0][0:-1]
    color = input_[1][0:-1]
    time_rem = input_[2][0:-1]
    matrix_values = compute_matrix(input_)
    opponent = input_[0].strip()

    

    agent = Agent(move_type, color, time_rem, matrix_values, opponent)

    