"""
Expressions and relations.
"""
__all__ = "Expr", "UnOp", "BinOp", "Var", "Relation"

from abc import ABC, abstractmethod
from dataclasses import dataclass
from numbers import Rational
from typing import Self


@dataclass(frozen=True, slots=True, init=False)
class Expr(ABC):
    """
    Abstract base for arithemetic expressions.
    """
    @abstractmethod
    def __init__(self):
        ...

    def __add__(self, other: Self | Rational) -> "BinOp":
        """
        Add two expressions.
        """
        return BinOp("+", self, other)

    def __radd__(self, other: Self | Rational) -> "BinOp":
        """
        Add two expressions.
        """
        return BinOp("+", other, self)

    def __sub__(self, other: Self | Rational) -> "BinOp":
        """
        Subtract two expressions.
        """
        return BinOp("-", self, other)

    def __rsub__(self, other: Self | Rational) -> "BinOp":
        """
        Subtract two expressions.
        """
        return BinOp("-", other, self)

    def __mul__(self, other: Self | Rational) -> "BinOp":
        """
        Multiply two expressions.
        """
        return BinOp("*", self, other)

    def __rmul__(self, other: Self | Rational) -> "BinOp":
        """
        Multiply two expressions.
        """
        return BinOp("*", other, self)

    def __truediv__(self, other: Self | Rational) -> "BinOp":
        """
        Divide two expressions.
        """
        return BinOp("/", self, other)

    def __rtruediv__(self, other: Self | Rational) -> "BinOp":
        """
        Divide two expressions.
        """
        return BinOp("/", other, self)

    def __pow__(self, other: Self | Rational) -> "BinOp":
        """
        Exponentiate two expressions.
        """
        return BinOp("**", self, other)

    def __rpow__(self, other: Self | Rational) -> "BinOp":
        """
        Exponentiate two expressions.
        """
        return BinOp("**", other, self)

    def __neg__(self) -> "UnOp":
        """
        Negate an expression.
        """
        return UnOp("-", self)

    def __lt__(self, other: Self | Rational) -> "Relation":
        """
        Return the less-than relation between two expressions.
        """
        return Relation("<", self, other)

    def __le__(self, other: Self | Rational) -> "Relation":
        """
        Return the less-than-or-equals relation between two expressions.
        """
        return Relation("<=", self, other)

    def __eq__(self, other: Self | Rational) -> "Relation":
        """
        Return the equals relation between two expressions.
        """
        return Relation("==", self, other)

    def __ne__(self, other: Self | Rational) -> "Relation":
        """
        Return the not-equals relation between two expressions.
        """
        return Relation("!=", self, other)

    def __gt__(self, other: Self | Rational) -> "Relation":
        """
        Return the greater-than relation between two expressions.
        """
        return Relation(">", self, other)

    def __ge__(self, other: Self | Rational) -> "Relation":
        """
        Return the greater-than-or-equals relation between two expressions.
        """
        return Relation(">=", self, other)


@dataclass(frozen=True, slots=True, eq=False)
class UnOp(Expr):
    """
    An unary operation.
    """
    symbol: str
    expr: Expr

    def __str__(self) -> str:
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

    def __str__(self) -> str:
        lhs = f"({self.lhs})" if isinstance(self.lhs, BinOp) else f"{self.lhs}"
        rhs = f"({self.rhs})" if isinstance(self.rhs, BinOp) else f"{self.rhs}"
        return f"{lhs} {self.symbol} {self.rhs}"


@dataclass(frozen=True, slots=True, eq=False)
class Var(Expr):
    """
    A variable.
    """
    name: str

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True, slots=True, eq=False)
class Relation:
    """
    A relation between two expressions or relations.

    Arithmetic operations on relations apply to both sides. Logical operations
    on relations create compound relations (relation of relations). Comparisons
    of relations not supported. Relations are not expressions.
    """
    symbol: str
    lhs: Expr
    rhs: Expr

    def __add__(self, other: Expr | Rational) -> "Relation":
        """
        Add to both sides of a relation.
        """
        return Relation(self.symbol, self.lhs + other, self.rhs + other)

    def __radd__(self, other: Expr | Rational) -> "Relation":
        """
        Add to both sides of a relation.
        """
        return Relation(self.symbol, other + self.lhs, other + self.rhs)

    def __sub__(self, other: Expr | Rational) -> "Relation":
        """
        Subtract from both sides of a relation.
        """
        return Relation(self.symbol, self.lhs - other, self.rhs - other)

    def __rsub__(self, other: Expr | Rational) -> "Relation":
        """
        Subtract from both sides of a relation.
        """
        return Relation(self.symbol, other - self.lhs, other - self.rhs)

    def __mul__(self, other: Expr | Rational) -> "Relation":
        """
        Multiply both sides of a relation.
        """
        return Relation(self.symbol, self.lhs * other, self.rhs * other)

    def __rmul__(self, other: Expr | Rational) -> "Relation":
        """
        Multiply both sides of a relation.
        """
        return Relation(self.symbol, other * self.lhs, other * self.rhs)

    def __truediv__(self, other: Expr | Rational) -> "Relation":
        """
        Divide both sides of a relation.
        """
        return Relation(self.symbol, self.lhs / other, self.rhs / other)

    def __rtruediv__(self, other: Expr | Rational) -> "Relation":
        """
        Divide both sides of a relation.
        """
        return Relation(self.symbol, other / self.lhs, other / self.rhs)

    def __pow__(self, other: Expr | Rational) -> "Relation":
        """
        Exponentiate both sides of a relation.
        """
        return Relation(self.symbol, self.lhs ** other, self.rhs ** other)

    def __rpow__(self, other: Expr | Rational) -> "Relation":
        """
        Exponentiate both sides of a relation.
        """
        return Relation(self.symbol, other ** self.lhs, other ** self.rhs)

    def __neg__(self) -> "Relation":
        """
        Negate both sides of a relation.
        """
        return Relation(self.symbol, -self.lhs, -self.rhs)

    def __invert__(self) -> "Relation":
        """
        Invert the relation.
        """
        simple = {"<": ">=", "<=": ">", "==": "!=", "!=": "==", ">": "<=", ">=": "<"}
        compound = {"&": "|", "|": "&"}
        if self.symbol in simple:
            return Relation(simple[self.symbol], self.lhs, self.rhs)
        if self.symbol in compound:
            return Relation(compound[self.symbol], ~self.lhs, ~self.rhs)
        if self.symbol == "^":
            return Relation("&", self.lhs, self.rhs) | Relation("&", ~self.lhs, ~self.rhs)

        raise NotImplementedError(f"Can't invert symbol {self.symbol!r}")

    def __or__(self, other: "Relation") -> "Relation":
        """
        Either relation.
        """
        return Relation("|", self, other)

    def __and__(self, other: "Relation") -> "Relation":
        """
        Both relations.
        """
        return Relation("&", self, other)

    def __xor__(self, other: "Relation") -> "Relation":
        """
        Either relation, but not both.
        """
        return Relation("^", self, other)

    def __str__(self) -> str:
        lhs = f"({self.lhs})" if isinstance(self.lhs, Relation) else f"{self.lhs}"
        rhs = f"({self.rhs})" if isinstance(self.rhs, Relation) else f"{self.rhs}"
        return f"{lhs} {self.symbol} {rhs}"
