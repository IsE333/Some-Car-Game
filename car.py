import math
from pydoc import ispackage
from rectangle import Rectangle
from textRenderer import TextRenderer
import pygame
class Car(Rectangle):
    def __init__(self, surface, xPos:int, yPos:int, maxSpeed:float, rot:float, isPlaced:bool) -> None:
        super().__init__(surface, (0,192,0), xPos, yPos, 32, 64, rot)
        self.maxSpeed, self.speed = maxSpeed, 0.0
        self.rotation = 0
        self.speedMeter = TextRenderer(self.surface,(32,255,32), str(self.speed)[0:6], 32, pygame.display.get_window_size()[0]-110, pygame.display.get_window_size()[1]-50)
        self.isPlaced = isPlaced
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