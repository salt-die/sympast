__all__ = "Expr", "BinOp", "Var"

from dataclasses import dataclass

_EXPR_BODY = """
def __{0}__(self, other):
    return BinOp('{1}', self, other)
def __r{0}__(self, other):
    return BinOp('{1}', other, self)
"""
_SYMBOL_MAP = dict(add="+", sub="-", mul="*", truediv="/")

@dataclass(frozen=True, slots=True)
class Expr:
    for _item in _SYMBOL_MAP.items():
        exec(_EXPR_BODY.format(*_item))
    del _item

@dataclass(frozen=True, slots=True)
class BinOp(Expr):
    op: str
    lhs: Expr
    rhs: Expr

    def __str__(self):
        lhs = f"({self.lhs})" if isinstance(self.lhs, BinOp) else f"{self.lhs}"
        rhs = f"({self.rhs})" if isinstance(self.rhs, BinOp) else f"{self.rhs}"
        return f"{lhs} {self.op} {rhs}"

@dataclass(frozen=True, slots=True)
class Var(Expr):
    name: str

    def __str__(self):
        return self.name
