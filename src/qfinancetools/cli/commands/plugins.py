from __future__ import annotations

import json
import typer

from qfinancetools.core.plugins import discover_plugins
from qfinancetools.cli.renderers.plugins import render_plugins


plugins_app = typer.Typer(no_args_is_help=True)


@plugins_app.command("list")
def list_plugins(
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    snapshot = discover_plugins()
    if as_json:
        typer.echo(json.dumps(snapshot.model_dump(), indent=2))
        return
    render_plugins(snapshot)
