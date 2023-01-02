__all__ = "Expr", "UnOp", "BinOp", "Equation", "Var"

from dataclasses import dataclass
from textwrap import dedent

_BINOPS_SYMBOLS = {
    "add": "+", "sub": "-", "mul": "*", "truediv": "/", "matmul": "@", "floordiv": "//",
    "mod": "%", "pow": "**", "lshift": "<<", "rshift": ">>", "and": "&", "xor": "^", "or": "|",
}
_UNOPS_SYMBOLS = {"neg": "-", "pos": "+", "invert": "~"}
_EQUATION_SYMBOLS = {"lt": "<", "le": "<=", "eq": "==", "ne": "!=", "gt": ">", "ge": ">="}


@dataclass(frozen=True, slots=True)
class Expr:
    for name, symbol in _BINOPS_SYMBOLS.items():
        exec(dedent(
            f"""
            def __{name}__(self, other):
                return BinOp("{symbol}", self, other)
            def __r{name}__(self, other):
                return BinOp("{symbol}", other, self)
            """
        ))
    for name, symbol in _UNOPS_SYMBOLS.items():
        exec(dedent(
            f"""
            def __{name}__(self):
                return UnOp("{symbol}", self)
            """
        ))
    for name, symbol in _EQUATION_SYMBOLS.items():
        exec(dedent(
            f"""
            def __{name}__(self, other):
                return Equation("{symbol}", self, other)
            """
        ))
    del name, symbol


@dataclass(frozen=True, slots=True, eq=False)
class UnOp(Expr):
    symbol: str
    expr: Expr

    def __str__(self):
        expr = f"({self.expr})" if isinstance(self.expr, BinOp) else f"{self.expr}"
        return f"{self.symbol}{expr}"


@dataclass(frozen=True, slots=True, eq=False)
class BinOp(Expr):
    symbol: str
    lhs: Expr
    rhs: Expr

    def __str__(self):
        lhs = f"({self.lhs})" if isinstance(self.lhs, BinOp) else f"{self.lhs}"
        rhs = f"({self.rhs})" if isinstance(self.rhs, BinOp) else f"{self.rhs}"
        return f"{lhs} {self.symbol} {rhs}"


@dataclass(frozen=True, slots=True)
class Equation:  # NOT an expression
    symbol: str
    lhs: Expr
    rhs: Expr

    for name in _BINOPS_SYMBOLS:
        exec(dedent(
            f"""
            def __{name}__(self, other):
                return type(self)(
                    self.symbol,
                    self.lhs.__{name}__(other),
                    self.rhs.__{name}__(other),
                )
            def __r{name}__(self, other):
                return type(self)(
                    self.symbol,
                    self.lhs.__r{name}__(other),
                    self.rhs.__r{name}__(other),
                )
            """
        ))
    for name in _UNOPS_SYMBOLS:
        exec(dedent(
            f"""
            def __{name}__(self):
                return type(self)(self.symbol, self.lhs.__{name}__(), self.rhs.__{name}__())
            """
        ))
    del name

    def __str__(self):
        return f"{self.lhs} {self.symbol} {self.rhs}"


@dataclass(frozen=True, slots=True, eq=False)
class Var(Expr):
    name: str

    def __str__(self):
        return self.name
