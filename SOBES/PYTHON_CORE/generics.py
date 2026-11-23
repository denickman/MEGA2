

# в Python есть ограничения (constraints) для дженериков — аналог Swift

from typing import TypeVar

T = TypeVar("T", bound=int)   # T должен быть int или его подкласс

def double(x: T) -> T:
    return x * 2

# Или через явный список допустимых типов:
T = TypeVar("T", int, float)   # T может быть ТОЛЬКО int или float, не что-то ещё