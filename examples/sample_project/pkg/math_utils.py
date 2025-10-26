"""Tiny math utilities."""

def add(a,b):
    """Return a + b."""
    return a+b

def fib(n):
    """Return first n Fibonacci numbers."""
    a,b=0,1
    out=[]
    for _ in range(n):
        out.append(a)
        a,b=b,a+b
    return out
