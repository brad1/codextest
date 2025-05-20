# codextest

This repository contains simple utilities.

## CLI utility

Run `cli.py` without arguments to see usage instructions. Use the `--test` option to scan the current environment for PostgreSQL connection settings:

```bash
python3 cli.py --test
```

Every invocation of `cli.py` is appended to `history.list` in the
repository root so you can review past commands.

