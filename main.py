import pygame
import level
import player as playerModule
from config import FPS, WIDTH, HEIGHT
from scoreCounter import ScoreCounter

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My AAA Game")
clock = pygame.time.Clock()

running = True
player = playerModule.Player(0, 0)
scoreCounter = ScoreCounter()

# Main game loop
while running:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    # Logic
    player.tick()
    level.tick(player, scoreCounter)

    # Render    
    screen.fill((0, 0, 0))
    player.render(screen)
    level.render(screen, player)
    scoreCounter.render(screen)
    pygame.display.flip()

    # tick the clock so that our computer doesn't explode
    clock.tick(FPS)


