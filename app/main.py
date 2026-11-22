# app/main.py
# A simple, safe Python function — our "application" fixture
# The security scanners use this file as their target.

def greet(name: str) -> str:
    """Return a greeting message."""
    return f"Hello, {name}! Welcome to the DevSecOps demo."

def add(a: int, b: int) -> int:
    """Return the sum of two numbers."""
    return a + b

if __name__ == "__main__":
    print(greet("World"))
    print(f"2 + 3 = {add(2, 3)}")
