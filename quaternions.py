import sympy
import numpy as np


class ComplexSymbol(sympy.Symbol):

    def __mul__(self, x):
        if isinstance(x, ComplexSymbol):
            return _table[self.name][x.name]
        return super(ComplexSymbol, self).__mul__(x)

    def __rmul__(self, x):
        if isinstance(x, ComplexSymbol):
            return _table[x.name][self.name]
        return super(ComplexSymbol, self).__rmul__(x)


_table = {
    "i": {"i": -1, "j": ComplexSymbol("k"), "k": -ComplexSymbol("j")},
    "j": {"i": -ComplexSymbol("k"), "j": -1, "k": ComplexSymbol("i")},
    "k": {"i": ComplexSymbol("j"), "j": -ComplexSymbol("i"), "k": -1}
}

i = ComplexSymbol("i")
j = ComplexSymbol("j")
k = ComplexSymbol("k")

def multiply(p, q):
    n = sympy.expand(p * q)
    parts = []
    for key, val in n.as_coefficients_dict().items():
        if str(key).replace(" ", "") in ("i**2", "j**2", "k**2"):
            parts.append((-1, val))
        elif isinstance(key, sympy.core.mul.Mul):
            operands = str(key).split("*")
            parts.append((_table[operands[0]][operands[1]], val))
    result = 0
    for part in parts:
        result += (part[0] * part[1])
    return result

def transform(point, angle, axis):
    div = np.sqrt(sum([x ** 2 for x in axis]))
    axis = axis / div * np.sin(angle)
    angle = np.radians(angle / 2)
    a = np.cos(angle)
    b, c, d = axis.tolist()
    q = a + b * i + c * j + d * k
    inverse = a - b * i - c * j - d * k

    p = point[0] * i + point[1] * j + point[2] * k
    return multiply(multiply(q, p), inverse)

angle = 120
axis_vector = np.array([1, 1, 1])
point = np.array([1, 1, 1])
n = transform(point, angle, axis_vector)
original = transform(point, 360, axis_vector)
print(n)
print(original)