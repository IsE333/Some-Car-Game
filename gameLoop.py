import pygame
from border import Border
from gameMode import GameMode
from gameMode import GameModes
from car import Car

class GameLoop():
    def __init__(self) -> None:
        pygame.init()
        self.cw, self.ch = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((self.cw, self.ch), pygame.FULLSCREEN)
        self.lines = []
        self.deletedLines = []
        self.car = Car(self.screen, 0, 0, 6.6, 0, False)
        self.gameMode = GameMode(GameModes.BUILD,self.screen)
        self.drawingLine=False
        self.running = True

    def loop(self):
        pygame.display.set_caption("Game")
        FPS = 60
        fpsClock = pygame.time.Clock()
        
        self.clickRD=False
        while self.running:
            self.clickLU = False
            self.clickLD = False
            
            self.takeInput()
            
            self.screen.fill((0,0,0))
            self.lineUpdate()
            self.carUpdate()
            self.runUpdate()
            self.draw()
            
            fpsClock.tick(FPS)
    def lineUpdate(self):
        if self.clickLD and self.gameMode.mode == GameModes.BUILD:
            self.drawingLine = True
            self.line = Border(self.screen, (255,255,0), pygame.mouse.get_pos(), pygame.mouse.get_pos(), (255,128,128))
        elif self.drawingLine and not self.clickLU and self.gameMode.mode == GameModes.BUILD:
            self.line.endPos = pygame.mouse.get_pos()
            self.line.draw()
        elif self.clickLU and self.drawingLine and self.gameMode.mode == GameModes.BUILD:
            self.drawingLine = False
            self.line.endPos = pygame.mouse.get_pos()
            self.lines.append(self.line)
            self.line.draw()
        if self.clickRD and self.gameMode.mode == GameModes.BUILD:#deletelines :(
            for L in self.lines:
                if L.startPos[0] > L.endPos[0]: 
                    rayX = [x for x in range(L.endPos[0], L.startPos[0]+1)]
                    slope = (L.startPos[1] - L.endPos[1])/((L.startPos[0] - L.endPos[0])+1*(L.startPos[0] == L.endPos[0]))
                    if slope > 0:
                        rayY = [int(x*slope + min(L.endPos[1],L.startPos[1])) for x in range(0, L.startPos[0] - L.endPos[0]+1)]
                    else:
                        rayY = [int(x*slope + max(L.endPos[1],L.startPos[1])) for x in range(0, L.startPos[0] - L.endPos[0]+1)]
                else:
                    rayX = [x for x in range(L.startPos[0], L.endPos[0]+1)]
                    slope = (L.endPos[1] - L.startPos[1])/((L.endPos[0] - L.startPos[0])+1*(L.startPos[0] == L.endPos[0]))
                    if slope > 0:
                        rayY = [int(x*slope + min(L.endPos[1],L.startPos[1])) for x in range(0, L.endPos[0] - L.startPos[0]+1)]
                    else:
                        rayY = [int(x*slope + max(L.endPos[1],L.startPos[1])) for x in range(0, L.endPos[0] - L.startPos[0]+1)]
                for points in range(0,len(rayX)):
                    if rayX[points] in range(pygame.mouse.get_pos()[0]-4,pygame.mouse.get_pos()[0]+5) and rayY[points] in range(pygame.mouse.get_pos()[1]-4, pygame.mouse.get_pos()[1]+5):
                        self.lines.remove(L)
                        break
        if self.gameMode.mode != GameModes.BUILD and self.drawingLine:
            self.drawingLine = False
    def carUpdate(self):
        if self.gameMode.mode == GameModes.CAR and not self.car.isPlaced and not self.clickLD:
            self.car.xPos = pygame.mouse.get_pos()[0] - self.car.xSize/2
            self.car.yPos = pygame.mouse.get_pos()[1] - self.car.ySize/2
            self.car.draw()
        elif self.gameMode.mode == GameModes.CAR and self.clickLD and not self.car.isPlaced:
            self.car.isPlaced = True
            self.car.draw()
        elif self.gameMode.mode == GameModes.CAR and self.clickRD and self.car.isPlaced:
            self.car.isPlaced = False
    def runUpdate(self):
        if self.car.isPlaced and self.gameMode.mode == GameModes.RUN:
            self.car.update()
    def draw(self):
        for L in self.lines:
            L.draw()
        if self.car.isPlaced:
            self.car.draw()
            
        self.gameMode.drawButtonsAndCurrentMode(self.clickLD)
        pygame.display.update()
        pygame.display.flip()
    def takeInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clickLD = True
                if event.button == 3:
                    self.clickRD = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.clickLU = True
                if event.button == 3:
                    self.clickRD=False # this is an expection, it will be false here, it will not be false in next frame unlike others 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_r:#run
                    self.gameMode.runButton()
                if event.key == pygame.K_UP:
                    self.car.up = True
                if event.key == pygame.K_LEFT:
                    self.car.left = True
                if event.key == pygame.K_RIGHT:
                    self.car.right = True
                if event.key == pygame.K_DOWN:
                    self.car.down = True
                if event.key == pygame.K_z:#undo,redo
                    mods = pygame.key.get_mods()
                    if mods & pygame.KMOD_LCTRL and mods & pygame.KMOD_LSHIFT and len(self.deletedLines)>0:
                        self.lines.append(self.deletedLines.pop())
                    elif mods & pygame.KMOD_LCTRL and not mods & pygame.KMOD_LSHIFT and len(self.lines)>0:
                        self.deletedLines.append(self.lines.pop())
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.car.up = False
                if event.key == pygame.K_LEFT:
                    self.car.left = False
                if event.key == pygame.K_RIGHT:
                    self.car.right = False
                if event.key == pygame.K_DOWN:
                    self.car.down = False