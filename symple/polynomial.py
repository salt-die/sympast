__all__ = "symbol", "symbols", "Polynomial"

from math import prod
from numbers import Number
from typing import Self

import numpy as np
from scipy.signal import convolve

_SS = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

def symbol(s: str, *, type=int):
    """
    Create a symbol.

    Parameters
    ----------
    s : str
        Symbol name.
    type : Number, default: int
        Type for coefficients of the polynomial.
    """
    return Polynomial((s,), np.array([type(), type() + 1]))

def symbols(s: str, *, type=int):
    """
    Create symbols from a space- or comma-delimited string.

    Parameters
    ----------
    s : str
        Space- or comma-delimited string.
    type : Number, default: int
        Type for coefficients of the polynomial.
    """
    return tuple(symbol(sym, type=type) for sym in s.replace(",", " ").split())

def _trim(arr: np.ndarray) -> np.ndarray:
    """
    Remove trailing zeros from a polynomial array.
    """
    nvars = len(arr.shape)
    axes = tuple(tuple(np.s_[-(i == j):] for i in range(nvars)) for j in range(nvars))
    trimmed = (np.s_[:-1],) * nvars
    while not any(arr[axis].any() for axis in axes):
        arr = arr[trimmed]
    return arr


class Polynomial:
    """
    Multivariate polynomials.
    """
    __slots__ = "vars", "array"

    def __init__(self, vars: tuple[str, ...], array: np.ndarray):
        self.vars = vars
        if len(array.shape) != len(vars):
            raise ValueError("Array dimension doesn't match number of variables.")

        if not array.any():
            self.array = np.zeros((1,) * len(vars), array.dtype)
        else:
            self.array = _trim(array)

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
        return len(self.array) - 1

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
        a_vars = set(a.vars)
        b_vars = set(b.vars)
        vars_ = tuple(sorted(a_vars | b_vars))
        a_len, b_len = len(a.array), len(b.array)

        a_axis = tuple(np.s_[:a_len] if symbol in a_vars else 0 for symbol in vars_)
        a_normal = np.zeros((max(a_len, b_len),) * len(vars_), dtype=a.array.dtype)
        a_normal[a_axis] = a.array

        b_axis = tuple(np.s_[:b_len] if symbol in b_vars else 0 for symbol in vars_)
        b_normal = np.zeros_like(a_normal)
        b_normal[b_axis] = b.array

        return vars_, a_normal, b_normal

    def __add__(self, other: Number | Self) -> Self:
        if isinstance(other, Number):
            array = self.array + type(other)()  # Re=cast array to be compatible with number type.
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
        values.update((var, symbol(var, type=self.dtype)) for var in self.vars if var not in values)

        return sum(
            self.array[tuple(term)] * prod(values[var]**exp for var, exp in zip(self.vars, term))
            for term in np.argwhere(self.array)
        )

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
