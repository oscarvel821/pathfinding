from math import sqrt

def lerp(A : int, B: int, t : float) -> float:
    return A + (B - A) * t

def euclideanDistance(x1 : int, y1 : int, x2 : int, y2 :int) -> float:
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def manhattanDistance(x1 : int, y1 : int, x2 : int, y2 :int) -> float:
    return abs(x1 - x2) + abs(y1 - y2)