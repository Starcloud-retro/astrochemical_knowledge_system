import unittest
from pathlib import Path

from src.nasa_data import (
    load_exoplanet_snapshot,
    find_planet,
    record_to_facts,
)


ROOT = Path(__file__).resolve().parents[1]


class NASADataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = load_exoplanet_snapshot(
            ROOT / "data" / "nasa_exoplanet_snapshot.csv"
        )

    def test_snapshot_loads(self):
        self.assertGreaterEqual(len(self.records), 3)

    def test_find_planet(self):
        record = find_planet(self.records, "Kepler-22 b")
        self.assertEqual(record["host_name"], "Kepler-22")

    def test_numeric_parsing(self):
        record = find_planet(self.records, "HD 209458 b")
        self.assertIsInstance(record["equilibrium_temperature_k"], float)
        self.assertGreater(record["equilibrium_temperature_k"], 1000)

    def test_missing_mass_remains_missing(self):
        record = find_planet(self.records, "Kepler-22 b")
        self.assertIsNone(record["planet_mass_earth"])

    def test_normalization(self):
        record = find_planet(self.records, "TRAPPIST-1 g")
        facts = record_to_facts(record)
        self.assertEqual(facts["data_source"], "NASA Exoplanet Archive")
        self.assertEqual(facts["planet_name"], "TRAPPIST-1 g")


if __name__ == "__main__":
    unittest.main()
