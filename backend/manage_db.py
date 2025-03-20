#!/usr/bin/env python
import os
import sys
from alembic.config import Config
from alembic import command


def run_migrations():
    """Run database migrations."""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


def create_migration(message):
    """Create a new migration."""
    alembic_cfg = Config("alembic.ini")
    command.revision(alembic_cfg, autogenerate=True, message=message)


def rollback_migration(revision):
    """Rollback to a specific migration."""
    alembic_cfg = Config("alembic.ini")
    command.downgrade(alembic_cfg, revision)


def show_migrations():
    """Show migration history."""
    alembic_cfg = Config("alembic.ini")
    command.history(alembic_cfg)


def main():
    if len(sys.argv) < 2:
        print("Usage: python manage_db.py [command] [args]")
        print("\nCommands:")
        print("  migrate          Run all pending migrations")
        print("  create [message] Create a new migration")
        print("  rollback [rev]   Rollback to a specific migration")
        print("  show            Show migration history")
        sys.exit(1)

    command = sys.argv[1]

    if command == "migrate":
        run_migrations()
    elif command == "create":
        if len(sys.argv) < 3:
            print("Error: Migration message is required")
            sys.exit(1)
        create_migration(sys.argv[2])
    elif command == "rollback":
        if len(sys.argv) < 3:
            print("Error: Migration revision is required")
            sys.exit(1)
        rollback_migration(sys.argv[2])
    elif command == "show":
        show_migrations()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
