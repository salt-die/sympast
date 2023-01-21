import numpy as np

from .polynomial import *

def content(poly: Polynomial) -> int:
    """
    Return gcd of coefficients of poly.
    """
    if np.can_cast(poly.dtype, int, "same_kind"):
        return np.gcd.reduce(poly.array, axis=None)

    raise ValueError("Polynomial coefficients are not integers.")

def primitive_part(poly: Polynomial) -> Polynomial:
    """
    Return poly divided by its content.
    """
    return Polynomial(poly.vars, poly.array // content(poly))

def primitive_part_content(poly: Polynomial) -> tuple[Polynomial, int]:
    """
    Return both the primitive part and content of poly.
    """
    cont = content(poly)
    return Polynomial(poly.vars, poly.array // cont), cont

def isolate_variable(poly: Polynomial, var: str | Polynomial) -> Polynomial:
    """
    Return polynomial with all variables except var evaluated at 1.
    """
    if isinstance(var, Polynomial):
        if len(var.vars) != 1 or (var.array != [0, 1]).any():
            raise ValueError("var should be str or Polynomial of deg 1 with root 0.")
        var = var.vars[0]
    vars = dict.fromkeys(poly.vars, 1)
    vars.pop(var, None)
    return poly.eval(**vars)

def factor_monomial(poly: Polynomial) -> tuple[Polynomial, Polynomial]:
    """
    Return (m, poly / m) for some monomial m of highest degree that divides poly.
    """
    cont = content(poly)
    nvars = len(poly.vars)
    exps = tuple(np.argwhere(poly.array).min(axis=0))

    mono = np.zeros_like(poly.array)
    mono[exps] = cont

    deflated = np.zeros_like(poly.array)
    deflated[tuple(np.s_[:nvars - e] for e in exps)] = poly.array[tuple(np.s_[e:] for e in exps)]

    return Polynomial(poly.vars, mono), Polynomial(poly.vars, deflated // cont)
