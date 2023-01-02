__all__ = "Expr", "BinOp", "Var"

_SYMBOL_MAP = dict(add="+", sub="-", mul="*", truediv="/")
_EXEC_STR = """
def __{op}__(self, other):
    return BinOp('{symbol}', self, other)
def __r{op}__(self, other):
    return BinOp('{symbol}', other, self)
"""


class Expr:
    for op, symbol in _SYMBOL_MAP.items():
        exec(_EXEC_STR.format(op=op, symbol=symbol))


class BinOp(Expr):
    __match_args__ = "op", "lhs", "rhs"

    def __init__(self, op, lhs, rhs):
        self.op, self.lhs, self.rhs = op, lhs, rhs

    def __str__(self):
        lhs = f"({self.lhs})" if isinstance(self.lhs, BinOp) else f"{self.lhs}"
        rhs = f"({self.rhs})" if isinstance(self.rhs, BinOp) else f"{self.rhs}"
        return f"{lhs} {self.op} {rhs}"


class Var(Expr):
    __match_args__ = "name",

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
