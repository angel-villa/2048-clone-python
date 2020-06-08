# Angel Villa

import pygame
import os

icon_dir = os.getcwd()+"\\icons\\"
alt_icon_dir = os.getcwd()+"/icons/"

class GameWindow:
    def __init__(self, size):
        self.size = size
        self.width = 64 + 72* self.size
        self.height = 64 + 72 * self.size
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((215,240,255))

    def update_game_state(self, game_array):
        for i in range(0, self.size):
            for j in range(0, self.size):
                try:
                    icon = pygame.image.load(icon_dir+str(game_array[i][j])+".png").convert()
                except pygame.error as e:
                    icon = pygame.image.load(alt_icon_dir+str(game_array[i][j])+".png").convert()
                self.screen.blit(icon, (j * 72 + 32, i * 72 + 32))      
                pygame.display.update()