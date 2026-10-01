# Rule-Based Astrochemical Knowledge System — V1

## Final AI PBL implementation

This project is a **Python rule-based expert system** with:

- JSON knowledge representation
- forward-chaining inference
- explanation trace
- manual astrochemical input
- NASA Exoplanet Archive data-backed input
- Tkinter + ttk GUI
- insufficient-data handling
- automated tests
- reproducible demo scenarios

The NASA pathway is an **additional source of facts**. It does not replace the original manual input pathway.

## Important scientific scope

The system does **not** claim that bulk exoplanet parameters prove the existence of specific molecules.

NASA Exoplanet Archive values are used to construct simple, transparent environmental facts such as:

- cool / moderate / hot equilibrium-temperature regime
- Earth-sized / intermediate-sized / giant-sized radius regime
- combined environmental profile

The final output explicitly states when atmospheric composition cannot be inferred from the available data.

## Why a local NASA snapshot?

A live network call can fail during a classroom demonstration. V1 therefore ships with a small local CSV snapshot whose source URLs and retrieval date are recorded.

This should be described as:

**"NASA Exoplanet Archive data-backed inference"**

not "real-time NASA data".

## Run

```bash
python app.py
```

## Tests

```bash
python -m unittest discover -s tests -v
```

## Project structure

```text
astrochemical_knowledge_system_v1/
├── app.py
├── README.md
├── requirements.txt
├── data/
│   ├── rules.json
│   └── nasa_exoplanet_snapshot.csv
├── src/
│   ├── __init__.py
│   ├── engine.py
│   ├── knowledge_base.py
│   ├── nasa_data.py
│   └── gui.py
├── tests/
│   ├── test_engine.py
│   └── test_nasa_data.py
└── docs/
    ├── CHANGE_AUDIT.md
    ├── DEMO_GUIDE.md
    ├── PROJECT_OVERVIEW.md
    ├── SCIENCE_SCOPE.md
    └── VIVA_QA.md
```

## V1 data flow

```text
Manual input ─────────────┐
                         ├─> normalized facts
NASA snapshot record ─────┘
                              ↓
                        JSON rule base
                              ↓
                       forward chaining
                              ↓
                         derived facts
                              ↓
                       explanation trace
                              ↓
                          Tkinter GUI
```

## Freeze point

V1 is intended as the academic PBL submission.

Future work can add richer astrochemical ontologies, literature-backed reaction rules, spectroscopy evidence, uncertainty, and additional astronomical datasets without changing the basic expert-system architecture.

## Public web demo

A static browser demo is included under `web/` for Vercel. The primary PBL implementation remains the Python/Tkinter desktop application. Set Vercel Root Directory to `web` and Framework Preset to `Other`.

## Optional Streamlit frontend

A Python web interface is included as `streamlit_app.py`.

It reuses the same JSON knowledge base, NASA snapshot and forward-chaining engine used by the desktop application.

Run it with:

```bash
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

The Streamlit version has the same three conceptual sections as the verified web demo:

- Manual Astrochemistry
- NASA Exoplanet Data
- Method & Scope

The Tkinter + ttk application remains the primary desktop implementation.
