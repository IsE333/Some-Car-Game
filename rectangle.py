import drawable
import pygame
import numpy
class Rectangle(drawable.Drawable):
    def __init__(self, surface, color, bgColor, xPos, yPos, xSize, ySize, rot) -> None:
        super().__init__(surface, color)
        self.xPos, self.yPos, self.xSize, self.ySize = xPos, yPos, xSize, ySize
        self.bgColor = bgColor
        self.rotation = rot
    def draw(self):
        midX,midY = self.xPos + self.xSize/2, self.yPos + self.ySize/2

        p1x,p1y = self.rotate(midX,midY,self.xPos, self.yPos, self.rotation)
        p2x,p2y= self.rotate(midX,midY,self.xPos+self.xSize, self.yPos, self.rotation)
        p3x,p3y= self.rotate(midX,midY,self.xPos+self.xSize, self.yPos+self.ySize, self.rotation)
        p4x,p4y= self.rotate(midX,midY,self.xPos, self.yPos+self.ySize, self.rotation)
        
        pygame.draw.polygon(self.surface, self.bgColor, [(p1x,p1y),(p2x,p2y),(p3x,p3y),(p4x,p4y)])
        pygame.draw.polygon(self.surface, (self.color[0]*2,self.color[1]/2,self.color[2]/2), [(p1x,p1y),(p2x,p2y),(p3x,p3y),(p4x,p4y)], 1)
    
    def rotate(self, ox, oy, px, py, angle):
        qx = ox + numpy.cos(angle) * (px - ox) - numpy.sin(angle) * (py - oy)
        qy = oy + numpy.sin(angle) * (px - ox) + numpy.cos(angle) * (py - oy)
        return qx, qy
        