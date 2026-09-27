# V0 -> V1 Change Audit

| Component | V0 state | V1 requirement | Change | Reason |
|---|---|---|---|---|
| Python application | Working | Preserve | MUST DO: preserved | Existing implementation is the baseline |
| Tkinter GUI | Working manual screen | Keep + add NASA mode | MUST DO | Faculty demo needs both manual and data-backed pathways |
| JSON knowledge base | Working | Preserve + extend | MUST DO | Same representation used for both pathways |
| Forward chaining | Working | Preserve | MUST DO: no redesign | Core AI method already valid |
| Explanation trace | Present | Make clearer | MUST DO | Demonstrates explainability |
| NASA data | Missing in V0 | Add reliable data-backed path | MUST DO | Previously promised extension |
| Insufficient-data state | Minimal/absent | Add basic handling | MUST DO | Prevents forced conclusions |
| Live NASA API | Not required | Optional future | FUTURE | Network dependency could make demo fragile |
| ML / LLM / RAG | Not present | Do not add | FUTURE / unnecessary | Outside project scope |
| Database | Not present | Do not add | FUTURE / unnecessary | No academic need |
| Advanced chemical network | Not present | Do not add now | FUTURE | Requires much stronger domain validation |

## Exact V1 additions

- `src/nasa_data.py`
- `data/nasa_exoplanet_snapshot.csv`
- NASA Exoplanet Data GUI tab
- method/scope GUI tab
- NASA-specific rule group in `rules.json`
- insufficient-data display
- NASA data tests
- final demo and viva documentation

## Core preserved architecture

`app.py -> loader -> GUI -> normalized facts -> rule engine -> trace`

The forward-chaining engine remains the same conceptual engine for both input pathways.
