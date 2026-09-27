"""NASA Exoplanet Archive snapshot loading and normalization.

V1 deliberately uses a small local snapshot for demo reliability.
The source and retrieval metadata are stored in the CSV itself.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


NUMERIC_COLUMNS = {
    "equilibrium_temperature_k",
    "planet_radius_earth",
    "planet_mass_earth",
    "orbital_period_days",
    "stellar_temperature_k",
}


def _to_float(value: str) -> float | None:
    value = (value or "").strip()
    if value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def load_exoplanet_snapshot(path: str | Path) -> list[dict[str, Any]]:
    """Read the local NASA-backed CSV snapshot."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"NASA snapshot not found: {path}")

    records = []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        required = {
            "planet_name",
            "host_name",
            "equilibrium_temperature_k",
            "planet_radius_earth",
            "planet_mass_earth",
            "orbital_period_days",
            "stellar_temperature_k",
            "source_url",
            "retrieved_date",
        }
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"NASA snapshot is missing columns: {sorted(missing)}")

        for row in reader:
            clean = dict(row)
            for column in NUMERIC_COLUMNS:
                clean[column] = _to_float(clean.get(column, ""))
            records.append(clean)

    return records


def record_to_facts(record: dict[str, Any]) -> dict[str, Any]:
    """Convert one archive record to the internal fact representation."""
    return {
        "planet_name": record.get("planet_name"),
        "host_name": record.get("host_name"),
        "planet_eq_temp_k": record.get("equilibrium_temperature_k"),
        "planet_radius_earth": record.get("planet_radius_earth"),
        "planet_mass_earth": record.get("planet_mass_earth"),
        "orbital_period_days": record.get("orbital_period_days"),
        "stellar_temperature_k": record.get("stellar_temperature_k"),
        "data_source": "NASA Exoplanet Archive",
    }


def find_planet(records: list[dict[str, Any]], planet_name: str) -> dict[str, Any]:
    """Find one planet by exact display name."""
    for record in records:
        if record.get("planet_name") == planet_name:
            return record
    raise KeyError(f"Planet not found in local NASA snapshot: {planet_name}")
