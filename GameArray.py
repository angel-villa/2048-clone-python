# Angel Villa

import random 

''' 
# no longer used
# uncomment if you want to use print_game_state() on GameArray object (draws array to terminal)
def print_space(n):
    print(" " * n, end ="")
'''

class GameArray:
    def __init__(self, size):
        self.size = size
        self.score = 0
        self.arr = [[0 for x in range(self.size)] for y in range(self.size)]
        # am = already merged, used to keep track of tiles that have been merged into
        self.am = [[False for x in range(self.size)] for y in range(self.size)]
        self.undo_moves = [0 for x in range(20)]
        self.undo_score = [0 for x in range(20)]
        
    # reset the am array after each turn
    def reset_merged(self):
        self.am = [[False for x in range(self.size)] for y in range(self.size)]
        
    # returns the contents of the current game array, using this to prevent referencing issues
    def get_arr(self):
        temp = [[0 for x in range(self.size)] for y in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                temp[i][j] = self.arr[i][j]
        return temp
        
    # returns the max tile value of the game array
    def max_tile(self):
        return max(max(row) for row in self.arr)
        
    # returns the value of the top right corner tile
    def corner_tile(self):
        return self.arr[0][self.size-1]
        
    def left_col_sum(self):
        temp_sum = 0
        for row in self.arr:
            temp_sum += row[self.size-1]
        return temp_sum
        
    def top_right_weighted_sum(self):
        temp_sum = 0
        ascend_row = False
        weight = int(self.size**2)
        for j in range(self.size-1, -1, -1):
            ascend_row = not ascend_row
            if ascend_row:
                for i in range(self.size):
                    temp_sum += 2**(weight)/(2**int(self.size**2)) * self.arr[i][j]
                    weight -= 1
            else:
                for i in range(self.size-1, -1, -1):
                    temp_sum += 2**(weight)/(2**int(self.size**2)) * self.arr[i][j]
                    weight -= 1
        return temp_sum
                    
    # pop from undo_moves array to undo to previous turn's array
    def undo(self):
        if self.undo_moves:
            self.score = self.undo_score.pop()
            
            temp_arr = self.undo_moves.pop()
            k = 0
            for i in range(self.size):
                for j in range(self.size):
                    self.arr[i][j] = temp_arr[k]
                    k += 1
    
    def add_next(self):
        num_open = 0
        loop_count = 0

        # count all empty tiles
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.arr[i][j] == 0:
                    num_open += 1

        decide_int = random.randint(0, num_open - 1)
        refer_int = random.randint(1, 10)

        # add new tile to an empty space with probabilities
        # p(new tile == 2) = 0.9
        # p(new tile == 4) = 0.1
        if num_open != 0:
            for i in range(0, self.size):
                for j in range(0, self.size):
                    if self.arr[i][j] == 0:
                        if decide_int == loop_count and refer_int == 10:
                            self.arr[i][j] = 4
                        elif decide_int == loop_count and refer_int <= 9:
                            self.arr[i][j] = 2
                        loop_count += 1
        # elif num_open == 0:
            # print("You lose.")
            
    def can_shift(self, key):
        if key == 's':
            return self.can_shift_down()
        elif key == 'a':
            return self.can_shift_left()
        elif key == 'd':
            return self.can_shift_right()
        elif key == 'w':
            return self.can_shift_up()
        return False
        
    def can_shift_down(self):
        empty_count = 0
        merge_count = 0
        
        # for every tile in the array...
        for j in range(0, self.size):
            for i in range(self.size - 1, -1, -1):
                # ...look downwards
                #   if      there is a same-value tile downhill with nothing in between,
                #   or if   there is space between the tile and the next downhill tile
                # the array can shift, return true
                if i > 0 and self.arr[i][j] != 0 and self.arr[i][j] == self.arr[i - 1][j]:
                    merge_count += 1
                for k in range(self.size - 1, i, -1):
                    if self.arr[i][j] != 0 and self.arr[k][j] == 0:
                        empty_count += 1
                    
        if empty_count != 0 or merge_count != 0:
            return True
        else:
            return False

    def can_shift_left(self):
        empty_count = 0
        merge_count = 0
        
        # see can_shift_down
        for i in range(0, self.size):
            for j in range(0, self.size):
                if j < self.size - 1 and self.arr[i][j] != 0 and self.arr[i][j] == self.arr[i][j + 1]:
                    merge_count += 1
                for k in range(0, j):
                    if self.arr[i][j] != 0 and self.arr[i][k] == 0:
                        empty_count += 1
                    
        if empty_count != 0 or merge_count != 0:
            return True
        else:
            return False

    def can_shift_right(self):
        empty_count = 0
        merge_count = 0
    
        # see can_shift_down
        for i in range(0, self.size):
            for j in range(self.size - 1, -1, -1):
                if j > 0 and self.arr[i][j] != 0 and self.arr[i][j] == self.arr[i][j - 1]:
                    merge_count += 1
                for k in range(self.size - 1, j, -1):
                    if self.arr[i][j] != 0 and self.arr[i][k] == 0:
                        empty_count += 1
                    
        if empty_count != 0 or merge_count != 0:
            return True
        else:
            return False    
        
    def can_shift_up(self):
        empty_count = 0
        merge_count = 0
    
        # see can_shift_down
        for i in range(0, self.size):
            for j in range(0, self.size):
                if i < self.size - 1 and self.arr[i][j] != 0 and self.arr[i][j] == self.arr[i + 1][j]:
                    merge_count += 1
                for k in range(0, i):
                    if self.arr[i][j] != 0 and self.arr[k][j] == 0:
                        empty_count += 1
                    
        if empty_count != 0 or merge_count != 0:
            return True
        else:
            return False    
    
    def shift(self, direction):     
        prev_score = self.score
        
        prev = [0 for i in range(self.size**2)]
        k = 0
        for i in range(self.size):
            for j in range(self.size):
                prev[k] = self.arr[i][j]
                k += 1
        
        if direction == 'w' and self.can_shift_up():
            # append the current array "prev" (I know...) to undo_moves array
            # dequeue from undo moves such that it does not exceed 20 moves
            # TO DO: make this a deque
            self.undo_moves.append(prev);
            self.undo_score.append(prev_score)
            if len(self.undo_moves) > 20:
                self.undo_moves = self.undo_moves[1:]
            if len(self.undo_score) > 20:
                self.undo_score = self.undo_score[1:]
                
            # convoluted logic to transform (shift) game array based on the input move
            for j in range(0, self.size):
                for i in range(0, self.size):
                    if self.arr[i][j] != 0:
                        for k in range(0, i):
                            if self.arr[k][j] == 0:
                                place_int = self.arr[i][j]
                                self.arr[i][j] = 0
                                self.arr[k][j] = place_int
                            elif self.arr[k][j] != 0 and self.arr[k][j] != self.arr[i][j] and self.arr[k + 1][j] == 0:
                                place_int = self.arr[i][j]
                                self.arr[i][j] = 0
                                self.arr[k + 1][j] = place_int
                            elif self.arr[k][j] == self.arr[i][j]:
                                empty_between = 0
                                for l in range(i - 1, k, -1):
                                    if self.arr[l][j] != 0:
                                        empty_between += 1
                                        
                                # if a tile was just merged-into this turn, do not use it to merge again
                                # this little bug (tile merged more than once) was unbeknownst to me for a while,
                                # luckily the fix was small and simple by creating the 'already merged' array
                                if i - 1 == k and self.am[k][j] == False:
                                    self.arr[i][j] = 0
                                    self.arr[k][j] = self.arr[k][j] * 2
                                    self.score += self.arr[k][j]
                                    self.am[k][j] = True
                                elif empty_between == 0 and self.am[k][j] == False:
                                    self.arr[i][j] = 0
                                    self.arr[k][j] = self.arr[k][j] * 2
                                    self.score += self.arr[k][j]
                                    self.am[k][j] = True
            self.add_next()
            self.reset_merged()
            
        # see if statement above
        elif direction == 'a' and self.can_shift_left():
            self.undo_moves.append(prev);
            self.undo_score.append(prev_score)
            if len(self.undo_moves) > 20:
                self.undo_moves = self.undo_moves[1:]
            if len(self.undo_score) > 20:
                self.undo_score = self.undo_score[1:]
                
            for i in range(0, self.size):
                for j in range(0, self.size):
                    if self.arr[i][j] != 0:
                        for k in range(0, j):
                            if self.arr[i][k] == 0:
                                place_int = self.arr[i][j]
                                self.arr[i][j] = 0
                                self.arr[i][k] = place_int
                            elif self.arr[i][k] != 0 and self.arr[i][k] != self.arr[i][j] and self.arr[i][k + 1] == 0:
                                place_int = self.arr[i][j]
                                self.arr[i][j] = 0
                                self.arr[i][k + 1] = place_int
                            elif self.arr[i][k] == self.arr[i][j]:
                                empty_between = 0
                                for l in range(j - 1, k, -1):
                                    if self.arr[i][l] != 0:
                                        empty_between += 1
                                if j - 1 == k and self.am[i][k] == False:
                                    self.arr[i][j] = 0
                                    self.arr[i][k] = self.arr[i][k] * 2
                                    self.score += self.arr[i][k]
                                    self.am[i][k] = True
                                elif empty_between == 0 and self.am[i][k] == False:
                                    self.arr[i][j] = 0
                                    self.arr[i][k] = self.arr[i][k] * 2
                                    self.score += self.arr[i][k]
                                    self.am[i][k] = True
            self.add_next()              
            self.reset_merged()
            
        # see if statement above
        elif direction == 's' and self.can_shift_down():
            self.undo_moves.append(prev);
            self.undo_score.append(prev_score)
            if len(self.undo_moves) > 20:
                self.undo_moves = self.undo_moves[1:]
            if len(self.undo_score) > 20:
                self.undo_score = self.undo_score[1:]
                
            for j in range(0, self.size):
                for i in range(self.size - 1, -1, -1):
                    if self.arr[i][j] != 0:
                        for k in range(self.size - 1, i, -1):
                            if self.arr[k][j] == 0:
                                place_int = self.arr[i][j]
                                self.arr[i][j] = 0
                                self.arr[k][j] = place_int
                            elif self.arr[k][j] != 0 and self.arr[k][j] != self.arr[i][j] and self.arr[k - 1][j] == 0:
                                place_int = self.arr[i][j]
                                self.arr[i][j] = 0
                                self.arr[k - 1][j] = place_int
                            elif self.arr[k][j] == self.arr[i][j]:
                                empty_between = 0
                                for l in range(i + 1, k):
                                    if self.arr[l][j] != 0:
                                        empty_between += 1
                                if i + 1 == k and self.am[k][j] == False:
                                    self.arr[i][j] = 0
                                    self.arr[k][j] = self.arr[k][j] * 2
                                    self.score += self.arr[k][j]
                                    self.am[k][j] = True
                                    
                                elif empty_between == 0 and self.am[k][j] == False:
                                    self.arr[i][j] = 0
                                    self.arr[k][j] = self.arr[k][j] * 2
                                    self.score += self.arr[k][j]
                                    self.am[k][j] = True
                                    
            self.add_next()      
            self.reset_merged()
            
        # see if statement above
        elif direction == 'd' and self.can_shift_right():
            self.undo_moves.append(prev);
            self.undo_score.append(prev_score)
            if len(self.undo_moves) > 20:
                self.undo_moves = self.undo_moves[1:]
            if len(self.undo_score) > 20:
                self.undo_score = self.undo_score[1:]

            for i in range(0, self.size):
                for j in range(self.size - 1, -1, -1):
                    if self.arr[i][j] != 0:
                        for k in range(self.size - 1, j, -1):
                            if self.arr[i][k] == 0:
                                place_int = self.arr[i][j]
                                self.arr[i][j] = 0
                                self.arr[i][k] = place_int
                            elif self.arr[i][k] != 0 and self.arr[i][k] != self.arr[i][j] and self.arr[i][k- 1] == 0:
                                place_int = self.arr[i][j]
                                self.arr[i][j] = 0
                                self.arr[i][k - 1] = place_int
                            elif self.arr[i][k] == self.arr[i][j]:
                                empty_between = 0
                                for l in range(j + 1, k):
                                    if self.arr[i][l] != 0:
                                        empty_between += 1
                                if j + 1 == k and self.am[i][k] == False:
                                    self.arr[i][j] = 0
                                    self.arr[i][k] = self.arr[i][k] * 2
                                    self.score += self.arr[i][k]
                                    self.am[i][k] = True
                                elif empty_between == 0 and self.am[i][k] == False:
                                    self.arr[i][j] = 0
                                    self.arr[i][k] = self.arr[i][k] * 2
                                    self.score += self.arr[i][k]
                                    self.am[i][k] = True
            self.add_next()      
            self.reset_merged()
            
        # undo if 'b' is pressed
        elif direction == 'b' and (len(self.undo_moves) >= 1):
            self.undo()
        
'''
    # draw game board to terminal
    # no longer used, we pygame now
    # uncomment if you want to feel like a hacker playing 2048 on a black and green terminal
    def print_game_state(self):
        print("_" * (self.size*6))
        for i in range(0, self.size):
            print('|')
            for j in range(0,self.size):
                if self.arr[i][j] != 0:
                    print_space(5 - len(str(self.arr[i][j])))
                    print(str(self.arr[i][j]) + "|",end="")
                else:
                    print_space(5)
                    print("|",end ="")
            print("\n")
            print("_" * (self.size*6))
'''