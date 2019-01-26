import pygame
import game_functions as gf
from pygame.sprite import Group
from settings import Settings
from squirrel import Squirrel
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
    dobie = Dobie(ai_settings, screen)
    # Make a group to store bullets in.
    bullets = Group()
    squirrel = Squirrel(ai_settings, screen)


    # Start the main loop for the game.
    while True:
        # Watch for keyboard and mouse events.
        gf.check_events(ai_settings, screen, dobie, bullets)
        dobie.update()
        gf.update_bullets(bullets)
        gf.update_screen(ai_settings, screen, dobie, squirrel, bullets)

run_game()
