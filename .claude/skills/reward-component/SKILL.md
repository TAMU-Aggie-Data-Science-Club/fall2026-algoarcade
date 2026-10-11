---
name: reward-component
description: The contract for reward terms in this repo and the tests each one must ship with. Use when adding, changing or tuning a reward component or its weight, working under src/algoarcade/rewards, or investigating an agent that is farming reward without making progress.
paths: src/algoarcade/rewards/**
---

# Adding or changing a reward component

An agent will find every way a reward can be earned without doing what you meant. Assume that, and build the guard with the component.

A component implements the `RewardComponent` protocol in `src/algoarcade/rewards/base.py`: a `name`, a `reset(state)` called with the first state of an episode, and a `score(prev, curr)` that returns a float. It keeps its own per-episode memory (a visited set, a best-so-far) and clears it in `reset`. Its weight lives in config, never in the component.

Every component ships with four things.

An isolation test: `score(state, state)` is exactly 0.0, and the first `score` after `reset` on an unchanged state is exactly 0.0. A reward that fires on reset teaches the agent to die quickly.

An exploit test: a scripted policy that tries the obvious farm (walk between two tiles, mash a button in a menu, faint on purpose, level in the first grass forever) and must earn less than a bound you state in the test.

A log column. The environment reports each component's raw value in the step info as `reward/<name>`. Check that the new name appears in the schema. After October 25 a new column is a schema change, which is a PM decision.

An exploit note in the pull request: one or two sentences on how an agent would game this component and what stops it.

Prefer terms that pay for a new maximum (a new flag, a first visit this episode, a higher level sum) over terms that pay for a change. Use coordinates for novelty, never screen hashes or a sliding window. Validate any RAM field before paying on it. Penalties and the heal reward exist but are off by default; turning one on is experiment E5, not a tuning step.

When you tune a weight, change one weight, state the ratio you are aiming for (badge above everything, events above level), and watch the per-component chart and five minutes of video before trusting the return curve.

The contract is in `docs/harness-spec.md` under "Reward registry", and the reasoning in `docs/technical-plan.md` under "Reward design". TRN-02 owns this skill and updates it when the registry lands.
