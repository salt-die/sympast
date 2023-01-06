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

    args = expr.args
    for i, arg in enumerate(args, start=1):
        if isinstance(arg, Expr) and arg.symbol == "+":
            break
    else:
        return expr

    coef = i + 1 if i == 1 else i - 1
    args = [arg for j, arg in enumerate(args, start=1) if j != i and j != coef]
    distributed = Expr("+", *(expr[coef] * term for term in expr[i].args))
    if len(args) == 0:
        return distributed

    args.insert(min(i, coef), distributed)
    return Expr("*", *args)
