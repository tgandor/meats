from __future__ import annotations

# This will not cause a NameError, even though Any is not defined
def greet(name: str) -> Any:
    print("Look Ma, no type errors!")

greet("Alice")
