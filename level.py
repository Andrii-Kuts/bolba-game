import random
import pygame
from obstacle import Obstacle
from player import Player
from cabbage import Cabbage
from config import WIDTH, HEIGHT

obstacles = []
cabbages = []

BLOCK_SIZE = 70
ROWS = 101
COLUMNS = 101
OFFSET_X = 100
OFFSET_Y = 100

def pointFromGrid(row, column):
    return (OFFSET_X + (column+0.5) * BLOCK_SIZE, OFFSET_Y + (row+0.5) * BLOCK_SIZE)

def createLevelFromGrid(grid):
    for i in range(ROWS):
        for j in range(COLUMNS):
            if grid[i][j]:
                x = j * BLOCK_SIZE + OFFSET_X
                y = i * BLOCK_SIZE + OFFSET_Y
                obstacles.append(Obstacle(
                    x,
                    x + BLOCK_SIZE,
                    y,
                    y + BLOCK_SIZE
                ))

def placeCabbage(i, j):
    point = pointFromGrid(i, j)
    cabbages.append(Cabbage(point[0], point[1]))

DX = [0, 1, 0, -1]
DY = [1, 0, -1, 0]

def generateMaze(grid, loopProbability):
    stack = [(1, 1)]
    grid[1][1] = False

    while len(stack) > 0:
        x, y = stack.pop()

        directions = [0, 1, 2, 3]
        random.shuffle(directions)
        for direction in directions:
            newX = x + DX[direction]*2
            newY = y + DY[direction]*2
            if newX < 0 or newX >= ROWS or newY < 0 or newY >= COLUMNS:
                continue
            if not grid[newX][newY]:
                if random.random() < loopProbability:
                    grid[x+DX[direction]][y+DY[direction]] = False
                continue
            grid[x+DX[direction]][y+DY[direction]] = False
            grid[newX][newY] = False
            stack.append((newX, newY))
    


def createLevel():
    grid = [[True for _ in range(0, COLUMNS)] for _ in range(0, ROWS)]

    grid[0][1] = False
    grid[ROWS-1][COLUMNS-1] = False
    generateMaze(grid, 0.1)

    for i in range(ROWS):
        for j in range(COLUMNS):
            if not grid[i][j] and random.random() < 0.1:
                placeCabbage(i, j)

    createLevelFromGrid(grid)

def handleCollisions(player: Player, vx, vy):
    for obstacle in obstacles:
        newVx = obstacle.limitX(player, vx)
        if vx > 0:
            vx = min(vx, newVx)
        else:
            vx = max(vx, newVx)
    player.x += vx
    for obstacle in obstacles:
        newVy = obstacle.limitY(player, vy)
        if vy > 0:
            vy = min(vy, newVy)
        else:
            vy = max(vy, newVy)
    player.y += vy
    return (vx, vy)

def handleCabbageCollection(player: Player, scoreCounter):
    for cabbage in cabbages:
        if cabbage.touchesPlayer(player):
            cabbages.remove(cabbage)
            scoreCounter.increment()

def tick(player, scoreCounter):
    handleCabbageCollection(player, scoreCounter)


def render(screen, player):
    for obstacle in obstacles:
        pygame.draw.rect(
            screen,
            "white",
            pygame.Rect(
                obstacle.l - player.x + WIDTH/2.0,
                obstacle.d - player.y + HEIGHT/2.0,
                obstacle.r - obstacle.l,
                obstacle.u - obstacle.d
            )
        )
    for cabbage in cabbages:
        cabbage.render(screen, player)

createLevel()
