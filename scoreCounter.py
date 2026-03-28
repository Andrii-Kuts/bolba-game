import pygame
from config import WIDTH

class ScoreCounter:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.counterText = self.font.render(f'Score: {self.score}', True, 'green')
        self.textRect = self.counterText.get_rect()
        self.textRect.center = (WIDTH - 150, 50)

    def updateCounter(self):
        self.counterText = self.font.render(f'Score: {self.score}', True, 'green')
        self.textRect = self.counterText.get_rect()
        self.textRect.center = (WIDTH - 150, 50)

    def increment(self):
        self.score = self.score+1
        self.updateCounter()

    def render(self, screen):
        screen.blit(self.counterText, self.textRect)