# runqueue

The experiment queue for the training box. An experiment is a Python file naming a base config and the factors to vary. The queue expands it into runs and executes them unattended.

Arrives with OPS-04 (Sahil).

Contract: `docs/technical-plan.md`, Run queue. Nobody launches runs on the box by hand once this exists.
