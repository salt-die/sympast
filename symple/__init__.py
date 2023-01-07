from numbers import Number

from .expr import *
from .transforms import *

def solve(expr: Expr, value: Number):
    """
    Solve `expr == value` for some expression of a single variable.
    """
    eq = expr == value
    if expr.symbol == "+":
        if not isinstance(expr.args[-1], Number):
            return eq
        eq -= expr.args[-1]
    elif expr.symbol == "*":
        if not isinstance(expr.args[0], Number):
            return eq
        eq /= expr.args[0]
    elif expr.symbol == "**":
        if not isinstance(expr.args[1], Number):
            return eq
        eq **= 1 / expr.args[1]
    else:
        return value

    return solve(eq.lhs, eq.rhs)