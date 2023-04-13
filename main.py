import pygame
from game import Game

if __name__ == '__main__':
    pygame.init()
    juego = Game()
    juego.run()
    pygame.quit()
