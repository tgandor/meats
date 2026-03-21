from __future__ import annotations

from typing import TYPE_CHECKING, get_type_hints

if TYPE_CHECKING:
    # this is the hack to satisfy the type checker, but it will not be executed at runtime
    from typing import Any

# This will not cause a NameError, even though Any is not defined
def greet(name: str = "") -> Any:
    print(f"Look {name or 'Ma'}, no type errors!")

greet("Alice")

print(f"{greet.__annotations__=}")  # OK, returns strings
print(f"{get_type_hints(greet)=}")  # this raises, because it tries to evaluate the annotations
