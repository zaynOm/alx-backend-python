#!/usr/bin/env python3
"Complex types - functions"
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    "Make a closure that multipliyies two floats"

    def multiply(n: float) -> float:
        return n * multiplier

    return multiply
