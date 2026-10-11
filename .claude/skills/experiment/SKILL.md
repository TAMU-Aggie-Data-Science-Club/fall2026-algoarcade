---
name: experiment
description: Rules for defining, launching and reporting training runs in this repo. Use when writing an experiment definition, choosing hyperparameters or seeds, starting a run locally or on the training box, comparing two runs, or writing up a result with a number in it.
paths: src/algoarcade/training/**, src/algoarcade/runqueue/**, experiments/**
---

# Running an experiment

A result we cannot reproduce or compare is not a result. These rules exist so that every number in the writeup traces to runs that differ in exactly one way.

Change one factor. An experiment names the baseline config and the single factor it varies. If you need to change two things, that is two experiments.

Set gamma explicitly. The library default of 0.99 gives a horizon of about 100 steps, and our episodes are thousands of steps long. An agent at the default does not crash. It does not learn. We start at 0.997.

Use five seeds for anything you will claim, on the same seed set as the arm you compare against. Three seeds is exploratory and must be labeled that way. Report the interquartile mean with a bootstrap interval, and print the seed count next to it.

Treat a step-budget end as truncation, not termination, and bootstrap the value there.

Every run records its seed, git commit, ROM SHA-1, reward config hash and resolved config in its run directory. Commit your code before you launch, or the commit hash means nothing.

Evaluate from the fixed start state with the archive off, whatever the training used.

Debug locally with one environment and 1,000 steps. Nothing interactive happens on the training box. Once the queue exists, a run on the box goes through the queue, never a terminal.

Never change the logging schema to suit a run. It freezes on October 25.

Before you believe a curve, watch the agent. Check the per-component reward chart, check that unique tiles rise with return, and watch five minutes of video.

A negative result is a result. Write down what you ran and what happened, including the arm that lost.

The experiment table and the compute budget are in `docs/technical-plan.md` under "Experiments". TRN-01 owns this skill and updates it when the runner lands.
