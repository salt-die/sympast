__all__ = "symbol", "symbols", "Polynomial"

from math import prod
from numbers import Number
from typing import Self

import numpy as np
from scipy.signal import convolve

_SS = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

def symbol(s: str, *, dtype=int):
    """
    Create a symbol.

    Parameters
    ----------
    s : str
        Symbol name.
    type : Number, default: int
        Type for coefficients of the polynomial.
    """
    return Polynomial((s,), np.array([dtype(), dtype() + 1]))

def symbols(s: str, *, dtype=int):
    """
    Create symbols from a space- or comma-delimited string.

    Parameters
    ----------
    s : str
        Space- or comma-delimited string.
    type : Number, default: int
        Type for coefficients of the polynomial.
    """
    return tuple(symbol(sym, dtype=dtype) for sym in s.replace(",", " ").split())

def _trim(vars: tuple[str, ...], arr: np.ndarray) -> tuple[tuple[str, ...], np.ndarray]:
    """
    Remove unused variables and trailing zeros from a polynomial array.
    """
    monos = np.argwhere(arr)
    if len(monos) == 0:
        return (), np.array(0)
    max_exps = monos.max(axis=0)
    used_vars = tuple(var for e, var in zip(max_exps, vars) if e)
    axes = tuple(np.s_[:e + 1] for e in max_exps)
    return used_vars, np.array(arr[axes].squeeze())


class Polynomial:
    """
    Multivariate polynomials.
    """
    __slots__ = "vars", "array"

    def __init__(self, vars: tuple[str, ...], array: np.ndarray):
        if len(array.shape) != len(vars):
            raise ValueError("Array dimension doesn't match number of variables.")

        self.vars, self.array = _trim(vars, array)

    def copy(self) -> Self:
        """
        Return a copy.
        """
        return Polynomial(self.vars, self.array.copy())

    @property
    def deg(self) -> int:
        """
        Degree of polynomial.
        """
        where = np.argwhere(self.array)
        if len(where) == 0:
            return 0
        return where.sum(axis=1).max()

    @property
    def dtype(self) -> type:
        """
        Data type of coefficients.
        """
        return type(self.array.reshape(-1)[0])

    def _normalize(a: Self, b: Self) -> tuple[tuple[str, ...], np.ndarray, np.ndarray]:
        """
        Combine variables of two polynomials and make their arrays compatible.
        """
        vars_ = tuple(sorted(set(a.vars) | set(b.vars)))

        a_shape = dict(zip(a.vars, a.array.shape))
        b_shape = dict(zip(b.vars, b.array.shape))

        a_axes = tuple(np.s_[:a_shape[var]] if var in a_shape else 0 for var in vars_)
        b_axes = tuple(np.s_[:b_shape[var]] if var in b_shape else 0 for var in vars_)

        shape = tuple(max(a_shape.get(var, -1), b_shape.get(var, -1)) for var in vars_)
        a_normal = np.zeros(shape, a.array.dtype)
        b_normal = np.zeros(shape, b.array.dtype)

        a_normal[a_axes] = a.array
        b_normal[b_axes] = b.array

        return vars_, a_normal, b_normal

    def __add__(self, other: Number | Self) -> Self:
        if isinstance(other, Number):
            array = np.array(self.array + type(other)())  # Re=cast array to be compatible with number type.
            array.reshape(-1)[0] += other
            return Polynomial(self.vars, array)

        if not isinstance(other, Polynomial):
            return NotImplemented

        vars_, self_normal, other_normal = self._normalize(other)

        return Polynomial(vars_, self_normal + other_normal)

    __radd__ = __add__

    def __sub__(self, other: Number | Self) -> Self:
        return self + -other

    def __rsub__(self, other: Number | Self) -> Self:
        return other + -self

    def __mul__(self, other: Number | Self) -> Self:
        if isinstance(other, Number):
            return Polynomial(self.vars, self.array * other)

        if not isinstance(other, Polynomial):
            return NotImplemented

        vars_, self_normal, other_normal = self._normalize(other)

        return Polynomial(vars_, convolve(self_normal, other_normal))

    __rmul__ = __mul__

    def __neg__(self) -> Self:
        return -1 * self

    def __truediv__(self, other: Number) -> Self:
        # TODO: Implement rational polynomials
        if isinstance(other, Number):
            return Polynomial(self.vars, self.array / other)

        return NotImplemented

    def __pow__(self, other: int) -> Self:
        if not isinstance(other, int):
            return NotImplemented

        if other < 0:
            # TODO: Implement rational polynomials
            return NotImplemented

        if other == 0:
            return 1

        if other == 1:
            return self

        if other % 2 == 1:
            return self * self ** (other - 1)

        return (self * self) ** (other // 2)

    def _power_str(self, var, power) -> str:
        if power == 0:
            return ""
        if power == 1:
            return var

        return f"{var}{str(power).translate(_SS)}"

    def __repr__(self) -> str:
        return f"Polynomial(vars={self.vars!r}, array={self.array!r})"

    def _str_helper(self):
        for term in np.argwhere(self.array)[::-1]:
            coef = self.array[tuple(term)]
            power = "".join(map(self._power_str, self.vars, term))
            if coef == 1:
                if power:
                    yield power
                else:
                    yield str(coef)
            else:
                yield f"{coef}{power}"

    def __str__(self) -> str:
        return " + ".join(self._str_helper()) or "0"

    def eval(self, **values: Number) -> Self | Number:
        """
        Evaluate a polynomial at some values.

        Keyword arguments should be variable names, e.g., `(x ** 2 + y ** 3).eval(x=2, y=3)`.
        """
        powers = (values.get(var, 1) ** np.arange(s) for var, s in zip(self.vars, self.array.shape))
        products = self.array * np.array(np.meshgrid(*powers, indexing="ij")).prod(axis=0)
        vars = tuple(var for var in self.vars if var not in values)
        if not vars:
            return products.sum()
        sum_indices = tuple(i for i, var in enumerate(self.vars) if var in values)
        return Polynomial(vars, products.sum(axis=sum_indices))

    @property
    def roots(self) -> tuple[Number, ...]:
        """
        Roots of the polynomial.

        Raises
        ------
        ValueError
            If polynomial has more than one variable.
        """
        if len(self.vars) > 1:
            raise ValueError("Can't calculate roots of multivariate polynomials.")

        if self.deg == 1:
            c, coef = self.array
            return (-c / coef,)

        return tuple(np.polynomial.Polynomial(self.array).roots())
