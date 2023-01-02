__all__ = "Expr", "BinOp", "Var"

from operator import itemgetter

_SYMBOL_MAP = dict(add="+", sub="-", mul="*", truediv="/")
_EXPR_BODY = """
def __{0}__(self, other):
    return BinOp('{1}', self, other)
def __r{0}__(self, other):
    return BinOp('{1}', other, self)
"""
_EXPR_NEW = """
def __new__(cls, {0}):
    return tuple.__new__(cls, ({0}))
"""

class ExprMeta(type):
    """
    Expression metaclass.

    Expressions are named tuples that respect inheritance.
    """
    def __new__(meta, name, bases, namespace):
        args = tuple(namespace.get("__annotations__", ()))
        exec(_EXPR_NEW.format(", ".join(args)), locals(), namespace)
        namespace["__new__"].__defaults__ = tuple(namespace[arg] for arg in args if arg in namespace)

        def __repr__(self):
            return f"{name}({', '.join(f'{arg}={self[i]!r}' for i, arg in enumerate(args))})"

        namespace |= {
            '__slots__': (),
            '__repr__': __repr__,
            '__match_args__': args,
        }
        for index, arg in enumerate(args):
            namespace[arg] = property(itemgetter(index), doc=f"Alias for field number {index}.")

        return super().__new__(meta, name, bases, namespace)

class Expr(tuple, metaclass=ExprMeta):
    for _item in _SYMBOL_MAP.items():
        exec(_EXPR_BODY.format(*_item))
    del _item

class BinOp(Expr):
    op: str
    lhs: Expr
    rhs: Expr

    def __str__(self):
        lhs = f"({self.lhs})" if isinstance(self.lhs, BinOp) else f"{self.lhs}"
        rhs = f"({self.rhs})" if isinstance(self.rhs, BinOp) else f"{self.rhs}"
        return f"{lhs} {self.op} {rhs}"

class Var(Expr):
    name: str

    def __str__(self):
        return self.name
