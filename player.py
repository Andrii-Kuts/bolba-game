import pygame
from config import FPS, WIDTH, HEIGHT
import level

PLAYER_ACCELERATION = 4000
PLAYER_DECELERATION = 4000
PLAYER_MAX_SPEED = 300
SPRINT_SPEED = 1000
MIN_SPEED = 0

CHARACTER_SIZE = 100
HITBOX_SIZE = 60

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = HITBOX_SIZE / 2.0
        self.player_velocity_x = 0
        self.player_velocity_y = 0
        self.player_direction = 0

        bolba_source = pygame.transform.scale(
            pygame.image.load("bolba.png").convert_alpha(),
            (CHARACTER_SIZE, CHARACTER_SIZE),
        )

        self.bolba_rotated = [
            bolba_source,
            pygame.transform.rotate(bolba_source, 270),
            pygame.transform.rotate(bolba_source, 180),
            pygame.transform.rotate(bolba_source, 90),
        ]

    def tick(self):
        keystate = pygame.key.get_pressed()

        sprinting = False
        maxSpeed = 0
        if keystate[pygame.K_SPACE]:
            maxSpeed = SPRINT_SPEED
        else:
            maxSpeed = PLAYER_MAX_SPEED

        if keystate[pygame.K_a]:
            self.player_velocity_x = max(
                self.player_velocity_x - PLAYER_ACCELERATION / FPS,
                -maxSpeed
            )
        elif keystate[pygame.K_d]:
            self.player_velocity_x = min(
                self.player_velocity_x + PLAYER_ACCELERATION / FPS,
                maxSpeed
            )
        else:
            if self.player_velocity_x > 0:
                self.player_velocity_x = max(0, self.player_velocity_x - PLAYER_DECELERATION / FPS)
            else:
                self.player_velocity_x = min(0, self.player_velocity_x + PLAYER_DECELERATION / FPS)

        if keystate[pygame.K_w]:
            self.player_velocity_y = max(
                self.player_velocity_y - PLAYER_ACCELERATION / FPS,
                -maxSpeed
            )
        elif keystate[pygame.K_s]:
            self.player_velocity_y = min(
                self.player_velocity_y + PLAYER_ACCELERATION / FPS,
                maxSpeed
            )
        else:
            if self.player_velocity_y > 0:
                self.player_velocity_y = max(0, self.player_velocity_y - PLAYER_DECELERATION / FPS)
            else:
                self.player_velocity_y = min(0, self.player_velocity_y + PLAYER_DECELERATION / FPS)
        
        if abs(self.player_velocity_x) > abs(self.player_velocity_y)+0.01 and abs(self.player_velocity_x) > MIN_SPEED:
            self.player_direction = 3 if self.player_velocity_x > 0 else 1
        if abs(self.player_velocity_y) > abs(self.player_velocity_x)+0.01 and abs(self.player_velocity_y) > MIN_SPEED:
            self.player_direction = 0 if self.player_velocity_y > 0 else 2

        vx = self.player_velocity_x / FPS
        vy = self.player_velocity_y / FPS

        vx, vy = level.handleCollisions(self, vx, vy)

        self.player_velocity_x = vx * FPS
        self.player_velocity_y = vy * FPS
        self.x += vx
        self.y += vy

    def render(self, screen):
        bolba = self.bolba_rotated[self.player_direction]
        screen.blit(bolba, (WIDTH/2.0-CHARACTER_SIZE / 2.0, HEIGHT/2.0-CHARACTER_SIZE / 2.0))

