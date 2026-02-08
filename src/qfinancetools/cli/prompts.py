from __future__ import annotations

import typer


def _parse_list(value: str) -> list[str]:
    cleaned = value.replace(",", " ")
    parts = [part.strip() for part in cleaned.split()]
    return [part for part in parts if part]


def prompt_float(label: str, default: float | None = None) -> float:
    if default is None:
        return float(typer.prompt(label))
    return float(typer.prompt(label, default=default))


def prompt_int(label: str, default: int | None = None) -> int:
    if default is None:
        return int(typer.prompt(label))
    return int(typer.prompt(label, default=default))


def prompt_bool(label: str, default: bool = False) -> bool:
    return bool(typer.prompt(label, default=default))


def prompt_list_float(label: str) -> list[float]:
    raw = typer.prompt(label)
    return [float(item) for item in _parse_list(raw)]


def prompt_list_int(label: str) -> list[int]:
    raw = typer.prompt(label)
    return [int(item) for item in _parse_list(raw)]


def prompt_optional_float(label: str) -> float | None:
    raw = typer.prompt(label, default="")
    raw = raw.strip()
    if not raw:
        return None
    return float(raw)
