from fractions import Fraction
from numbers import Rational

from .expr import *

def solve(expr: Expr, value: Fraction=Fraction()):
    """
    Solve `expr == value` for some expression of a single variable.
    """
    match expr:
        case Var():
            return value
        case BinOp("+", Rational(), _):
            return solve(expr.rhs, value - expr.lhs)
        case BinOp("+", _, Rational()):
            return solve(expr.lhs, value - expr.rhs)
        case BinOp("-", Rational(), _):
            return solve(expr.rhs, expr.lhs - value)
        case BinOp("-", _, Rational()):
            return solve(expr.lhs, value + expr.rhs)
        case BinOp("*", Rational(), _):
            return solve(expr.rhs, Fraction(value, expr.lhs))
        case BinOp("*", _, Rational()):
            return solve(expr.lhs, Fraction(value, expr.rhs))
        case BinOp("/", Rational(), _):
            return solve(expr.rhs, Fraction(expr.lhs, value))
        case BinOp("/", _, Rational()):
            return solve(expr.lhs, expr.rhs * value)
