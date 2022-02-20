import math
import drawable
import pygame
class Rectangle(drawable.Drawable):
    def __init__(self, surface, color, xPos, yPos, xSize, ySize, rot:float) -> None:
        super().__init__(surface, color)
        self.xPos, self.yPos, self.xSize, self.ySize = xPos, yPos, xSize, ySize
        self.rotation = rot
    def draw(self):
        midX,midY = self.xPos + self.xSize/2, self.yPos + self.ySize/2

        p1x,p1y = self.rotate(midX,midY,self.xPos, self.yPos, self.rotation)
        p2x,p2y= self.rotate(midX,midY,self.xPos+self.xSize, self.yPos, self.rotation)
        p3x,p3y= self.rotate(midX,midY,self.xPos+self.xSize, self.yPos+self.ySize, self.rotation)
        p4x,p4y= self.rotate(midX,midY,self.xPos, self.yPos+self.ySize, self.rotation)
        
        pygame.draw.line(self.surface, self.color, (p1x,p1y), (p2x,p2y), 2)
        pygame.draw.line(self.surface, self.color, (p2x,p2y), (p3x,p3y), 2)
        pygame.draw.line(self.surface, self.color, (p3x,p3y), (p4x,p4y), 2)
        pygame.draw.line(self.surface, self.color, (p4x,p4y), (p1x,p1y), 2)
    def rotate(self, ox, oy, px, py, angle) -> tuple[int,int]:
        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return int(qx), int(qy)
        