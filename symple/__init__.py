from numbers import Number

from .polynomial import *

def solve(poly: Polynomial, value: Number):
    """
    Solve the equation `poly == value` for a polynomial of a single variable.
    """
    if len(poly.vars) > 1:
        return ValueError("Can't solve polynomial of more than one variable.")

    if poly.deg == 1:
        c, coef = poly.array
        return (value - c) / coef

    # TODO: Eigenvalues...
    return NotImplemented
