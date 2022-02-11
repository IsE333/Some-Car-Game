import math
from rectangle import Rectangle
from textRenderer import TextRenderer
import pygame
class Car(Rectangle):
    def __init__(self, surface, color, bgColor, xPos, yPos, xSize, ySize, maxSpeed, rot) -> None:
        super().__init__(surface, color, bgColor, xPos, yPos, xSize, ySize, rot)
        self.maxSpeed, self.speed = maxSpeed, 0.0
        self.rotation = 0
    def update(self, buttons):
        free = not (buttons[0] or buttons[1])
        if buttons[0] and self.speed<self.maxSpeed:
            self.speed += 0.16
        elif buttons[3] and self.speed>-self.maxSpeed/3:
            self.speed -= 0.16
        elif abs(self.speed)>0.5 and free:
            self.speed *= 0.99
        elif abs(self.speed)>0.01 and free:
            self.speed *= 0.8
        elif free: 
            self.speed = 0
        if buttons[1] and not buttons[2]:
            self.rotation -= 3.1416*self.speed/360
        if buttons[2] and not buttons[1]:
            self.rotation += 3.1416*self.speed/360

        self.yPos -= math.cos(self.rotation)*self.speed
        self.xPos += math.sin(self.rotation)*self.speed
        speedMeter = TextRenderer(self.surface,(32,255,32), str(self.speed)[0:6], 32, pygame.display.get_window_size()[0]-110, pygame.display.get_window_size()[1]-50)
        speedMeter.draw()