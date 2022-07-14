import operator


class Expression:
    
    def __init__(self, expr, symbolic=False):
        self.expr = expr
        self.symbolic = symbolic

    def _basic_operation(self, x, op, reverse=False):
        operands = {"a": "", "b": ""}

    def __mul__(self, x):
        return self._basic_operation(x, operator.mul)

    def __rmul__(self, x):
        return self.__mul__(x)

    def __add__(self, x):
        return self._basic_operation(x, operator.add)

    def __sub__(self, x):
        return self._basic_operation(x, operator.sub)

    def __rsub__(self, x):
        return self.__sub__(x) * -1

    def __truediv__(self, x):
        return self._basic_operation(x, operator.truediv)

    def __rtruediv__(self, x):
        return self._basic_operation(x, operator.truediv, reverse=True)

    def __repr__(self):
        if not self.symbolic:
            return str(self.expr)
        return "".join([str(elem) for elem in self.expr])


class ComplexSymbol:
    
    def __init__(self, letter):
        self.letter = letter
        self.coef = 1
        self.expr = Expression([1, self.letter], symbolic=True)

    def __mul__(self, x):
        return Expression(x) * self

    def __rmul__(self, x):
        return Expression(x) * self

    def __repr__(self):
        return repr(self.expr)


i = ComplexSymbol("i")
i = 2 * i
print(i)
