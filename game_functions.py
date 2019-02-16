import sys
import pygame
from bullet import Bullet
from squirrel import Squirrel

def check_events(ai_settings, screen, ship, bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        # Move the ship to the right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(ai_settings, screen, ship, squirrels, bullets):
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    # Redraw the bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    squirrels.draw(screen)

    # Make the most recently drawn screen visible.
    pygame.display.flip()

def update_bullets(bullets):
    """Update position of bullets and get rid of old bullets"""
    # Update bullet positions
    bullets.update()
    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    # Create  a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def create_fleet(ai_settings, screen, squirrels):
    """Create a full fleet of squirrels"""
    # Create a squirrel and find the number of suirrels in a row.
    # Spacing between each squirel is equal to one squirrel width
    squirrel = Squirrel(ai_settings, screen)
    squirrel_width = squirrel.rect.width
    number_squirrels_x = get_number_squirrels_x(ai_settings, squirrel.rect.width)

    # create the first row of squirrels
    for squirrel_number in range(number_squirrels_x):
        # Create an squirrel and place it in the row.
        create_squirrel(ai_settings, screen, squirrels, squirrel_number)


def get_number_squirrels_x(ai_settings, squirrel_width):
    """Determine the number of squirrels that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * squirrel_width
    number_squirrels_x = int(available_space_x / (2 * squirrel_width))
    return number_squirrels_x


def create_squirrel(ai_settings, screen, squirrels, squirrel_number):
    """Create a squirrel and place it in the row."""
    squirrel = Squirrel(ai_settings, screen)
    squirrel_width = squirrel.rect.width
    squirrel.x = squirrel_width + 2 * squirrel_width * squirrel_number
    squirrel.rect.x = squirrel.x
    squirrels.add(squirrel)