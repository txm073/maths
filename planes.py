from utils import *

class Point:
    
    def __init__(
        self, 
        x: Number, 
        y: Number, 
        z: Number, 
        name: Optional[str] = None, 
        vector: Optional[bool] = False
    ) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.name = name
        
    def __add__(self, p: 'Point') -> 'Point':
        return Point(self.x + p.x, self.y + p.y, self.z + p.z)    
    
    def __sub__(self, p: 'Point') -> 'Point':
        return Point(self.x - p.x, self.y - p.y, self.z - p.z)    
    
    def __eq__(self, p: 'Point') -> bool:
        return self.x == p.x and self.y == p.y and self.z == p.z
    
    def __repr__(self) -> str:
        return f"{'Point' if self.name is None else str(self.name)}({self.x}, {self.y}, {self.z})"


Vector3D = Point


class Plane:
    
    def cartesian(self: 'Plane', x: Number, y: Number, z: Number, d: Number) -> None:
        self.x, self.y, self.z, self.d = x, y, z, d
        self.normal = Vector3D(self.x, self.y, self.z, vector=True)

    def vector(self: 'Plane', p1: Point, p2: Point, p3: Point) -> None:
        l1, l2 = p1 - p2, p1 - p3
        self.normal = self.cross(l1, l2)
        self.x, self.y, self.z = self.normal.x, self.normal.y, self.normal.z
        self.d = self.dot(self.normal, p1)
        
    def cross(self, v1: Vector3D, v2: Vector3D) -> Vector3D:
        return Vector3D(
            x=(v1.y * v2.z - v1.z * v2.y),
            y=-(v1.x * v2.z - v1.z * v2.x),
            z=(v1.y * v2.x - v1.x * v2.y),
            vector=True
        )

    def dot(self, v1: Vector3D, v2: Vector3D) -> Number:
        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

    def __repr__(self) -> str:
        return f"Plane({self.x}x+{self.y}y+{self.z}z={self.d})"
    
    __init__ = overload(cartesian, vector)
    

class Line:

    def __init__(self, p1: Point, p2: Point) -> None:
        self.p1, self.p2 = p1, p2
        self.direction = p1 - p2

    def __repr__(self) -> str:
        return f"Line(({self.p1.x}, {self.p1.y}, {self.p1.z}) + k({self.direction.x}, {self.direction.y}, {self.direction.z}))"
    
    
def is_parallel(l1: Line, l2: Line) -> None:
    k1 = l1.direction.x / l2.direction.x
    k2 = l1.direction.y / l2.direction.y
    k3 = l1.direction.z / l2.direction.z
    return k1 == k2 == k3

def intersection_point(l1: Line, l2: Line) -> Point:
    pass

def shortest_distance(l1: Line, l2: Line) -> Number:
    pass

    
l1 = Line(Point(2, 5, -3), Point(-1, 4, 7))
l2 = Line(Point(0, 0, 0), Point(-6, -2, 20))
pi = Plane(Point(3, 0, 2, "A"), Point(1, 3, -4, "B"), Point(7, 6, -5, "C"))
