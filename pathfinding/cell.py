import pygame
from helper import lerp

class Cell:

    WHITE = (255,250,240)
    GREY = (169,169,169)
    GREEN = (60,179,113)
    RED = (255,99,71)
    BLUE = (240,248,255)
    YELLOW = (255,255,195)
    PURPLE = (216,191,216)

    def __init__(self, x: int, y : int, width_offset : int, height_offset : int) -> None:
        self.x = x
        self.y = y
        self.width_offset = width_offset
        self.height_offset = height_offset
        self.count = None
        self.isStartCell = False
        self.isEndCell = False
        self.isWall = False
        self.visited = False
        self.path = False
        self.inQueue = False
        self.alpha = 255
        self.fLocalGoal = float('inf')
        self.fGlobalGoal = float('inf')
        self.hCost = float('inf')
        self.vecNeighbors = []
        self.parent = None

    def draw_text(self, text, font, text_col,screen, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    def draw(self, win : pygame.Surface, font) -> None:
        color = self.WHITE
        if self.isStartCell:
            color = self.GREEN
        elif self.isEndCell:
            color = self.RED
        elif self.isWall:
            color = self.GREY
        elif self.visited:
            color = self.BLUE
        elif self.path:
            color = self.YELLOW
        elif self.inQueue:
            color = self.PURPLE

        # pygame.draw.rect(win, color, (self.x, self.y, self.width_offset - 2, self.height_offset - 2))

        s = pygame.Surface((self.width_offset - 2, self.height_offset - 2))
        s.set_alpha(self.alpha)
        s.fill(color)
        win.blit(s, (self.x, self.y))
        if self.count:
            t = 0.35
            if self.count >= 100:
                t = 0.20
            x = lerp(self.x, self.x + self.width_offset, t)
            y = lerp(self.y, self.y + self.height_offset, t)
            self.draw_text(str(self.count), font, (0,0,0), win, x, y)

    # def updateStatus(self, isWall : bool, visited : bool, path : bool, inQueue : bool) -> None:
    #     self.isWall = isWall
    #     self.visited = visited
    #     self.path = path
    #     self.inQueue = inQueue

    def __lt__(self, other):
        if self.hCost == other.hCost:
            return self.fGlobalGoal < other.fGlobalGoal
        return self.hCost < other.hCost