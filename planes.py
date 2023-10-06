from typing import Iterable, Callable, Any, Optional, Union

Number = Union[int, float, complex]

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
    
    def __repr__(self) -> str:
        return f"{'Point' if self.name is None else str(self.name)}({self.x}, {self.y}, {self.z})"


Vector3D = Point


def overload(*functions: Iterable[Callable]) -> Callable:
    def wrapper(*args: Iterable[Any], **kwargs: dict[Any, Any]) -> Callable:
        # Match correct overload from functions list
        arg_values = list(args) + list(kwargs.values())
        arg_types = [type(arg) for arg in arg_values]
        copy = list(functions)
        copy = list(filter(lambda fn: len(fn.__annotations__) - 1 == len(arg_values), copy))
        for fn in copy:
            annotations = fn.__annotations__
            if annotations.get("return"):
                annotations.pop("return")
            is_match = True
            for expected_type, actual_type in zip(annotations.values(), arg_types):
                if isinstance(expected_type, actual_type):
                    is_match = False
                    break
            if is_match:
                return fn(*args, **kwargs)    
        raise TypeError(
            "no overloaded function matched the given arguments"
        )
    return wrapper


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
    

print(Plane(2, 5, -3, 12))
print(Plane(Point(3, 0, 2, "A"), Point(1, 3, -4, "B"), Point(7, 6, -5, "C")))