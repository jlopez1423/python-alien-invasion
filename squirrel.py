import pygame
from pygame.sprite import Sprite


class Squirrel(Sprite):
    """A class to represent a single squirrel in the fleet."""

    def __init__(self, ai_settings, screen):
        """Initialize the squirrel and set its starting position."""
        super(Squirrel, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the squirrel image and se its rect attribute.
        self.image = pygame.image.load('images/squirrel.jpg')
        self.rect = self.image.get_rect()

        # Start each new squirrel near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the squirrel at its current location."""
        self.screen.blit(self.image, self.rect)