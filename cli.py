#!/usr/bin/env python3
"""Simple command line utility to scan for postgres connections."""
import os
import sys
from pathlib import Path

USAGE = """Usage: cli.py [--test]\n\nOptions:\n  --test       Scan environment for postgres DB connections.\n  -h, --help   Show this help message.\n"""

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
