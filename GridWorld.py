# Ting Yao (ty168)
import pygame
import random
import sys
from AStar import *
from pygame.locals import *
from time import monotonic

BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREEN = (0, 120, 55)
GREY = (220, 220, 220)
DARKGREY = (128, 128, 128)
RED = (255, 45, 45)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
class GridWorld():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Grid World")
        self.clock = pygame.time.Clock()
        self.screen_res = [909,909]
        self.screen = pygame.display.set_mode(self.screen_res)
        self.quit = False
        self.type = "RFA"
        self.initializegrid()
    def initializegrid(self):
        self.grid = Grid(self)
        self.agent = Agent(self.grid, self.grid.start, self.grid.goal, self.type)
        self.grid.random()
        self.run = False
    def loop(self):

        while True:
            self.draw()
            self.clock.tick(60)
            if self.run:
                if self.agent.finished:
                    self.agent.resultpath()
                    self.run = False
                    endtime = monotonic()
                    print("Time Used: %0.6f seconds" % (endtime - starttime))
                elif self.agent.failed:
                    self.run = False
                else:
                    self.agent.astep()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        starttime = monotonic()
                        self.run = not self.run
                    if event.key == K_c:
                        self.grid.clear_path()
                        self.agent = Agent(self.grid, self.grid.start, self.grid.goal, self.type)
                    if event.key == K_r:
                        self.initializegrid()
                    if event.key == K_1:
                        self.grid.clear_path()
                        self.type = "RFA"
                        self.agent.new_plan(self.type)
                    if event.key == K_2:
                        self.grid.clear_path()
                        self.type = "MYRFA"
                        self.agent.new_plan(self.type)
                    if event.key == K_3:
                        self.grid.clear_path()
                        self.type = "RBA"
                        self.agent.new_plan(self.type)
                    if event.key == K_4:
                        self.grid.clear_path()
                        self.type = "RFAG"
                        self.agent.new_plan(self.type)
    def draw(self):
        self.screen.fill(0)
        self.grid.update()
        pygame.display.update()

class Grid:
    def __init__(self, game):
        self.game = game
        self.width = 101
        self.height = 101
        self.nodes = {(i, j):Node(self, (i, j)) for i in range(self.height) for j in range(self.width)}
        self.row_range = 101
        self.col_range = 101
        temp1 = random.randint(1,100)
        temp2 = random.randint(1,100)
        temp3 = random.randint(1,100)
        temp4 = random.randint(1,100)
        self.start = (temp1, temp2)
        self.goal = (temp3, temp4)
    def random(self):
        for node in self.nodes.values():
            node.random_blocked()
    def update(self):
        for node in self.nodes.values():
            node.update()
            node.draw(self.game.screen)
        for i in range(self.width):
            pygame.draw.line(self.game.screen, [100]*3, (9*i, 0), (9*i, 909))
        for i in range(self.height):
            pygame.draw.line(self.game.screen, [100]*3, (0, (9*i)), (909, (9*i)))
    def clear_path(self):
        for node in self.nodes.values():
            if node.checked:
                node.checked = False
            if node.in_path:
                node.in_path = False
            if node.frontier:
                node.frontier = False

class Node():
    def __init__(self, grid, pos):
        self.grid = grid
        self.game = self.grid.game
        self.pos = pos
        self.blit_pos = [self.pos[1]*9, self.pos[0]*9]
        self.color = GREY
        self.image = pygame.Surface((9, 9))
        self.rect = self.image.get_rect(topleft=self.blit_pos)
        self.in_path = False
        self.checked = False
        self.frontier = False
        self.blocked = False
        self.start = False
        self.goal = False
        self.g = 1
        self.h = sys.maxsize
        self.f = sys.maxsize
    def update(self):
        #The order of these lines is important
        if self.blocked:
            self.color = BLACK
        elif self.start:
            self.color = YELLOW
        elif self.goal:
            self.color = RED
        elif self.in_path:
            self.color = GREEN
        elif self.frontier:
            self.color = PURPLE
        elif self.checked:
            self.color = DARKGREY
        else:
            self.color = GREY
    def random_blocked(self):
        temp = random.randrange(1,10)
        if temp < 4 and not self.start and not self.goal:
            self.blocked = True
    def draw(self, screen):
        self.image.fill(self.color)
        screen.blit(self.image, self.rect)

if __name__ == '__main__':
    game = GridWorld()
    game.loop()
