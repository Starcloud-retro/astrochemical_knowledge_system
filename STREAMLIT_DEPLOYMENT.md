# Streamlit Version

The Streamlit interface is an optional frontend for the same project.

It reuses:
- `src/engine.py`
- `src/knowledge_base.py`
- `src/nasa_data.py`
- `data/rules.json`
- `data/nasa_exoplanet_snapshot.csv`

It does not introduce a second inference engine.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy on Streamlit Community Cloud

1. Push this project to GitHub.
2. Open Streamlit Community Cloud.
3. Create a new app from the GitHub repository.
4. Main file path: `streamlit_app.py`
5. Deploy.

## Demo tabs

1. Manual Astrochemistry
2. NASA Exoplanet Data
3. Method & Scope

## Important scientific statement

The NASA mode uses the existing local NASA Exoplanet Archive snapshot.
It is data-backed and reproducible, but it is not a real-time API implementation.
