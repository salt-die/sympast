# sympast

Currently, just a simple solver for arithmetic expressions of a single variable.

Maybe I'll add more. Maybe I won't.

```py
from sympast import Var, solve

x = Var('x')

expr = ((474 + (2 * (((785 + (((((((((824 + (40 * (x - 645))) / 8) + 351) + 733) / 6) - 650) * 49) - 458) * 2)) / 3) - 575))) / 2) + 434

solve(expr, 91894585615351)  # Fraction(3375719472770, 1)
```