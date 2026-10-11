"""The shape of one reward term. Contract: docs/harness-spec.md, Reward registry."""

from typing import Protocol

from algoarcade.games.base import GameState


class RewardComponent(Protocol):
    name: str

    def reset(self, state: GameState) -> None:
        """Called with the first state of an episode."""
        ...

    def score(self, prev: GameState, curr: GameState) -> float:
        """Reward for moving from prev to curr. Zero when nothing changed."""
        ...
