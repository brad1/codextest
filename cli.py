#!/usr/bin/env python3
"""Simple command line utility to scan for postgres connections."""
import os
import sys
from pathlib import Path

HISTORY_FILE = Path.home() / ".codextest_history"


def save_history(args):
    """Append the given arguments to the history file."""
    try:
        with open(HISTORY_FILE, "a", encoding="utf-8") as fh:
            fh.write(" ".join(args) + "\n")
    except OSError:
        # Failing to write history should not prevent the CLI from working
        pass

USAGE = (
    "Usage: cli.py [--test]\n\n"
    "Options:\n"
    "  --test       Scan environment for postgres DB connections.\n"
    "  -h, --help   Show this help message.\n\n"
    "Command history is saved to ~/.codextest_history."
)

def print_usage():
    print(USAGE.strip())


def scan_env():
    env_vars = [
        "DATABASE_URL",
        "POSTGRES_URL",
        "POSTGRES_URI",
        "POSTGRES_DSN",
        "PGHOST",
        "PGPORT",
        "PGUSER",
        "PGPASSWORD",
        "PGDATABASE",
    ]

    found = False
    for var in env_vars:
        if var in os.environ:
            print(f"{var}={os.environ[var]}")
            found = True

    pgpass = os.environ.get("PGPASSFILE", str(Path.home() / ".pgpass"))
    if os.path.exists(pgpass):
        print(f"Found pgpass file at {pgpass}")
        found = True

    pgservice = os.environ.get("PGSERVICEFILE", str(Path.home() / ".pg_service.conf"))
    if os.path.exists(pgservice):
        print(f"Found pg service file at {pgservice}")
        found = True

    if not found:
        print("No postgres connection info found.")


def main(argv=None):
    argv = argv or sys.argv[1:]
    save_history(argv)
    if not argv or argv[0] in {"-h", "--help"}:
        print_usage()
        return 0

    if argv[0] == "--test":
        scan_env()
        return 0

    print_usage()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
