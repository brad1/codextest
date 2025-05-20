# codextest

This repository contains simple utilities.

## CLI utility

Run `cli.py` without arguments to see usage instructions. Use the `--test` option to scan the current environment for PostgreSQL connection settings and verify which tools from `requirements.list` are installed:

```bash
python3 cli.py --test
```

Each invocation of the CLI is appended to `~/.codextest_history` so you can review
the commands you've run.

