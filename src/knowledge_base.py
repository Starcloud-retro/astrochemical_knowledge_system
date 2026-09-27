"""Load and validate the JSON knowledge base."""

import json
from pathlib import Path
from typing import Any


def load_rules(path: str | Path) -> list[dict[str, Any]]:
    """Load rules and verify the minimum fields used by the inference engine."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Knowledge-base file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        payload = json.load(file)

    rules = payload.get("rules")
    if not isinstance(rules, list):
        raise ValueError("Knowledge base must contain a top-level 'rules' list.")

    required = {"id", "title", "conditions", "conclusion", "explanation"}

    seen_ids = set()
    for rule in rules:
        missing = required - set(rule)
        if missing:
            raise ValueError(
                f"Rule {rule.get('id', '<unknown>')} missing fields: {sorted(missing)}"
            )

        if rule["id"] in seen_ids:
            raise ValueError(f"Duplicate rule id: {rule['id']}")
        seen_ids.add(rule["id"])

        if not isinstance(rule["conditions"], list):
            raise ValueError(f"Rule {rule['id']} conditions must be a list.")
        if not isinstance(rule["conclusion"], dict):
            raise ValueError(f"Rule {rule['id']} conclusion must be an object.")

    return rules
