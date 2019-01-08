import pygame

class Dobie:

    def __init__(self, ai_settings, screen):
        """Initialize the new image I got"""
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the dobie and get its rect.
        self.image = pygame.image.load('images/dobietransparent.png')
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the ship's center
        self.center = float(self.rect.centerx)

        # Movement Flag
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Update the shipsposition based on the movement flag."""
        if self.moving_right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left:
            self.center -= self.ai_settings.ship_speed_factor

        # Update the rect object from self.center.
        self.rect.centerx = self.center