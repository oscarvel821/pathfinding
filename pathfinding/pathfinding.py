from cell import Cell
from queue import Queue, PriorityQueue
from helper import euclideanDistance, manhattanDistance, lerp

def bfs(StartNode : Cell, EndNode : Cell, nodes : list[Cell], q : Queue, gridWidth : int, gridHeight : int, checks_per_frame : int) -> bool:
    
    for i in range(checks_per_frame):
        if q.empty():
            print("BFS Done : Path Not Found")
            return True
        
        c = q.get()

        if c.visited:
            continue

        if c == EndNode:
            print("BFS Done : Path Found")
            q = Queue()
            return True
        
        for node in c.vecNeighbors:
            if not node.visited and not node.isWall and not node.isStartCell:
                node.parent = c
                q.put(node)

        c.visited = True
    
    return False

def dfs(StartNode : Cell, EndNode : Cell, nodes : list[Cell], stack : list, gridWidth : int, gridHeight : int, checks_per_frame : int) -> bool:

    for i in range(checks_per_frame):
        if not stack:
            print("DFS Done : Path Not Found")
            return True
        
        c = stack.pop()

        if c.visited:
            continue

        if c == EndNode:
            print("DFS Done : Path Found")
            stack = []
            return True
        
        for node in c.vecNeighbors:
            if not node.visited and not node.isWall and not node.isStartCell:
                node.parent = c
                stack.append(node)

        c.visited = True
    
    return False

def aStar(StartNode : Cell, EndNode : Cell, nodes : list[Cell], pq : PriorityQueue, gridWidth : int, gridHeight : int, checks_per_frame : int) -> bool:
    
    for i in range(checks_per_frame):

        if pq.empty():
            print("A Star Done : Path Not Found")
            return True
        
        c = pq.get()

        # if c.visited:
        #     continue

        if c == EndNode:
            print("A Star Done : Path Found")
            q = PriorityQueue()
            return True
        
        #x and y position of the current node
        x1 = lerp(c.x, c.x + c.width_offset, 0.5)
        y1 = lerp(c.y, c.y + c.height_offset, 0.5)

        #x and y position of the end node
        x3 = lerp(EndNode.x, EndNode.x + EndNode.width_offset, 0.5)
        y3 = lerp(EndNode.y, EndNode.y + EndNode.height_offset, 0.5)
        
        for node in c.vecNeighbors:
            if not node.visited and not node.isWall and not node.isStartCell:
                x2 = lerp(node.x, node.x + node.width_offset, 0.5)
                y2 = lerp(node.y, node.y + node.height_offset, 0.5)
                newLocalGoal = manhattanDistance(c.x, c.y, node.x, node.y) + c.fLocalGoal
                # newLocalGoal = manhattanDistance(x1, y1, x2, y2) + c.fLocalGoal
                if newLocalGoal < node.fLocalGoal:
                    node.fLocalGoal = newLocalGoal
                    node.fGlobalGoal = manhattanDistance(node.x, node.y, EndNode.x, EndNode.y)
                    # node.fGlobalGoal = manhattanDistance(x2, y2, x3, y3)
                    node.hCost = node.fLocalGoal + node.fGlobalGoal
                    node.parent = c
                    pq.put(node)

        c.visited = True
    
    return False