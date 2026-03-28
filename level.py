import random
import pygame
from player import Player
from cabbage import Cabbage
from config import WIDTH, HEIGHT

class Obstacle:
    def __init__(self, l, r, d, u):
        self.l = l
        self.r = r
        self.u = u
        self.d = d

    def limitX(self, player: Player, vx):
        pu = player.y + player.radius
        pd = player.y - player.radius
        pl = player.x - player.radius
        pr = player.x + player.radius
        if pu <= self.d or pd >= self.u:
            return vx
        
        if vx > 0:
            d = self.l - pr
            if d < 0:
                return vx
            return min(vx, d)
        else:
            d = self.r - pl
            if d > 0:
                return vx
            return max(vx, d)
        
    def limitY(self, player: Player, vy):
        pu = player.y + player.radius
        pd = player.y - player.radius
        pl = player.x - player.radius
        pr = player.x + player.radius
        if pr <= self.l or pl >= self.r:
            return vy
        
        if vy > 0:
            d = self.d - pu
            if d < 0:
                return vy
            return min(vy, d)
        else:
            d = self.u - pd
            if d > 0:
                return vy
            return max(vy, d)
        

obstacles = []
cabbages = []

BLOCK_SIZE = 80
ROWS = 51
COLUMNS = 51
OFFSET_X = 100
OFFSET_Y = 100

def pointFromGrid(row, column):
    return (OFFSET_X + (column+0.5) * BLOCK_SIZE, OFFSET_Y + (row+0.5) * BLOCK_SIZE)

def createLevelFromGrid(grid):
    for i in range(ROWS):
        for j in range(COLUMNS):
            if grid[i][j]:
                obstacles.append(Obstacle(
                    j * BLOCK_SIZE + OFFSET_X,
                    (j+1) * BLOCK_SIZE + OFFSET_X,
                    i * BLOCK_SIZE + OFFSET_Y,
                    (i+1) * BLOCK_SIZE + OFFSET_Y
                ))

def placeCabbage(i, j):
    point = pointFromGrid(i, j)
    cabbages.append(Cabbage(point[0], point[1]))

DX = [0, 1, 0, -1]
DY = [1, 0, -1, 0]

def generateMaze(grid, x, y):
    grid[x][y] = False
    directions = [0, 1, 2, 3]
    random.shuffle(directions)
    for direction in directions:
        newX = x + DX[direction]*2
        newY = y + DY[direction]*2
        if newX < 0 or newX >= ROWS or newY < 0 or newY >= COLUMNS:
            continue
        if not grid[newX][newY]:
            continue
        grid[x+DX[direction]][y+DY[direction]] = False
        generateMaze(grid, newX, newY)


def createLevel():
    grid = [[True for _ in range(0, COLUMNS)] for _ in range(0, ROWS)]

    grid[0][1] = False
    generateMaze(grid, 1, 1)

    for i in range(ROWS):
        for j in range(COLUMNS):
            if not grid[i][j] and random.random() < 0.25:
                placeCabbage(i, j)

    createLevelFromGrid(grid)

def handleCollisions(player: Player, vx, vy):
    for obstacle in obstacles:
        newVx = obstacle.limitX(player, vx)
        if vx > 0:
            vx = min(vx, newVx)
        else:
            vx = max(vx, newVx)

        newVy = obstacle.limitY(player, vy)
        if vy > 0:
            vy = min(vy, newVy)
        else:
            vy = max(vy, newVy)
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
