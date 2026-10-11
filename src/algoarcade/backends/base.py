"""The one interface every emulator sits behind. Contract: docs/harness-spec.md, GameBackend."""

from collections.abc import Iterable
from enum import IntEnum
from typing import Protocol

import numpy as np
from numpy.typing import NDArray


class Button(IntEnum):
    """Values are the bit positions in the GBA key register. Game Boy backends ignore R and L."""

    A = 0
    B = 1
    SELECT = 2
    START = 3
    RIGHT = 4
    LEFT = 5
    UP = 6
    DOWN = 7
    R = 8
    L = 9


class GameBackend(Protocol):
    """Loading the ROM is the constructor's job, so it is not part of the protocol."""

    def step(self, frames: int = 1) -> None:
        """Advance with no input."""
        ...

    def press(self, buttons: Iterable[Button], hold: int = 8, release: int = 16) -> None:
        """Hold the buttons for `hold` frames, then let go for `release` frames."""
        ...

    def screen(self) -> NDArray[np.uint8]:
        """The current frame as (H, W, 3) RGB. A copy: the caller may keep or change it."""
        ...

    def read(self, address: int, size: int) -> bytes:
        """`size` bytes starting at `address`. Raises ValueError outside mapped memory."""
        ...

    def save_state(self) -> bytes: ...

    def load_state(self, state: bytes) -> None: ...

    def close(self) -> None: ...


def read_u8(backend: GameBackend, address: int) -> int:
    return backend.read(address, 1)[0]


def read_u16(backend: GameBackend, address: int) -> int:
    return int.from_bytes(backend.read(address, 2), "little")


def read_u32(backend: GameBackend, address: int) -> int:
    return int.from_bytes(backend.read(address, 4), "little")
