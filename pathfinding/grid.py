import pygame
from cell import Cell
from queue import Queue, PriorityQueue
from pathfinding import bfs, dfs, aStar
from helper import lerp, manhattanDistance, euclideanDistance
from line import Line

class Grid:

    CHECKS_PER_FRAME = 8

    def __init__(self, width : int, height: int, surface_width : int, surface_height : int, width_size : int, height_size, x_origin=0, y_origin=0, bfs_algo=False, dfs_algo=False, aStar_algo=False) -> None:
        self.width = width 
        self.height = height
        self.surface_width = surface_width
        self.surface_height = surface_height
        self.width_size = width_size
        self.height_size = height_size
        self.x_origin = x_origin
        self.y_origin = y_origin
        self.lines = []
        self.nodes = [0] * (self.width * height)
        self.bfs_algo = bfs_algo
        self.dfs_algo = dfs_algo
        self.aStar_algo = aStar_algo
        self.dataStruct = None

        #Initialize Data Structure
        if self.bfs_algo:
            self.dataStruct = Queue()
        elif self.dfs_algo:
            self.dataStruct = []
        elif self.aStar_algo:
            self.dataStruct = PriorityQueue()

        #Initialize grid
        for i in range(self.width):
            for j in range(self.height):
                self.nodes[i + j * self.width] = Cell(self.x_origin + i * self.width_size , self.y_origin + j * self.height_size, self.width_size, self.height_size)

        #Initialize start and end cells
        self.startCell = self.nodes[(self.width // 2) * self.width + 1]
        self.endCell = self.nodes[(self.width // 2) * self.width + (self.width - 2)]

        self.startCell.isStartCell = True
        self.endCell.isEndCell = True

        if self.bfs_algo:
            self.dataStruct.put(self.startCell)
        elif self.dfs_algo:
            self.dataStruct.append(self.startCell)
        elif self.aStar_algo:
            self.startCell.fLocalGoal = 0
            x1 = lerp(self.startCell.x, self.startCell.x + self.startCell.width_offset, 0.5)
            y1 = lerp(self.startCell.y, self.startCell.y + self.startCell.height_offset, 0.5)

            x2 = lerp(self.endCell.x, self.endCell.x + self.endCell.width_offset, 0.5)
            y2 = lerp(self.endCell.y, self.endCell.y + self.endCell.height_offset, 0.5)

            self.startCell.fGlobalGoal = manhattanDistance(self.startCell.x, self.startCell.y, self.endCell.x, self.endCell.y)
            # self.startCell.fGlobalGoal = manhattanDistance(x1, y1, x2, y2)
            self.startCell.hCost = self.startCell.fLocalGoal + self.startCell.fGlobalGoal
            self.dataStruct.put(self.startCell)

        #get neighbor nodes
        for i in range(self.width):
            for j in range(self.height):
                #get north neighbor
                if j > 0:
                    self.nodes[i + j * self.width].vecNeighbors.append(self.nodes[i + (j - 1) * self.width])
                #get south neighbor
                if j < self.height - 1:
                    self.nodes[i + j * self.width].vecNeighbors.append(self.nodes[i + (j + 1) * self.width])
                #get west neighbor
                if i > 0:
                    self.nodes[i + j * self.width].vecNeighbors.append(self.nodes[(i - 1) + j * self.width])
                #get east neighbor
                if i < self.width - 1:
                    self.nodes[i + j * self.width].vecNeighbors.append(self.nodes[(i + 1) + j * self.width])

    def drawGrid(self, win: pygame.Surface, font) -> None:
        for i in range(self.width):
            for j in range(self.height):
                self.nodes[i + j * self.width].draw(win, font)

        for l in self.lines:
            l.draw(win)

    def resetGrid(self) -> None:
        for i in range(self.width):
            for j in range(self.height):
                self.nodes[i + j * self.width].isWall = False
                self.nodes[i + j * self.width].visited = False
                self.nodes[i + j * self.width].path = False
                self.nodes[i + j * self.width].inQueue = False
                self.nodes[i + j * self.width].parent = None
                self.nodes[i + j * self.width].count = None
                self.nodes[i + j * self.width].fLocalGoal = float('inf')
                self.nodes[i + j * self.width].fGlobalGoal = float('inf')
                self.nodes[i + j * self.width].hCost = float('inf')
        
        #Initialize Data Structure
        if self.bfs_algo:
            self.dataStruct = Queue()
        elif self.dfs_algo:
            self.dataStruct = []
        elif self.aStar_algo:
            self.dataStruct = PriorityQueue()

        if self.bfs_algo:
            self.dataStruct.put(self.startCell)
        elif self.dfs_algo:
            self.dataStruct.append(self.startCell)
        elif self.aStar_algo:
            self.startCell.fLocalGoal = 0

            x1 = lerp(self.startCell.x, self.startCell.x + self.startCell.width_offset, 0.5)
            y1 = lerp(self.startCell.y, self.startCell.y + self.startCell.height_offset, 0.5)

            x2 = lerp(self.endCell.x, self.endCell.x + self.endCell.width_offset, 0.5)
            y2 = lerp(self.endCell.y, self.endCell.y + self.endCell.height_offset, 0.5)

            self.startCell.fGlobalGoal = manhattanDistance(self.startCell.x, self.startCell.y, self.endCell.x, self.endCell.y)
            # self.startCell.fGlobalGoal = manhattanDistance(x1, y1, x2, y2)
            self.startCell.hCost = self.startCell.fLocalGoal + self.startCell.fGlobalGoal
            self.dataStruct.put(self.startCell)

        #empty lines path
        self.lines = []

    def resetAnimation(self) -> None:
        #empty lines path
        self.lines = []

        for i in range(self.width):
            for j in range(self.height):
                self.nodes[i + j * self.width].visited = False
                self.nodes[i + j * self.width].path = False
                self.nodes[i + j * self.width].inQueue = False
                self.nodes[i + j * self.width].parent = None
                self.nodes[i + j * self.width].count = None
                self.nodes[i + j * self.width].fLocalGoal = float('inf')
                self.nodes[i + j * self.width].fGlobalGoal = float('inf')
                self.nodes[i + j * self.width].hCost = float('inf')

        #Initialize Data Structure
        if self.bfs_algo:
            self.dataStruct = Queue()
        elif self.dfs_algo:
            self.dataStruct = []
        elif self.aStar_algo:
            self.dataStruct = PriorityQueue()

        if self.bfs_algo:
            self.dataStruct.put(self.startCell)
        elif self.dfs_algo:
            self.dataStruct.append(self.startCell)
        elif self.aStar_algo:
            self.startCell.fLocalGoal = 0

            x1 = lerp(self.startCell.x, self.startCell.x + self.startCell.width_offset, 0.5)
            y1 = lerp(self.startCell.y, self.startCell.y + self.startCell.height_offset, 0.5)

            x2 = lerp(self.endCell.x, self.endCell.x + self.endCell.width_offset, 0.5)
            y2 = lerp(self.endCell.y, self.endCell.y + self.endCell.height_offset, 0.5)

            self.startCell.fGlobalGoal = manhattanDistance(self.startCell.x, self.startCell.y, self.endCell.x, self.endCell.y)
            # self.startCell.fGlobalGoal = manhattanDistance(x1, y1, x2, y2)
            self.startCell.hCost = self.startCell.fLocalGoal + self.startCell.fGlobalGoal
            self.dataStruct.put(self.startCell)

    def toggle_wall(self, position: tuple, prev_cell : Cell) -> Cell and int:
        if self.validPosition(position):
            x, y = position
            for i in range(self.width):
                for j in range(self.height):
                    cell_x = self.nodes[i + j * self.width].x
                    cell_y = self.nodes[i + j * self.width].y

                    if (x > cell_x and x < cell_x + self.width_size) and (y > cell_y and y < cell_y + self.height_size) and not self.nodes[i + j * self.width].isStartCell and not self.nodes[i + j * self.width].isEndCell and self.nodes[i + j * self.width] != prev_cell:
                        self.nodes[i + j * self.width].isWall = not self.nodes[i + j * self.width].isWall
                        return self.nodes[i + j * self.width], i + j * self.width
                    
        return prev_cell, None
    
    def setWall(self, index : int):
        if index:
            self.nodes[index].isWall = not self.nodes[index].isWall
    
    def setStartCell(self, index : int):
        if index:
            self.startCell.isStartCell = False
            self.startCell = self.nodes[index - 1]
            self.startCell.isStartCell = True
            self.resetAnimation()

    def setEndCell(self, index : int):
        if index:
            self.endCell.isEndCell = False
            self.endCell = self.nodes[index - 1]
            self.endCell.isEndCell = True
            self.resetAnimation()
    
    def moveStartCell(self, position : tuple) -> bool and int:
        if self.validPosition(position):
            x, y = position
            for i in range(self.width):
                for j in range(self.height):
                    cell_x = self.nodes[i + j * self.width].x
                    cell_y = self.nodes[i + j * self.width].y

                    if (x > cell_x and x < cell_x + self.width_size) and (y > cell_y and y < cell_y + self.height_size) and not self.nodes[i + j * self.width].isEndCell and not self.nodes[i + j * self.width].isWall:
                        self.startCell.isStartCell = False
                        self.startCell = self.nodes[i + j * self.width]
                        self.startCell.isStartCell = True
                        self.resetAnimation()
                        return True, (i + j * self.width) + 1
        return False, None

    def moveEndCell(self, position : tuple) -> bool and int:
        if self.validPosition(position):
            x, y = position
            for i in range(self.width):
                for j in range(self.height):
                    cell_x = self.nodes[i + j * self.width].x
                    cell_y = self.nodes[i + j * self.width].y

                    if (x > cell_x and x < cell_x + self.width_size) and (y > cell_y and y < cell_y + self.height_size) and not self.nodes[i + j * self.width].isStartCell and not self.nodes[i + j * self.width].isWall:
                        self.endCell.isEndCell = False
                        self.endCell = self.nodes[i + j * self.width]
                        self.endCell.isEndCell = True
                        self.resetAnimation()
                        return True, (i + j * self.width) + 1
        return False, None
    
    def validPosition(self, position: tuple) -> bool:
        x, y = position

        # if (x > self.x_origin and x < self.width * self.width_size) and (y > self.y_origin and y < self.height * self.height_size):
        #     return True
        if (x > self.x_origin and x < self.x_origin + self.surface_width) and (y > self.y_origin and y < self.y_origin + self.surface_height):
            return True
        return False
        
    def solveMap(self) -> bool:
        done = False
        if self.bfs_algo:
            done = bfs(self.startCell, self.endCell, self.nodes, self.dataStruct, self.width, self.height, self.CHECKS_PER_FRAME)
        elif self.dfs_algo:
            done = dfs(self.startCell, self.endCell, self.nodes, self.dataStruct, self.width, self.height, self.CHECKS_PER_FRAME)
        elif self.aStar_algo:
            done = aStar(self.startCell, self.endCell, self.nodes, self.dataStruct, self.width, self.height, self.CHECKS_PER_FRAME)

        #change the cell to in queue status
        if self.dfs_algo:
            for i in range(len(self.dataStruct)):
                self.dataStruct[i].inQueue = True
        elif self.bfs_algo:
            for item in self.dataStruct.queue:
                item.inQueue = True
        elif self.aStar_algo:
            for item in self.dataStruct.queue:
                item.inQueue = True


        if done and self.endCell.parent:
            # length = 0
            # current = self.endCell

            # while current:
            #     length += 1
            #     current = current.parent

            # count = length - 2

            current = self.endCell.parent

            while current.parent:
                # alpha = count / length * 255
                # current.alpha = alpha
                # current.count = count
                current.path = True
                current.visited = False
                current = current.parent
                # count -= 1
            
            current = self.endCell.parent

            while current.parent.parent:
                x1 = lerp(current.x, current.x + current.width_offset, 0.5)
                y1 = lerp(current.y, current.y + current.height_offset, 0.5)
                x2 = lerp(current.parent.x, current.parent.x + current.parent.width_offset, 0.5)
                y2 = lerp(current.parent.y, current.parent.y + current.parent.height_offset, 0.5)
                self.lines.append(Line(x1, y1, x2, y2))
                current = current.parent
        
        return done
    
        
