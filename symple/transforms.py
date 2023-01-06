"""
Transformations of expressions into equivalent expressions.
"""
__all__ = "collect", "distribute"

from math import prod
from numbers import Number

from .expr import *

def collect(expr: Expr):
    """
    Collect number terms in sum or products.
    """
    match expr.symbol:
        case "+":
            args = [arg for arg in expr.args if not isinstance(arg, Number)]
            total = sum(arg for arg in expr.args if isinstance(arg, Number))
            if total == 0:
                if len(args) == 1:
                    return args[0]
                return Expr("+", *args)
            return Expr("+", *args, total)
        case "*":
            args = [arg for arg in expr.args if not isinstance(arg, Number)]
            total = prod(arg for arg in expr.args if isinstance(arg, Number))
            if total == 0:
                return type(total)(0)
            if total == 1:
                if len(args) == 1:
                    return args[0]
                return Expr("*", *args)
            return Expr("*", *args, total)
        case _:
            return expr

def distribute(expr: Expr):
    """
    Apply a left- or right-distribution, e.g.:
        a * (b + c) -> a * b + a * c
        (b + c) * a -> a * b + a * c
    """
    if expr.symbol != "*":
        return expr

    for i, arg in enumerate(expr.args):
        if isinstance(arg, Expr) and arg.symbol == "+":
            break
    else:
        return expr

    j = i + 1 if i == 0 else i - 1
    args = [arg for k, arg in enumerate(expr.args) if k != i and k != j]

    terms = arg.args
    coef = expr.args[j]
    distributed = Expr("+", *(coef * term for term in terms))

    if len(args) == 0:
        return distributed

    args.insert(min(i, j), distributed)
    return Expr("*", *args)
