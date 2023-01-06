from numbers import Number

from .expr import *
from .transforms import *

def solve(expr: Expr, value: Number):
    """
    Solve `expr == value` for some expression of a single variable.
    """
    match expr.symbol:
        case "+" | "*" as s:
            expr = collect(expr)
            number = expr.args[-1]
            if not isinstance(number, Number):
                return expr == value

            result = value - number if s == "+" else value / number
            if len(expr.args) == 2:
                return solve(expr.args[0], result)
            return Expr(s, expr.args[:-1]) == result
        case "-":
            return solve(expr.args[0], -value)
        case _:
            return value
