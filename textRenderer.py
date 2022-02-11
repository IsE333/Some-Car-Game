from drawable import Drawable
import pygame
class TextRenderer(Drawable):
    def __init__(self, surface, color, text, size, xPos, yPos) -> None:
        super().__init__(surface, color)
        self.text = text
        self.size = size
        self.pos = xPos, yPos
        pygame.font.init()
    def draw(self):
        myfont = pygame.font.SysFont('Tahoma', self.size)
        textsurface = myfont.render(self.text, True, self.color)
        self.surface.blit(textsurface, self.pos)
