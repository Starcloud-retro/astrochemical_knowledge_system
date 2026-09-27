import json
import unittest
from pathlib import Path

from src.engine import compare, forward_chain, inferred_facts
from src.knowledge_base import load_rules


ROOT = Path(__file__).resolve().parents[1]
RULES = load_rules(ROOT / "data" / "rules.json")


class CompareTests(unittest.TestCase):
    def test_comparisons(self):
        self.assertTrue(compare(10, "<=", 20))
        self.assertTrue(compare(100000, ">=", 10000))
        self.assertTrue(compare("normal", "in", ["normal", "elevated"]))
        self.assertFalse(compare(30, "<", 20))


class ForwardChainTests(unittest.TestCase):
    def test_manual_chain(self):
        initial = {
            "temperature_k": 10,
            "density_cm3": 100000,
            "dust_grains_present": True,
            "uv_field": "low",
            "cosmic_ray_activity": "normal",
            "co_freezeout_evidence": True,
        }
        final, trace = forward_chain(initial, RULES, mode="manual")
        self.assertTrue(final["grain_surface_chemistry_favored"])
        self.assertTrue(final["co_surface_hydrogenation_favored"])
        self.assertTrue(final["methanol_ice_formation_plausible"])
        self.assertIn("M01", [step["rule_id"] for step in trace])
        self.assertIn("M04", [step["rule_id"] for step in trace])

    def test_nasa_hot_giant_chain(self):
        initial = {
            "planet_eq_temp_k": 1450,
            "planet_radius_earth": 15.58,
        }
        final, trace = forward_chain(initial, RULES, mode="nasa")
        self.assertEqual(final["planet_thermal_regime"], "hot")
        self.assertEqual(final["planet_size_regime"], "giant_size")
        self.assertEqual(final["nasa_environment_profile"], "hot_giant")
        self.assertEqual(
            final["composition_inference_status"],
            "not_determined_from_bulk_parameters",
        )

    def test_nasa_missing_temperature_does_not_invent_thermal_regime(self):
        initial = {"planet_radius_earth": 2.1}
        final, _ = forward_chain(initial, RULES, mode="nasa")
        self.assertNotIn("planet_thermal_regime", final)

    def test_inferred_facts(self):
        initial = {"a": 1}
        final = {"a": 1, "b": 2}
        self.assertEqual(inferred_facts(initial, final), {"b": 2})


if __name__ == "__main__":
    unittest.main()
