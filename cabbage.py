import pygame
from player import Player
from config import WIDTH, HEIGHT

RADIUS = 20

class Cabbage:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = RADIUS

    def touchesPlayer(self, player: Player):
        l1 = self.x - self.radius
        r1 = self.x + self.radius
        l2 = player.x - player.radius
        r2 = player.x + player.radius

        if l1 > r2 or r1 < l2:
            return False
        
        d1 = self.y - self.radius
        u1 = self.y + self.radius
        d2 = player.y - player.radius
        u2 = player.y + player.radius

        if d1 > u2 or u1 < d2:
            return False
        
        return True


    def render(self, screen, player):
        pygame.draw.circle(screen, 'green', (self.x - player.x+WIDTH/2.0, self.y - player.y+HEIGHT/2.0), self.radius)