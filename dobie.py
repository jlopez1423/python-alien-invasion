import pygame

class Dobie:

    def __init__(self, screen):
        """Initialize the new image I got"""
        self.screen = screen

        # Load the dobie and get its rect.
        self.image = pygame.image.load('images/dobietransparent.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
