# Angel Villa

import random 
import sys

def print_space(n):
    print(" " * n, end ="")

class GameArray:
    def __init__(self, size):
        self.size = size
        self.arr = [[0 for x in range(self.size)] for y in range(self.size)]
        self.previous_arr = self.get_arr()
        # am = already merged
        self.am = [[False for x in range(self.size)] for y in range(self.size)]
        self.undo_moves = [0 for x in range(20)]
        
    def reset_merged(self):
        self.am = [[False for x in range(self.size)] for y in range(self.size)]
        
    def get_arr(self):
        temp = [[0 for x in range(self.size)] for y in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                temp[i][j] = self.arr[i][j]
        return temp
        
    def undo(self):
        if isinstance(self.undo_moves[-1], list):
            temp_arr = self.undo_moves.pop(-1)
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

        if num_open != 0:
            for i in range(0, self.size):
                for j in range(0, self.size):
                    if self.arr[i][j] == 0:
                        if decide_int == loop_count and refer_int == 10:
                            self.arr[i][j] = 4
                        elif decide_int == loop_count and refer_int <= 9:
                            self.arr[i][j] = 2
                        loop_count += 1
        elif num_open == 0:
            print("You lose.")
        
    def can_shift_down(self):
        empty_count = 0
        merge_count = 0
    
        for j in range(0, self.size):
            for i in range(self.size - 1, -1, -1):
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
        temp_previous_arr = self.get_arr()
        
        prev = [0 for i in range(self.size**2)]
        k = 0
        for i in range(self.size):
            for j in range(self.size):
                prev[k] = self.arr[i][j]
                k += 1
        
        if direction == 'w' and self.can_shift_up():
            self.undo_moves.append(prev);
            if len(self.undo_moves) > 20:
                self.undo_moves = self.undo_moves[1:]
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
                                # Need to prevent [k,j] from getting merged again.
                                if i - 1 == k and self.am[k][j] == False:
                                    self.arr[i][j] = 0
                                    self.arr[k][j] = self.arr[k][j] * 2
                                    self.am[k][j] = True
                                elif empty_between == 0 and self.am[k][j] == False:
                                    self.arr[i][j] = 0
                                    self.arr[k][j] = self.arr[k][j] * 2
                                    self.am[k][j] = True
            self.add_next()
            self.reset_merged()
            self.previous_arr = temp_previous_arr
        elif direction == 'a' and self.can_shift_left():
            self.undo_moves.append(prev);
            if len(self.undo_moves) > 20:
                self.undo_moves = self.undo_moves[1:]
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
                                    self.am[i][k] = True
                                elif empty_between == 0 and self.am[i][k] == False:
                                    self.arr[i][j] = 0
                                    self.arr[i][k] = self.arr[i][k] * 2
                                    self.am[i][k] = True
            self.add_next()              
            self.reset_merged()
            self.previous_arr = temp_previous_arr
        elif direction == 's' and self.can_shift_down():
            self.undo_moves.append(prev);
            if len(self.undo_moves) > 20:
                self.undo_moves = self.undo_moves[1:]
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
                                    self.am[k][j] = True
                                    
                                elif empty_between == 0 and self.am[k][j] == False:
                                    self.arr[i][j] = 0
                                    self.arr[k][j] = self.arr[k][j] * 2
                                    self.am[k][j] = True
                                    
            self.add_next()      
            self.reset_merged()
            self.previous_arr = temp_previous_arr
        elif direction == 'd' and self.can_shift_right():
            self.undo_moves.append(prev);
            if len(self.undo_moves) > 20:
                self.undo_moves = self.undo_moves[1:]
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
                                    self.am[i][k] = True
                                elif empty_between == 0 and self.am[i][k] == False:
                                    self.arr[i][j] = 0
                                    self.arr[i][k] = self.arr[i][k] * 2
                                    self.am[i][k] = True
            self.add_next()      
            self.reset_merged()
            self.previous_arr = temp_previous_arr
        elif direction == 'b' and (len(self.undo_moves) >= 1):
            self.undo()
        
                
    def update_game_state(self):
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
        sys.stdout.flush()          
    

