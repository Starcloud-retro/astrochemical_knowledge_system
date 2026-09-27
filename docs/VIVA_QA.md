# Likely Viva Questions

## What is an expert system?

A program that represents domain knowledge explicitly and applies an inference mechanism to reason from facts toward conclusions.

## What is forward chaining?

A data-driven inference strategy that begins with known facts, fires rules whose premises are satisfied, adds new conclusions as facts, and repeats until no new facts can be derived.

## Why JSON?

JSON provides a simple structured representation for rules while keeping domain knowledge separate from Python code.

## Why Tkinter?

It is Python's standard desktop GUI toolkit, requires no extra framework for this project, and is sufficient for forms, buttons, tabs and output panels.

## Why not Streamlit?

Streamlit is useful for browser-based data apps, but V1 does not need a web server or external package. Tkinter keeps the submission lightweight and focuses attention on the AI reasoning.

## Why NASA Exoplanet Archive?

It provides curated catalogue parameters for confirmed exoplanets and their host systems. V1 uses selected archive values as real scientific input facts.

## Does the system detect molecules on exoplanets?

No. Bulk parameters such as radius and equilibrium temperature are not enough to establish molecular composition. V1 explicitly avoids that claim.

## Why are temperature/radius thresholds simple?

They are project-defined demonstration bins to show transparent symbolic reasoning. They are not claimed as universal astronomical taxonomy.

## Is this machine learning?

No. It is symbolic AI. The rules are explicitly represented rather than learned from training data.

## What is future work?

Literature-backed astrochemical ontology, spectroscopy evidence, uncertainty, competing hypotheses, additional datasets and systematic scientific evaluation.
