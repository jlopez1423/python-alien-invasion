import pygame
import game_functions as gf

from settings import Settings
from ship import Ship
from dobie import Dobie

def run_game():
    # Initialize game, settings and create a screen object.
    pygame.init()
    ai_settings = Settings()

    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make a ship
    # ship = Ship(screen)
    dobie = Dobie(screen)

    # Set background color.
    # bg_color = (230, 230, 230)
    # bg_color = (30, 144, 255)

    # Start the main loop for the game.
    while True:
        # Watch for keyboard and mouse events.
        gf.check_events()
        gf.update_screen(ai_settings, screen, dobie)


run_game()
