from io import StringIO
from utils import *

class Matrix:
    
    def __init__(self, data: Iterable[Number]) -> None:
        self.data = list(data)
        if not self.data:
            raise TypeError(
                "matrix cannot be 0x0"
            )
        self.rows = len(self.data)
        if not isinstance(self.data[0], list):
            self.rows = 1
            self.cols = len(self.data)
        else:
            self.cols = len(self.data[0])
            for row in self.data:
                if len(row) != self.cols:
                    raise TypeError(
                        "invalid matrix shape"
                    )

    def elem(self, i: int, j: int) -> Number:
        if self.rows == 1:
            return self.data[j]
        return self.data[i][j]        

    def row(self, i: int) -> list[Number]:
        return self.data[i]

    def col(self, i: int) -> list[Number]:
        return [self.data[j][i] for j in range(self.rows)]

    def is_row(self) -> bool:
        return self.rows == 1
    
    def is_column(self) -> bool:
        return self.cols == 1
    
    def is_square(self) -> bool:
        return self.rows == self.cols

    def __repr__(self) -> str:
        s = StringIO()
        col_lengths = [max([len(str(elem)) for elem in self.col(i)]) for i in range(self.cols)]
        negatives = [any(map(lambda x: x < 0, self.col(i))) for i in range(self.cols)]
        for i in range(self.rows):
            print("|", end="", file=s)
            for j in range(self.cols):
                str_len = len(str(self.elem(i, j)))
                left_pad = (col_lengths[j] - str_len) // 2
                if self.elem(i, j) >= 0 and negatives[j]:
                    left_pad += 1
                right_pad = col_lengths[j] - str_len - left_pad
                print(" " * left_pad + str(self.elem(i, j)) + " " * right_pad, end=" " if j + 1 != self.cols else "", file=s)
            print("|", file=s)
        return s.getvalue()[:-1]

    def __mul__(self, other: 'Matrix' | Number) -> 'Matrix':
        if isinstance(other, Number):
            return self.multiply_scalar(other)
        return self.multiply_matrix(self, other)
    
    def __pow__(self, exponent: int) -> 'Matrix':
        if not self.is_square():
            raise TypeError(
                "not a square matrix"
            )
        if exponent == 0:
            return Matrix(self.identity().data)
        elif exponent < 0:
            return self.inverse() ** (-exponent)
        m = Matrix([[1, 0], [0, 1]])
        for i in range(exponent):
            m *= self
        return m
    
    def identity(self) -> 'Matrix':
        if not self.is_square():
            raise TypeError(
                "not a square matrix"
            )
        return Matrix([[int(i == j) for j in range(self.cols)] for i in range(self.rows)])
    
    def multiply_matrix(self, m1: 'Matrix', m2: 'Matrix') -> 'Matrix':
        if m1.cols != m2.rows:
            raise TypeError(
                f"cannot multiply matrices of sizes {m1.rows}x{m1.cols} and {m2.rows}x{m2.cols}"
            )
        data = [[0 for j in range(m2.cols)] for i in range(m1.rows)]
        for i in range(m1.rows):
            for j in range(m2.cols):
                data[i][j] = self.dot(m1.row(i), m2.col(j))
        return Matrix(data) 

    def multiply_scalar(self, k: Number) -> 'Matrix':
        return Matrix([
            [self.elem(i, j) * k for j in range(self.cols)] for i in range(self.rows)
        ])

    def det(self) -> Number:
        pass 
    
    def inverse(self) -> 'Matrix':
        augmented = self.augment(self.identity())
        for j in range(self.cols):
            col = self.col(j)
            for i in range(self.rows):
                if not any(col):
                    raise TypeError(
                        "matrix is singular"
                    )
                
        return self

    def augment(self, other: 'Matrix') -> 'Matrix':
        if self.rows != other.rows or self.cols != other.cols:
            raise TypeError(
                "matrices must be square and have the same size to be augmented"
            ) 
        data = self.data.copy()
        for i in range(len(data)):
            data[i].extend(other.row(i))
        return Matrix(data)

    def dot(self, v1: Iterable[Number], v2: Iterable[Number]) -> Number:
        if len(v1) != len(v2):
            raise TypeError(
                f"cannot compute the dot product of vectors of length {len(v1)} and {len(v2)}"
            )
        return sum(i * j for i, j in zip(v1, v2))


m1 = Matrix([
    [1, -1,  2], 
    [2,  0,  3],
    [0,  1, -1]
])
m2 = Matrix([
    [1, -3], 
    [4, 5],
    [3, 0]
])
print(m1.inverse(), sep="\n")
