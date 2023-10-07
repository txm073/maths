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

    def set_row(self, i: int, row: list[Number]) -> None:
        if len(row) != self.cols:
            raise TypeError(
                f"row must contain exactly {self.cols} elements"
            )
        self.data[i] = row

    def set_col(self, i: int, col: list[Number]) -> None:
        if len(col) != self.rows:
            raise TypeError(
                f"column must contain exactly {self.rows} elements"
            )
        for r in range(self.rows):
            self.data[r][i] = col[r]

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

    def __mul__(self, other: Union['Matrix', Number]) -> 'Matrix':
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
            return self._ref() ** (-exponent)
        m = Matrix([[1, 0], [0, 1]])
        for _ in range(exponent):
            m *= self
        return m

    def ew_add(self, a: Union[list[Number], Number], b: Union[list[Number], Number]) -> Union[list[Number], Number]:
        if isinstance(a, Number):
            if isinstance(b, Number):
                return a + b
            return [a + elem for elem in b]
        if isinstance(b, Number):
            return [b + elem for elem in a]
        if len(a) != len(b):
            raise TypeError(
                "vectors must be the same length"
            )
        return [i + j for i, j in zip(a, b)]

    def ew_mul(self, a: Union[list[Number], Number], b: Union[list[Number], Number]) -> Union[list[Number], Number]:
        if isinstance(a, Number):
            if isinstance(b, Number):
                return a * b
            return [a * elem for elem in b]
        if isinstance(b, Number):
            return [b * elem for elem in a]
        if len(a) != len(b):
            raise TypeError(
                "vectors must be the same length"
            )
        return [i * j for i, j in zip(a, b)]
    
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

    def det(self, M: 'Matrix') -> Number:
        pass
    
    def inverse(self) -> 'Matrix':
        M = self.copy()
        print(self is M)
        augmented = M.augment(M.identity())
        reduced = M.rref(augmented)
        inverse_matrix = Matrix([reduced.row(i)[M.rows:] for i in range(reduced.rows)])
        return inverse_matrix

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
        return sum(self.ew_mul(v1, v2))

    def copy(self) -> 'Matrix':
        return Matrix(self.data)

    def rref(self, M: 'Matrix') -> 'Matrix':
        # Let's do forward step first.
        # at the end of this for loop, the matrix is in Row-Echelon format.
        for i in range(min(M.rows, M.cols)):
            # every iteration, ignore one more row and column
            for r in range(i, M.rows):
                # find the first row with a nonzero entry in first column
                zero_row = M.elem(r, i) == 0
                if zero_row:
                    continue
                # swap current row with first row
                M.data[i], M.data[r] = M.data[r], M.data[i]
                # add multiples of the new first row to lower rows so lower
                # entries of first column is zero
                first_row_first_col = M.elem(i, i)
                for rr in range(i + 1, M.rows):
                    this_row_first = M.elem(rr, i)
                    scalarMultiple = -1 * this_row_first / first_row_first_col
                    for cc in range(i, M.cols):
                        M.data[rr][cc] += M.data[i][cc] * scalarMultiple
                break
        # Now reduce
        for i in range(min(M.rows, M.cols) - 1, -1, -1):
            # divide last non-zero row by first non-zero entry
            first_elem_col = -1
            first_elem = -1
            for c in range(M.cols):
                if M.elem(i, c) == 0:
                    continue
                if first_elem_col == -1:
                    first_elem_col = c
                    first_elem = M.elem(i, c)
                M.data[i][c] /= first_elem
            # add multiples of this row so all numbers above the leading 1 is zero
            for r in range(i):
                this_row_above = M.elem(r, first_elem_col)
                scalarMultiple = -1 * this_row_above
                for cc in range(M.cols):
                    M.data[r][cc] += M.elem(i, cc) * scalarMultiple
            # disregard this row and continue
        return M

n = Number

m1 = Matrix([
    [n(1), n(-1),  n(2), n(13), n(3), n(-4)], 
    [n(0),  n(0),  n(3), n(8), n(-1),  n(2)],
    [n(3),  n(1), n(-1), n(67), n(-5),  n(-2)],
    [n(5),  n(14), n(-51), n(70), n(35),  n(6)],
    [n(3),  n(21), n(-16), n(17), n(15),  n(31)],
    [n(6),  n(-11), n(11), n(3), n(-1),  n(-3)]
])  
m2 = Matrix([
    [1, -3], 
    [4, 5],
    [3, 0]
])
m3 = Matrix([
    [n(1), n(-1),  n(2), n(13), n(3), n(-4)], 
    [n(0),  n(0),  n(3), n(8), n(-1),  n(2)],
    [n(3),  n(1), n(-1), n(67), n(-5),  n(-2)],
    [n(5),  n(14), n(-51), n(70), n(35),  n(6)],
    [n(3),  n(21), n(-16), n(17), n(15),  n(31)],
    [n(6),  n(-11), n(11), n(3), n(-1),  n(-3)]
])  
