import pygame
import sys
from config import Config, ConfigWindow
from game import Game

def main():

    pygame.init()
    
    config_window = ConfigWindow()
    config = config_window.show()
    
    if config:
        game = Game(config)
        game.run()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()