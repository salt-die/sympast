# symple

Simplify and solve simple symbolic expressions.

Simple expressions are variables or products, sums, and powers of a simple expression and a number.
```
    ┌────────────────┬────────────────┐
    │ simple         │ not simple     │
    ├────────────────┼────────────────┤
    │ x              │   ~            │
    │ x + 2          │ x + y          │
    │ 2 * x + 2      │ x * y          │
    │ 2 * x ** 4 + 2 │ x ** y         │
    └────────────────┴────────────────┘
```

```py
from symple import Expr, solve

x = Expr('x')

expr = ((474 + (2 * (((785 + (((((((((824 + (40 * (x - 645))) / 8) + 351) + 733) / 6) - 650) * 49) - 458) * 2)) / 3) - 575))) / 2) + 434 == 91894585615351
```