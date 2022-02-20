import math
from pydoc import ispackage
from rectangle import Rectangle
from textRenderer import TextRenderer
import pygame
class Car(Rectangle):
    def __init__(self, surface, xPos:int, yPos:int, maxSpeed:float, rot:float, isPlaced:bool) -> None:
        super().__init__(surface, (0,192,0), xPos, yPos, 32, 64, rot)
        self.maxSpeed, self.speed = maxSpeed, 0.0
        self.rotation = 0.0
        self.speedMeter = TextRenderer(self.surface,(32,255,32), str(self.speed)[0:6], 32, pygame.display.get_window_size()[0]-110, pygame.display.get_window_size()[1]-50)
        self.isPlaced = isPlaced
        self.range=256
        self.up = False
        self.down = False
        self.left = False
        self.right = False
    def update(self):
        free = not (self.up or self.down)
        if self.up and self.speed<self.maxSpeed:
            self.speed += 0.05 + (self.speed < 0)*0.05
        elif self.down and self.speed>-self.maxSpeed/3:
            self.speed -= 0.05 + (self.speed > 0)*0.10 
        elif abs(self.speed)>0.5 and free:
            self.speed *= 0.99
        elif abs(self.speed)>0.01 and free:
            self.speed *= 0.8
        elif free: 
            self.speed = 0
        if self.left and not self.right:
            self.rotation -= 3.1416*self.speed/360
        if self.right and not self.left:
            self.rotation += 3.1416*self.speed/360

        self.yPos -= math.cos(self.rotation)*self.speed
        self.xPos += math.sin(self.rotation)*self.speed
        self.speedMeter.text = str(self.speed)[0:6]
        self.speedMeter.draw()
    def drawRays(self, lines):
        for L in lines:
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
                    break
                pygame.draw.circle(self.surface,self.color,(rayX[points],rayY[points]),1)
        pygame.draw.line(self.surface, self.color, (self.xPos+self.xSize/2,self.yPos+self.ySize/2), self.rayEndPoint(self.rotate(self.xPos+self.xSize/2,self.yPos+self.ySize/2,self.xPos+self.xSize/2+self.range,self.yPos+self.ySize/2,self.rotation)))
        pygame.draw.line(self.surface, self.color, (self.xPos+self.xSize/2,self.yPos+self.ySize/2), self.rotate(self.xPos+self.xSize/2,self.yPos+self.ySize/2,self.xPos+self.xSize/2+(self.range*math.sqrt(2)/2),self.yPos+self.ySize/2-(self.range*math.sqrt(2)/2),self.rotation))
        pygame.draw.line(self.surface, self.color, (self.xPos+self.xSize/2,self.yPos+self.ySize/2), self.rotate(self.xPos+self.xSize/2,self.yPos+self.ySize/2,self.xPos+self.xSize/2-self.range,self.yPos+self.ySize/2,self.rotation))
        pygame.draw.line(self.surface, self.color, (self.xPos+self.xSize/2,self.yPos+self.ySize/2), self.rotate(self.xPos+self.xSize/2,self.yPos+self.ySize/2,self.xPos+self.xSize/2-(self.range*math.sqrt(2)/2),self.yPos+self.ySize/2-(self.range*math.sqrt(2)/2),self.rotation))
        pygame.draw.line(self.surface, self.color, (self.xPos+self.xSize/2,self.yPos+self.ySize/2), self.rotate(self.xPos+self.xSize/2,self.yPos+self.ySize/2,self.xPos+self.xSize/2,self.yPos+self.ySize/2+self.range,self.rotation))
        pygame.draw.line(self.surface, self.color, (self.xPos+self.xSize/2,self.yPos+self.ySize/2), self.rotate(self.xPos+self.xSize/2,self.yPos+self.ySize/2,self.xPos+self.xSize/2,self.yPos+self.ySize/2-self.range,self.rotation))
    
    def rayEndPoint(self, endPoint:tuple[int,int]) -> tuple[int,int]:
        
        return endPoint