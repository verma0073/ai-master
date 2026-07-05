"""
Command-line interface for the Prompt Library.

Usage:
    python cli.py list
    python cli.py list --category coding
    python cli.py show code-review-strict
    python cli.py render code-review-strict --var language=python --var code_snippet="print(1)"
    python cli.py search sql

Why a CLI at all, in a project whose "real" consumers will be Python imports:
    A CLI is the fastest way to manually sanity-check a prompt renders
    correctly before wiring it into an app, and it's a natural demo artifact
    for a portfolio / interview walkthrough ("let me show you the library").
"""

from __future__ import annotations

from pathlib import Path

import typer

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root, so `shared` imports work

from shared.prompts import PromptLibrary, PromptNotFoundError, PromptRenderError, PromptValidationError

app = typer.Typer(help="AI Master Prompt Library CLI")
PROMPTS_DIR = Path(__file__).parent / "prompts"


def _library() -> PromptLibrary:
    try:
        return PromptLibrary(PROMPTS_DIR)
    except PromptValidationError as e:
        typer.secho(str(e), fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command("list")
def list_prompts(
    category: str = typer.Option(None, help="Filter by category"),
    tag: str = typer.Option(None, help="Filter by tag"),
):
    lib = _library()
    prompts = lib.list(category=category, tag=tag)
    if not prompts:
        typer.echo("No prompts match that filter.")
        raise typer.Exit()
    for p in prompts:
        typer.echo(f"{p.id:<28} v{p.version:<8} [{p.category}]  {p.name}")


@app.command("show")
def show_prompt(prompt_id: str, version: str = typer.Option(None)):
    lib = _library()
    try:
        p = lib.get(prompt_id, version)
    except PromptNotFoundError as e:
        typer.secho(str(e), fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.echo(f"{p.name} (v{p.version})")
    typer.echo(p.description)
    typer.echo(f"Tags: {', '.join(p.tags)}")
    typer.echo("Variables:")
    for v in p.variables:
        req = "required" if v.required else f"optional, default={v.default!r}"
        typer.echo(f"  - {v.name} ({v.type.value}, {req}): {v.description}")
    typer.echo("---\nTemplate:\n" + p.template)


@app.command("render")
def render_prompt(
    prompt_id: str,
    var: list[str] = typer.Option([], help="key=value, repeatable"),
    version: str = typer.Option(None),
):
    lib = _library()
    kwargs = {}
    for item in var:
        if "=" not in item:
            typer.secho(f"Invalid --var '{item}', expected key=value", fg=typer.colors.RED)
            raise typer.Exit(code=1)
        k, v = item.split("=", 1)
        kwargs[k] = v

    try:
        rendered = lib.render(prompt_id, version=version, **kwargs)
    except (PromptNotFoundError, PromptRenderError) as e:
        typer.secho(str(e), fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.echo(rendered)


@app.command("search")
def search_prompts(query: str):
    lib = _library()
    results = lib.search(query)
    if not results:
        typer.echo("No matches.")
        raise typer.Exit()
    for p in results:
        typer.echo(f"{p.id:<28} {p.name} — {p.description.strip().splitlines()[0]}")


if __name__ == "__main__":
    app()
