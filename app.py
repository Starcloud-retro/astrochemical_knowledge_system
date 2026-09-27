"""Application entry point."""

from pathlib import Path

from src.gui import AstrochemistryApp
from src.knowledge_base import load_rules
from src.nasa_data import load_exoplanet_snapshot


def main():
    project_root = Path(__file__).resolve().parent

    rules = load_rules(project_root / "data" / "rules.json")
    planets = load_exoplanet_snapshot(
        project_root / "data" / "nasa_exoplanet_snapshot.csv"
    )

    app = AstrochemistryApp(rules=rules, planets=planets)
    app.mainloop()


if __name__ == "__main__":
    main()
