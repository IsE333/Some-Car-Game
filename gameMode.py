from enum import Enum
import pygame
from button import Button
from textRenderer import TextRenderer
class GameModes(Enum):
    BUILD = 0
    CAR = 1
    RUN = 2
class GameMode():
    def __init__(self, mode, surface) -> None:
        
        self.mode = mode
        self.surface = surface
        self.bttn1 = Button(self.surface,(64,128,255),10,10,200,50,"Lines",20,0)
        self.bttn2 = Button(self.surface,(64,128,255),220,10,200,50,"Car",20,0)
        self.currentModeText = TextRenderer(self.surface,(255,255,255),"Lines",30, 20, pygame.display.get_window_size()[1]-50)
        self.runText = TextRenderer(self.surface,(255,255,255),"Press R to Run", 16, 10, 60)
    def change(self, newM):
        self.mode = newM
    def runButton(self):
        if self.mode == GameModes.RUN: 
            self.change(GameModes.BUILD)
        else: 
            self.change(GameModes.RUN)
    def drawButtonsAndCurrentMode(self,clickCheck):
        if self.mode == GameModes.BUILD or self.mode == GameModes.CAR:
            if self.bttn1.drawAndUpdate(clickCheck): self.change(GameModes.BUILD)
            if self.bttn2.drawAndUpdate(clickCheck): self.change(GameModes.CAR)
            if self.mode == GameModes.BUILD:
                self.currentModeText.text = "Lines"
            else:
                self.currentModeText.text = "Car"
            self.runText.draw()
        else:
            self.currentModeText.text = "Running"
        self.currentModeText.draw()