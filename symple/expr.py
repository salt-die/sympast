"""
Expressions and relations defined here.
"""
__all__ = "Expr", "UnOp", "BinOp", "Var", "Relation"

from dataclasses import dataclass
from textwrap import dedent

_BINOPS_SYMBOLS = {
    "add": "+", "sub": "-", "mul": "*", "truediv": "/", "matmul": "@", "floordiv": "//",
    "mod": "%", "pow": "**", "lshift": "<<", "rshift": ">>", "and": "&", "xor": "^", "or": "|",
}
_UNOPS_SYMBOLS = {"neg": "-", "pos": "+", "invert": "~"}
_RELATION_SYMBOLS = {"lt": "<", "le": "<=", "eq": "==", "ne": "!=", "gt": ">", "ge": ">="}


@dataclass(frozen=True, slots=True)
class Expr:
    """
    Abstract base for expressions.
    """
    def __init__(self):
        raise NotImplementedError("Only subclasses of Expr should be instantiated.")

    # Dynamically generate all operators and relations:
    for name, symbol in _BINOPS_SYMBOLS.items():
        exec(dedent(
            f"""
            def __{name}__(self, other):
                return BinOp("{symbol}", self, other)
            def __r{name}__(self, other):
                return BinOp("{symbol}", other, self)

            __{name}__.__doc__ = __r{name}__.__doc__ = '''
            Apply '{symbol}' to an expression.
            '''
            """
        ))
    for name, symbol in _UNOPS_SYMBOLS.items():
        exec(dedent(
            f"""
            def __{name}__(self):
                '''
                Apply '{symbol}' to an expression.
                '''
                return UnOp("{symbol}", self)
            """
        ))
    for name, symbol in _RELATION_SYMBOLS.items():
        exec(dedent(
            f"""
            def __{name}__(self, other):
                '''
                Return the relation `self {symbol} other`.
                '''
                return Relation("{symbol}", self, other)
            """
        ))
    del name, symbol


@dataclass(frozen=True, slots=True, eq=False)
class UnOp(Expr):
    """
    An unary operation.
    """
    symbol: str
    expr: Expr

    def __str__(self):
        expr = f"({self.expr})" if isinstance(self.expr, BinOp) else f"{self.expr}"
        return f"{self.symbol}{expr}"


@dataclass(frozen=True, slots=True, eq=False)
class BinOp(Expr):
    """
    A binary operation.
    """
    symbol: str
    lhs: Expr
    rhs: Expr

    def __str__(self):
        lhs = f"({self.lhs})" if isinstance(self.lhs, BinOp) else f"{self.lhs}"
        rhs = f"({self.rhs})" if isinstance(self.rhs, BinOp) else f"{self.rhs}"
        return f"{lhs} {self.symbol} {rhs}"


@dataclass(frozen=True, slots=True, eq=False)
class Var(Expr):
    """
    A variable.
    """
    name: str

    def __str__(self):
        return self.name


@dataclass(frozen=True, slots=True, eq=False)
class Relation:
    """
    A comparison of two expressions.

    Operations on relations apply to both sides. Comparisons
    of relations not supported. Relations are not expressions.
    """
    symbol: str
    lhs: Expr
    rhs: Expr

    # Dynamically generate all operators and relations:
    for name, symbol in _BINOPS_SYMBOLS.items():
        exec(dedent(
            f"""
            def __{name}__(self, other):
                return type(self)(self.symbol, self.lhs {symbol} other, self.rhs {symbol} other)
            def __r{name}__(self, other):
                return type(self)(self.symbol, other {symbol} self.lhs, other {symbol} self.rhs)

            __{name}__.__doc__ = __r{name}__.__doc__ = '''
            Apply '{symbol}' to both sides of a relation.
            '''
            """
        ))
    for name, symbol in _UNOPS_SYMBOLS.items():
        exec(dedent(
            f"""
            def __{name}__(self):
                '''
                Apply '{symbol}' to both sides of a relation.
                '''
                return type(self)(self.symbol, {symbol}self.lhs, {symbol}self.rhs)
            """
        ))
    for name, symbol in _RELATION_SYMBOLS.items():
        exec(dedent(
            f"""
            def __{name}__(self, other):
                '''
                Comparison with '{symbol}' not supported.
                '''
                raise NotImplementedError("Comparison with '{symbol}' not supported.")
            """
        ))
    del name, symbol

    def __str__(self):
        return f"{self.lhs} {self.symbol} {self.rhs}"
