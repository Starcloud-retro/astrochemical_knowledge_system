# Project Overview

## Title

**Rule-Based Astrochemical Knowledge System**

## AI concept

Classical symbolic AI / expert system.

## Core AI method

**Forward chaining** over explicit IF-THEN production rules.

## Knowledge representation

Rules are stored in JSON so the domain knowledge is separate from the Python inference algorithm.

## Input pathways

### 1. Manual astrochemical pathway

The user supplies qualitative/physical environmental facts such as temperature, gas density, dust, UV field, cosmic-ray activity and CO freeze-out evidence.

### 2. NASA Exoplanet Archive pathway

V1 ships with a small local snapshot of selected NASA Exoplanet Archive parameters.

Those catalogue values are normalized into internal facts and sent through the same rule engine.

## Why the NASA rules are conservative

Bulk parameters such as equilibrium temperature and radius do not prove which molecules exist in an atmosphere.

Therefore V1 only infers broad environmental bins/profiles and explicitly concludes that composition is not determined from those bulk parameters.

## Output

- input / normalized facts
- fired rules
- derived facts
- explanation trace
- scientific limitation statement

## GUI

Tkinter + ttk.

Tkinter plays a role similar to Java AWT/Swing: it provides a desktop window, buttons, text fields, tabs, comboboxes and output areas.

## Project status

V1 is the academic PBL submission version.

Richer astrochemical chemistry, spectroscopy and probabilistic reasoning are future research directions.
