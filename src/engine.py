"""Forward-chaining inference engine."""

from __future__ import annotations
from typing import Any

SUPPORTED_OPERATORS = {"==", "!=", "<", "<=", ">", ">=", "in"}


def compare(actual: Any, operator: str, expected: Any) -> bool:
    """Evaluate one condition comparison."""
    if operator not in SUPPORTED_OPERATORS:
        raise ValueError(f"Unsupported operator: {operator}")

    if operator == "==":
        return actual == expected
    if operator == "!=":
        return actual != expected
    if operator == "<":
        return actual < expected
    if operator == "<=":
        return actual <= expected
    if operator == ">":
        return actual > expected
    if operator == ">=":
        return actual >= expected
    if operator == "in":
        return actual in expected
    return False


def condition_is_true(condition: dict[str, Any], facts: dict[str, Any]) -> bool:
    """Return True when a required fact exists and satisfies the condition."""
    fact_name = condition["fact"]
    if fact_name not in facts or facts[fact_name] is None:
        return False

    return compare(
        facts[fact_name],
        condition.get("operator", "=="),
        condition["value"],
    )


def rule_is_satisfied(rule: dict[str, Any], facts: dict[str, Any]) -> bool:
    """A rule is satisfied only when ALL of its conditions are true."""
    return all(condition_is_true(c, facts) for c in rule["conditions"])


def forward_chain(
    initial_facts: dict[str, Any],
    rules: list[dict[str, Any]],
    mode: str | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Apply production rules repeatedly until no new facts are produced."""
    facts = {k: v for k, v in initial_facts.items() if v is not None}
    trace: list[dict[str, Any]] = []
    fired_rule_ids: set[str] = set()

    changed = True
    while changed:
        changed = False

        for rule in rules:
            if rule["id"] in fired_rule_ids:
                continue

            rule_mode = rule.get("mode")
            if mode and rule_mode and rule_mode != mode:
                continue

            if not rule_is_satisfied(rule, facts):
                continue

            conclusion = rule["conclusion"]
            name = conclusion["fact"]
            value = conclusion["value"]

            is_new = name not in facts or facts[name] != value
            facts[name] = value
            fired_rule_ids.add(rule["id"])

            trace.append(
                {
                    "rule_id": rule["id"],
                    "title": rule["title"],
                    "conclusion_fact": name,
                    "conclusion_value": value,
                    "explanation": rule["explanation"],
                    "source_note": rule.get("source_note", ""),
                }
            )

            if is_new:
                changed = True

    return facts, trace


def inferred_facts(
    initial_facts: dict[str, Any],
    final_facts: dict[str, Any],
) -> dict[str, Any]:
    """Return facts created by the inference process rather than user/data input."""
    return {
        k: v
        for k, v in final_facts.items()
        if k not in initial_facts and v is not None
    }


def missing_requirements(
    initial_facts: dict[str, Any],
    rules: list[dict[str, Any]],
    mode: str,
) -> list[str]:
    """List missing input fact names needed by rules for the selected mode.

    This is intentionally simple. It helps the GUI explain incomplete-data cases
    without introducing probabilistic reasoning.
    """
    missing = set()
    for rule in rules:
        if rule.get("mode") != mode:
            continue
        for condition in rule["conditions"]:
            name = condition["fact"]
            # Only report externally supplied facts, not facts expected to be derived
            # by earlier rules.
            if condition.get("input_fact", False):
                if name not in initial_facts or initial_facts.get(name) is None:
                    missing.add(name)
    return sorted(missing)
