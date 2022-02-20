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
        self.rayColor=(192,0,0)
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
    def drawRays(self, lines:list):
        
        pygame.draw.line(self.surface, self.rayColor, (self.xPos+self.xSize/2,self.yPos+self.ySize/2), self.rayEndPoint(self.rotate(self.xPos+self.xSize/2,self.yPos+self.ySize/2,self.xPos+self.xSize/2+self.range,self.yPos+self.ySize/2,self.rotation), lines))
        pygame.draw.line(self.surface, self.rayColor, (self.xPos+self.xSize/2,self.yPos+self.ySize/2), self.rayEndPoint(self.rotate(self.xPos+self.xSize/2,self.yPos+self.ySize/2,self.xPos+self.xSize/2+(self.range*math.sqrt(2)/2),self.yPos+self.ySize/2-(self.range*math.sqrt(2)/2),self.rotation), lines))
        pygame.draw.line(self.surface, self.rayColor, (self.xPos+self.xSize/2,self.yPos+self.ySize/2), self.rayEndPoint(self.rotate(self.xPos+self.xSize/2,self.yPos+self.ySize/2,self.xPos+self.xSize/2-self.range,self.yPos+self.ySize/2,self.rotation), lines))
        pygame.draw.line(self.surface, self.rayColor, (self.xPos+self.xSize/2,self.yPos+self.ySize/2), self.rayEndPoint(self.rotate(self.xPos+self.xSize/2,self.yPos+self.ySize/2,self.xPos+self.xSize/2-(self.range*math.sqrt(2)/2),self.yPos+self.ySize/2-(self.range*math.sqrt(2)/2),self.rotation), lines))
        pygame.draw.line(self.surface, self.rayColor, (self.xPos+self.xSize/2,self.yPos+self.ySize/2), self.rayEndPoint(self.rotate(self.xPos+self.xSize/2,self.yPos+self.ySize/2,self.xPos+self.xSize/2,self.yPos+self.ySize/2+self.range,self.rotation), lines))
        pygame.draw.line(self.surface, self.rayColor, (self.xPos+self.xSize/2,self.yPos+self.ySize/2), self.rayEndPoint(self.rotate(self.xPos+self.xSize/2,self.yPos+self.ySize/2,self.xPos+self.xSize/2,self.yPos+self.ySize/2-self.range,self.rotation),lines))
    
    def rayEndPoint(self, endPoint:tuple[int,int], lines:list) -> tuple[int,int]:
        x, y = endPoint
        line1=((self.xPos+self.xSize/2, self.yPos+self.ySize/2),(endPoint[0], endPoint[1]))
        line2=((0,0),(0,0))
        for L in lines:
            line2 = ((L.startPos[0], L.startPos[1]), (L.endPos[0], L.endPos[1]))
            xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
            ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

            def det(a, b):
                return a[0] * b[1] - a[1] * b[0]

            div = det(xdiff, ydiff)
            if div == 0:
                pass
            else:
                d = (det(*line1), det(*line2))
                nx = det(d, xdiff) / div
                ny = det(d, ydiff) / div
                if self.dist((nx,ny),line1[0]) < self.dist((x,y),line1[0]):
                    x,y = nx,ny
        
        distX, distY = x - line1[0][0], y - line1[0][1]
        dist = math.sqrt(distX**2+distY**2)

        isBetweenPoints = (line2[1][0]<x<line2[0][0] or line2[1][0]>x>line2[0][0])
        
        isInRightDirection=(((x>line1[0][0] and line1[1][0]>line1[0][0])or(x<line1[0][0] and line1[1][0]<line1[0][0]))or((y>line1[0][1] and line1[1][1]>line1[0][1])or(y<line1[0][1] and line1[1][1]<line1[0][1])))
        #isInRightDirection=((x>line1[1][0]>line1[0][0]or x<line1[1][0]<line1[0][0])or(y>line1[1][1]>line1[0][1]or y<line1[1][1]<line1[0][1]))
        if dist>self.range or not isInRightDirection or not isBetweenPoints:
            return endPoint
        print(x,y)
        return x, y
    def dist(self,a:tuple[int,int],b:tuple[int,int]):
        return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

