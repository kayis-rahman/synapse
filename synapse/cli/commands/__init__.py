"""
SYNAPSE CLI Commands

Command modules for the unified CLI interface.
"""

from synapse.cli.commands import start
from synapse.cli.commands import stop
from synapse.cli.commands import status
from synapse.cli.commands import ingest
from synapse.cli.commands import query
from synapse.cli.commands import setup
from synapse.cli.commands import models

__all__ = [
    "start",
    "stop",
    "status",
    "ingest",
    "query",
    "setup",
    "models"
]
