# Angel Villa

# the commented lines are not integral to the gameplay, I simply used them to write the game board and input to a file

import pygame
import keyboard
import time

import GameArray
import GameWindow


keys = {'w' : '1', 'a' : '2', 's' : '3', 'd' : '4'}

# def remove_line(file):
    # lines = file.readlines()
    # lines = lines[:-1]
            
def main():
    # f = open("train_2048.txt", "a+")
    board = GameArray.GameArray(4)
    window = GameWindow.GameWindow(board.size)
    board.add_next()
    board.add_next()
    running = True
    while running:
        
        initial_state = board.get_arr()
        
        window.update_game_state(board.arr)
        pygame.event.get()
        
        move = keyboard.read_key()
        move = move + " "
        wasd_in = move[0]
        
        board.shift(wasd_in)
            
        curr_state = board.get_arr()
        window.update_game_state(board.arr) 

        time.sleep(0.1)
        
        if wasd_in == 'p':
            # f.close()
            running = False
        elif not (board.can_shift_up() or board.can_shift_down() or board.can_shift_left() or board.can_shift_right()):
            time.sleep(5)
            running = False
        # elif wasd_in == 'b' and (initial_state != curr_state):
            # remove_line(f)
        # elif (wasd_in in ['w', 'a', 's', 'd']) and (initial_state != curr_state):
            # for i in initial_state:
                # for j in i:
                    # f.write(str(j)+", ")
            # f.write(keys[wasd_in]+"\n")
        else:
            continue
            
if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()

