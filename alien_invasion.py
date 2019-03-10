import pygame
import game_functions as gf
from pygame.sprite import Group
from settings import Settings
from squirrel import Squirrel
from ship import Ship
from dobie import Dobie
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    # Initialize game, settings and create a screen object.
    pygame.init()
    ai_settings = Settings()

    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Squirrel Invasion")

    # Make the play button
    play_button = Button(ai_settings, screen, "Play")


    # Make a ship
    # ship = Ship(screen)
    # Make a dobie, group of squirrels and bullets.
    dobie = Dobie(ai_settings, screen)
    bullets = Group()
    squirrels = Group()
    # squirrel = Squirrel(ai_settings, screen)

    # Create a fleet of squirrels
    gf.create_fleet(ai_settings, screen, dobie, squirrels)

    # Create an instance to store game stats
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # Start the main loop for the game.
    while True:
        # Watch for keyboard and mouse events.
        gf.check_events(ai_settings, screen, stats, play_button, dobie, squirrels, bullets)
        # if stats.game_active:
        dobie.update()
        gf.update_bullets(ai_settings, screen, stats, sb, dobie, squirrels, bullets)
        gf.update_squirrels(ai_settings, stats, screen, dobie, squirrels, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, dobie, squirrels, bullets, play_button)

run_game()
