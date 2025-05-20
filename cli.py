#!/usr/bin/env python3
"""Simple command line utility to scan for postgres connections and verify requirements."""
import os
import sys
import shutil
from pathlib import Path

HISTORY_FILE = Path.home() / ".codextest_history"
REQUIREMENTS_FILE = Path(__file__).with_name("requirements.list")


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
    "  --test       Scan environment for postgres DB connections and check requirements.\n"
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


def check_requirements(requirements_path=None):
    """Check which command-line tools from requirements.list are installed."""
    path = Path(requirements_path or REQUIREMENTS_FILE)
    if not path.exists():
        print(f"Requirements file not found at {path}")
        return

    with open(path, "r", encoding="utf-8") as req_file:
        for line in req_file:
            req = line.strip()
            if not req:
                continue
            if shutil.which(req):
                print(f"{req}: found")
            else:
                print(f"{req}: not found")


def main(argv=None):
    argv = argv or sys.argv[1:]
    save_history(argv)
    if not argv or argv[0] in {"-h", "--help"}:
        print_usage()
        return 0

    if argv[0] == "--test":
        scan_env()
        check_requirements()
        return 0

    print_usage()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
