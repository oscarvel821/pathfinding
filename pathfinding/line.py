import pygame

class Line:

    ORANGE = (252, 161, 3)
    
    def __init__(self, x1, y1, x2, y2) -> None:
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self, win) -> None:
        pygame.draw.line(win, self.ORANGE, (self.x1, self.y1), (self.x2, self.y2), 3)