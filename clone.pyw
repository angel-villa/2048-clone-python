# Angel Villa

# the commented lines are not integral to the gameplay, I simply used them to write the game board and input to a file
# need to find a way to prevent pygame from freezing, stackoverflow suggestions did not work after some brief testing

import pygame
import keyboard
import time

import GameArray
import GameWindow
import decide_move as dm

# mapping inputs to integers for writing to file
keys = {'w' : '1', 'a' : '2', 's' : '3', 'd' : '4'}

def remove_line(file):
    lines = file.readlines()
    lines = lines[:-1]

# main game loop
def main():
    f = open("train_2048.txt", "a+")
    # size is the size of the grid, 4 is the original game
    size = 4
    board = GameArray.GameArray(size)
    window = GameWindow.GameWindow(board.size)
    
    # add two tiles to start the game
    board.add_next()
    board.add_next()
    
    running = True
    while running:
        initial_state = board.get_arr()
        initial_score = board.score
        window.update_game_state(board.arr, board.score)
        pygame.event.get()
                
        # move = keyboard.read_key()
        # move = move + " "
        # wasd_in = move[0]
        
        wasd_in = dm.decide_move(board, 1)
        board.shift(wasd_in)
            
        curr_state = board.get_arr()
        window.update_game_state(board.arr, board.score) 

        time.sleep(0.01)
        
        if wasd_in == 'p':
            # f.close()
            running = False
        elif not (board.can_shift_up() or board.can_shift_down() or board.can_shift_left() or board.can_shift_right()):
            time.sleep(30)
            running = False
        elif wasd_in == 'b' and (initial_state != curr_state):
            remove_line(f)
        elif (wasd_in in ['w', 'a', 's', 'd']) and (initial_state != curr_state):
            pass
            # max_val = 0
            # for i in initial_state:
                # for j in i:
                    # if j >= max_val:
                        # max_val = j
                    # f.write(str(j)+", ")
            # f.write(str(initial_score)+", "+str(max_val)+", "+keys[wasd_in]+"\n")
        else:
            continue
            
if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()

