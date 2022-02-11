from math import pi
import pygame
from button import Button
from textRenderer import TextRenderer
class GameMode():
    def __init__(self, mode, surface) -> None:
        self.mode = mode #0 build, 1 add car, 2 run
        self.surface = surface
        self.bttn1 = Button(self.surface,(64,128,255),(0,0,0),10,10,200,50,"Lines",20,0)
        self.bttn2 = Button(self.surface,(64,128,255),(0,0,0),220,10,200,50,"Car",20,0)
    def change(self, newM):
        self.mode = newM
    def drawButtonsAndCurrentMode(self,clickCheck):
        if self.mode == 0 or self.mode == 1:
            if self.bttn1.drawAndUpdate(clickCheck): self.change(0)
            if self.bttn2.drawAndUpdate(clickCheck): self.change(1)
            if self.mode == 0:
                currentModeText = TextRenderer(self.surface,(255,255,255),"Lines",30, 20, pygame.display.get_window_size()[1]-50)
                runText = TextRenderer(self.surface,(255,255,255),"Press R to Run", 16, 10, 60)
            else:
                currentModeText = TextRenderer(self.surface,(255,255,255),"Car",30, 20, pygame.display.get_window_size()[1]-50)
                runText = TextRenderer(self.surface,(255,255,255),"Press R to Run", 16, 10, 60)
            runText.draw()
        else:
            currentModeText = TextRenderer(self.surface,(255,255,255),"Running",30, 20, pygame.display.get_window_size()[1]-50)
        currentModeText.draw()