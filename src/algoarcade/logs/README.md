# logs

The logging schema, the Parquet writer and the fake logger. Parquet is the source of truth for every figure we publish.

Arrives with OPS-03 (Sahil). The schema freezes on October 25 under the tag `schema-v1`. After that, changing a field is a PM decision and means re-running training.

Contract: `docs/harness-spec.md`, Logging schema.
