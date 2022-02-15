from rectangle import Rectangle
from textRenderer import TextRenderer
import pygame
class Button(Rectangle):
    def __init__(self, surface, color, xPos, yPos, xSize, ySize, text, textSize, rot) -> None:
        super().__init__(surface, color, xPos, yPos, xSize, ySize, rot)
        self.text, self.textSize = text, textSize
        self.textRenderer = TextRenderer(self.surface, self.color, self.text, self.textSize, self.xPos + 10, self.yPos + 10)
    def drawAndUpdate(self,isClicked):
        if self.xPos < pygame.mouse.get_pos()[0] < self.xPos + self.xSize and self.yPos < pygame.mouse.get_pos()[1] < self.yPos + self.ySize:
            self.color = (64*(not isClicked),255*(not isClicked),255*(not isClicked))
            super().draw() #border
            self.textRenderer.draw() #text
            if isClicked: return True
        else:
            self.color = (64,128,255)
            super().draw() #border
            self.textRenderer.draw() #text
        return False