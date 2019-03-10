import sys
import pygame
from bullet import Bullet
from squirrel import Squirrel
from time import sleep


def ship_hit(ai_settings, stats, screen, dobie, squirrels, bullets):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships_left
        stats.ships_left -= 1

        # Empty the list of aliens and bullets
        squirrels.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, dobie, squirrels)
        dobie.center_dobie()

        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset game settings
        ai_settings.initialize_dynamic_settings()
        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

        # Reset the game stats
        stats.reset_stats()
        stats.game_active = True

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_dobie()


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


def update_screen(ai_settings, screen, stats, sb, ship, squirrels, bullets, play_button):
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    # Redraw the bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    squirrels.draw(screen)

    # Draw the score information
    sb.show_score()

    # Draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, dobie, squirrels, bullets):
    """Update position of bullets and get rid of old bullets"""
    # Update bullet positions
    bullets.update()
    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # Check for any bullets that have hit squirrels
    # If so get rid of the bullet and squirrel
    check_bullet_collisions(ai_settings, screen, stats, sb, dobie, squirrels, bullets)


def check_bullet_collisions(ai_settings, screen, stats, sb, dobie, squirrels, bullets):
    collisions = pygame.sprite.groupcollide(bullets, squirrels, True, True)
    if collisions:
        for squirrels in collisions.values():
            stats.score += ai_settings.alien_points * len(squirrels)
            sb.prep_score()


    if len(squirrels) == 0:
        # Destroy existing bullets and create new fleet
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, dobie, squirrels)


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    # Create  a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def create_fleet(ai_settings, screen, dobie,squirrels):
    """Create a full fleet of squirrels"""
    # Create a squirrel and find the number of suirrels in a row.
    # Spacing between each squirel is equal to one squirrel width
    squirrel = Squirrel(ai_settings, screen)
    squirrel_width = squirrel.rect.width
    number_squirrels_x = get_number_squirrels_x(ai_settings, squirrel.rect.width)
    number_rows = get_number_rows(ai_settings, dobie.rect.height, squirrel.rect.height)

    # create the first row of squirrels
    for row_number in range(number_rows):
        for squirrel_number in range(number_squirrels_x):
            # Create an squirrel and place it in the row.
            create_squirrel(ai_settings, screen, squirrels, squirrel_number, row_number)


def get_number_squirrels_x(ai_settings, squirrel_width):
    """Determine the number of squirrels that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * squirrel_width
    number_squirrels_x = int(available_space_x / (2 * squirrel_width))
    return number_squirrels_x


def create_squirrel(ai_settings, screen, squirrels, squirrel_number, row_number):
    """Create a squirrel and place it in the row."""
    squirrel = Squirrel(ai_settings, screen)
    squirrel_width = squirrel.rect.width
    squirrel.x = squirrel_width + 2 * squirrel_width * squirrel_number
    squirrel.rect.x = squirrel.x
    squirrel.rect.y = squirrel.rect.height + 2 * squirrel.rect.height * row_number
    squirrels.add(squirrel)


def get_number_rows(ai_settings, ship_height, squirrel_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height -
                         (3 * squirrel_height) - ship_height)
    number_rows = int(available_space_y / (2 * squirrel_height))
    return number_rows


def update_squirrels(ai_settings, stats, screen, dobie, squirrels, bullets):
    """Update the positions of all the squirrels in the fleet."""
    """Check if the fleet is at an edge then update the positions of all squirrels in fleet"""
    check_fleet_edges(ai_settings, squirrels)
    squirrels.update()

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(dobie, squirrels):
        ship_hit(ai_settings, stats, screen, dobie, squirrels, bullets)
    # Look for squirrels hitting the bottom of the screen
    check_aliens_bottom(ai_settings, stats, screen, dobie, squirrels, bullets)


def check_fleet_edges(ai_settings, squirrels):
    """respond appropriately if any aliens have reached an edge."""
    for squirrel in squirrels.sprites():
        if squirrel.check_edges():
            change_fleet_direction(ai_settings, squirrels)
            break

def change_fleet_direction(ai_settings, squirrels):
    """Drop the entire fleet and change the fleets direction"""
    for squirrel in squirrels.sprites():
        squirrel.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_aliens_bottom(ai_settings, stats, screen, dobie, squirells, bullets):
    """Check if any squirrels have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for squirrel in squirells.sprites():
        if squirrel.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit
            ship_hit(ai_settings, stats, screen, dobie, squirells, bullets)
            break