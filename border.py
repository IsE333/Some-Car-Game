from drawable import Drawable
import pygame

class Border(Drawable):
    def __init__(self, surface, color, start_pos, end_pos, circleColor) -> None:
        super().__init__(surface, color)
        self.startPos = start_pos
        self.endPos = end_pos
        self.cColor = circleColor
    def draw(self):
        pygame.draw.line(self.surface, self.color, self.startPos, self.endPos)
        pygame.draw.circle(self.surface,self.cColor,self.startPos,4)
        pygame.draw.circle(self.surface,self.cColor,((self.startPos[0]+self.endPos[0])/2,(self.startPos[1]+self.endPos[1])/2),4)
        pygame.draw.circle(self.surface,self.cColor,self.endPos,4)