from asyncio.windows_events import NULL
from re import X
import pygame
from border import Border
from gameMode import GameMode
from rectangle import Rectangle
from car import Car

class GameLoop():
    def __init__(self) -> None:
        pygame.init()
        self.cw, self.ch = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.w, self.h = self.cw,self.ch
        if self.cw/self.ch > 32/30: self.w,self.h= self.ch*32/30,self.ch
        if self.cw/self.ch < 32/30: self.w,self.h= self.cw*30/32,self.cw
        self.screen = pygame.display.set_mode((self.cw, self.ch), pygame.FULLSCREEN)
        self.lines = [] 
        self.car = 0
    def loop(self):
        pygame.display.set_caption("Game")
        FPS = 60
        fpsClock = pygame.time.Clock()

        backGround = Rectangle(self.screen,(0,0,0),(0,0,0),0,0,pygame.display.get_window_size()[0],pygame.display.get_window_size()[1], 0)
        gameMode = GameMode(0,self.screen)

        drawingLine=False
        isThereACar = False
        carButtons = [False for _ in range(0,4)] # up, left, right, down
        oldMousePosition=[0,0]
        deletedLines = []
        running = True
        clickRD=False
        while running:
            clickLU = False
            clickLD = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                #if pygame.mouse.get_pressed()[0]:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        clickLD = True
                    if event.button == 3:
                        clickRD = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        clickLU = True
                    if event.button == 3:
                        clickRD=False # this is an expection, it will be false here, it will not be false in next frame unlike others 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_r:#run
                        if gameMode.mode == 2: gameMode.change(0)
                        else: gameMode.change(2)
                    if event.key == pygame.K_UP:
                        carButtons[0] =True
                    if event.key == pygame.K_LEFT:
                        carButtons[1] =True
                    if event.key == pygame.K_RIGHT:
                        carButtons[2] =True
                    if event.key == pygame.K_DOWN:
                        carButtons[3] =True
                    if event.key == pygame.K_z:#undo,redo
                        mods = pygame.key.get_mods()
                        if mods & pygame.KMOD_LCTRL and mods & pygame.KMOD_LSHIFT and len(deletedLines)>0:
                            self.lines.append(deletedLines.pop())
                        elif mods & pygame.KMOD_LCTRL and not mods & pygame.KMOD_LSHIFT and len(self.lines)>0:
                            deletedLines.append(self.lines.pop())
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        carButtons[0] =False
                    if event.key == pygame.K_LEFT:
                        carButtons[1] =False
                    if event.key == pygame.K_RIGHT:
                        carButtons[2] =False
                    if event.key == pygame.K_DOWN:
                        carButtons[3] =False
            
            #LineMode
            if clickLD and gameMode.mode == 0:
                drawingLine = True
                oldMousePosition = pygame.mouse.get_pos()
            elif drawingLine and not clickLU and gameMode.mode == 0:
                line = Border(self.screen, (255,255,0), oldMousePosition, pygame.mouse.get_pos(), (255,128,128))
                line.draw()
            elif clickLU and drawingLine and gameMode.mode == 0:
                drawingLine = False
                line = Border(self.screen, (255,255,0), oldMousePosition, pygame.mouse.get_pos(), (255,128,128))
                self.lines.append(line)
                line.draw()
            if clickRD and gameMode.mode == 0:#deletelines :(
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
            if gameMode.mode != 0 and drawingLine:
                drawingLine = False
            #CarMode
            if gameMode.mode == 1 and not isThereACar and not clickLD:
                car = Car(self.screen,(0,255,0),(0,0,0),pygame.mouse.get_pos()[0]-16,pygame.mouse.get_pos()[1]-32, 32, 64, 13, 0)
                car.draw()
            elif gameMode.mode == 1 and clickLD and not isThereACar:
                isThereACar = True
                self.car = car
                car = NULL
            elif gameMode.mode ==1 and clickRD and isThereACar:
                isThereACar=False
                self.car=NULL
            #RunMode
            if isThereACar and gameMode.mode == 2:
                self.car.update(carButtons)

            for L in self.lines:
                L.draw()
            if isThereACar:
                self.car.draw()
            gameMode.drawButtonsAndCurrentMode(clickLD)
            pygame.display.flip()
            pygame.display.update()
            fpsClock.tick(FPS)
            backGround.draw() #this will be first rendered after waiting