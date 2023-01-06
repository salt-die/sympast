"""
Expressions and relations.
"""
__all__ = "Expr", "Relation"

from numbers import Number
from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True, slots=True, eq=False)
class Expr:
    """
    Abstract base for arithmetic expressions.
    """
    symbol: str
    args: tuple[Self | Number]

    def __init__(self, symbol, *args):
        object.__setattr__(self, "symbol", symbol)
        object.__setattr__(self, "args", args)

    def __add__(self, other: Self | Number) -> Self:
        """
        Add two expressions.
        """
        match self.symbol:
            case "+":
                return Expr("+", *self.args, other)
            case _:
                return Expr("+", self, other)

    def __radd__(self, other: Self | Number) -> Self:
        """
        Add two expressions.
        """
        match self.symbol:
            case "+":
                return Expr("+", other, *self.args)
            case _:
                return Expr("+", other, self)

    def __sub__(self, other: Self | Number) -> Self:
        """
        Subtract two expressions.
        """
        return self + -other

    def __rsub__(self, other: Self | Number) -> Self:
        """
        Subtract two expressions.
        """
        return other + -self

    def __mul__(self, other: Self | Number) -> Self:
        """
        Multiply two expressions.
        """
        match self.symbol:
            case "*":
                return Expr("*", *self.args, other)
            case _:
                return Expr("*", self, other)

    def __rmul__(self, other: Self | Number) -> Self:
        """
        Multiply two expressions.
        """
        match self.symbol:
            case "*":
                return Expr("*", other, *self.args)
            case _:
                return Expr("*", other, self)

    def __truediv__(self, other: Self | Number) -> Self:
        """
        Divide two expressions.
        """
        return self * other ** -1

    def __rtruediv__(self, other: Self | Number) -> Self:
        """
        Divide two expressions.
        """
        return other * self ** -1

    def __pow__(self, other: Self | Number) -> Self:
        """
        Exponentiate two expressions.
        """
        match self.symbol:
            case "**":
                base, exp = self.args
                return Expr("**", base, exp * other)
            case _:
                return Expr("**", self, other)

    def __rpow__(self, other: Self | Number) -> Self:
        """
        Exponentiate two expressions.
        """
        return Expr("**", other, self)

    def __neg__(self) -> Self:
        """
        Negate an expression.
        """
        match self.symbol:
            case "-":
                return self.args[0]
            case _:
                return Expr("-", self)

    def __lt__(self, other: Self | Number) -> "Relation":
        """
        Return the less-than relation between two expressions.
        """
        return Relation("<", self, other)

    def __le__(self, other: Self | Number) -> "Relation":
        """
        Return the less-than-or-equals relation between two expressions.
        """
        return Relation("<=", self, other)

    def __eq__(self, other: Self | Number) -> "Relation":
        """
        Return the equals relation between two expressions.
        """
        return Relation("==", self, other)

    def __ne__(self, other: Self | Number) -> "Relation":
        """
        Return the not-equals relation between two expressions.
        """
        return Relation("!=", self, other)

    def __gt__(self, other: Self | Number) -> "Relation":
        """
        Return the greater-than relation between two expressions.
        """
        return Relation(">", self, other)

    def __ge__(self, other: Self | Number) -> "Relation":
        """
        Return the greater-than-or-equals relation between two expressions.
        """
        return Relation(">=", self, other)

    def __str__(self) -> str:
        PRECEDENCE = {"+": 0, "*": 1, "-": 2, "**": 3}

        def nest_str(expr):
            if (
                isinstance(expr, Expr) and
                expr.symbol in PRECEDENCE and
                PRECEDENCE[expr.symbol] < PRECEDENCE[self.symbol]
            ):
                return f"({expr})"
            return f"{expr}"

        match len(self.args):
            case 0:
                return self.symbol
            case 1:
                return f"{self.symbol}{nest_str(self.args[0])}"
            case _:
                return f" {self.symbol} ".join(map(nest_str, self.args))


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

    def __add__(self, other: Expr | Number) -> "Relation":
        """
        Add to both sides of a relation.
        """
        return Relation(self.symbol, self.lhs + other, self.rhs + other)

    def __radd__(self, other: Expr | Number) -> "Relation":
        """
        Add to both sides of a relation.
        """
        return Relation(self.symbol, other + self.lhs, other + self.rhs)

    def __sub__(self, other: Expr | Number) -> "Relation":
        """
        Subtract from both sides of a relation.
        """
        return Relation(self.symbol, self.lhs - other, self.rhs - other)

    def __rsub__(self, other: Expr | Number) -> "Relation":
        """
        Subtract from both sides of a relation.
        """
        return Relation(self.symbol, other - self.lhs, other - self.rhs)

    def __mul__(self, other: Expr | Number) -> "Relation":
        """
        Multiply both sides of a relation.
        """
        return Relation(self.symbol, self.lhs * other, self.rhs * other)

    def __rmul__(self, other: Expr | Number) -> "Relation":
        """
        Multiply both sides of a relation.
        """
        return Relation(self.symbol, other * self.lhs, other * self.rhs)

    def __truediv__(self, other: Expr | Number) -> "Relation":
        """
        Divide both sides of a relation.
        """
        return Relation(self.symbol, self.lhs / other, self.rhs / other)

    def __rtruediv__(self, other: Expr | Number) -> "Relation":
        """
        Divide both sides of a relation.
        """
        return Relation(self.symbol, other / self.lhs, other / self.rhs)

    def __pow__(self, other: Expr | Number) -> "Relation":
        """
        Exponentiate both sides of a relation.
        """
        return Relation(self.symbol, self.lhs ** other, self.rhs ** other)

    def __rpow__(self, other: Expr | Number) -> "Relation":
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
