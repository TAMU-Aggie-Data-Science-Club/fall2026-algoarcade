---
name: deslop
description: Removes the unnecessary code that coding agents tend to add, without changing behavior. Use after an agent wrote a lot of code, or when asked to simplify or deslop a file or a diff. Targets narrating comments, restating docstrings, impossible-case error handling, single-use helpers, speculative abstractions and leftover debug code. For a whole branch before a pull request, use pr-cleanup, which includes this.
---

# Deslop

Review the diff between this branch and its base (`git diff $(git merge-base HEAD main)...HEAD`, or the staged and unstaged changes if nothing is committed). Change only lines the diff touched. Keep behavior identical, and run `uv run poe check` afterwards to prove it.

This is not a bug hunt. If you find a bug, report it and leave it alone.

## What to remove

A comment that says what the next line does. Keep a comment only when it says why, or records something the code cannot: a hardware quirk, a source for a constant, a trap.

A docstring that restates the signature. A public function gets a docstring when its contract is not obvious from its name and types.

Handling for a case that cannot happen: a `try` around code that does not raise, a `None` check on a value that is never `None`, a fallback for a config field that always exists. Validate at the boundary (a file, a ROM, user input, an API response) and trust it inside.

A helper called once, a wrapper that only forwards, a class with one method and no state.

An abstraction with one implementation. The project has four protocols on purpose: GameBackend, GameState, StateReader, RewardComponent. Anything else needs a second implementation before it earns a base class or a registry.

Options nobody asked for: a parameter no caller sets, a config flag with one value, a "future use" hook.

Leftovers: `print` debugging, commented-out code, a TODO with no issue number, an unused import or variable.

## Before and after

Narrating comments and a restating docstring:

```python
def read_party_levels(backend, count):
    """Read the party levels.

    Args:
        backend: The backend to read from.
        count: The number of party members.

    Returns:
        A list of levels.
    """
    # Initialize the list of levels
    levels = []
    # Loop over each party member
    for slot in range(count):
        # Read the level byte and add it to the list
        levels.append(read_u8(backend, PARTY + slot * 100 + 0x54))
    return levels
```

```python
def read_party_levels(backend, count):
    return [read_u8(backend, PARTY + slot * 100 + 0x54) for slot in range(count)]
```

Defensive code for impossible states:

```python
def score(self, prev, curr):
    try:
        if prev is None or curr is None:
            return 0.0
        gained = curr.party_level_sum - prev.party_level_sum
        return float(min(max(gained, 0), self.cap)) if gained is not None else 0.0
    except Exception:
        return 0.0
```

```python
def score(self, prev, curr):
    return float(min(max(curr.party_level_sum - prev.party_level_sum, 0), self.cap))
```

A single-use helper and an abstraction with one implementation:

```python
class BaseFrameSkipper(ABC):
    @abstractmethod
    def skip(self, backend, action): ...


class DefaultFrameSkipper(BaseFrameSkipper):
    def skip(self, backend, action):
        self._do_press(backend, action)

    def _do_press(self, backend, action):
        backend.press(action, hold=8, release=16)
```

```python
backend.press(action, hold=8, release=16)
```

Leftovers:

```python
obs, info = env.reset(seed=seed)
print("DEBUG obs", obs.shape)
# obs = normalize(obs)  # old approach
# TODO: maybe handle other backends later
```

```python
obs, info = env.reset(seed=seed)
```

## Report

List what you removed, by file, in one line each. Say what you left alone and why if it looked removable but was not. Paste the tail of `uv run poe check`.
