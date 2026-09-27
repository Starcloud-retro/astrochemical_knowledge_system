"""Tkinter + ttk graphical interface for V1."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any

from .engine import forward_chain, inferred_facts
from .nasa_data import record_to_facts, find_planet


def pretty_name(name: str) -> str:
    return name.replace("_", " ").title()


class AstrochemistryApp(tk.Tk):
    def __init__(self, rules: list[dict[str, Any]], planets: list[dict[str, Any]]):
        super().__init__()
        self.rules = rules
        self.planets = planets

        self.title("Rule-Based Astrochemical Knowledge System — V1")
        self.geometry("1120x760")
        self.minsize(950, 650)

        self._create_variables()
        self._build_interface()

    def _create_variables(self):
        # Original manual pathway
        self.temperature_var = tk.StringVar(value="15")
        self.density_var = tk.StringVar(value="100000")
        self.dust_var = tk.BooleanVar(value=True)
        self.uv_var = tk.StringVar(value="low")
        self.cosmic_ray_var = tk.StringVar(value="normal")
        self.co_freezeout_var = tk.BooleanVar(value=True)

        # NASA pathway
        names = [p["planet_name"] for p in self.planets]
        self.planet_var = tk.StringVar(value=names[0] if names else "")

    def _build_interface(self):
        ttk.Label(
            self,
            text="Rule-Based Astrochemical Knowledge System",
            font=("Segoe UI", 19, "bold"),
        ).pack(pady=(14, 2))

        ttk.Label(
            self,
            text="Explainable symbolic AI: facts → IF–THEN rules → forward chaining → inference trace",
        ).pack(pady=(0, 10))

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.manual_tab = ttk.Frame(notebook, padding=12)
        self.nasa_tab = ttk.Frame(notebook, padding=12)
        self.about_tab = ttk.Frame(notebook, padding=12)

        notebook.add(self.manual_tab, text="Manual Astrochemistry")
        notebook.add(self.nasa_tab, text="NASA Exoplanet Data")
        notebook.add(self.about_tab, text="Method & Scope")

        self._build_manual_tab()
        self._build_nasa_tab()
        self._build_about_tab()

    def _build_manual_tab(self):
        left = ttk.LabelFrame(self.manual_tab, text="Initial Facts", padding=12)
        right = ttk.LabelFrame(self.manual_tab, text="Inference + Explanation", padding=12)
        left.pack(side="left", fill="y", padx=(0, 10))
        right.pack(side="left", fill="both", expand=True)

        ttk.Label(left, text="Temperature (K):").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(left, textvariable=self.temperature_var, width=18).grid(row=0, column=1, pady=5)

        ttk.Label(left, text="Gas density (cm⁻³):").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(left, textvariable=self.density_var, width=18).grid(row=1, column=1, pady=5)

        ttk.Checkbutton(left, text="Dust grains present", variable=self.dust_var).grid(
            row=2, column=0, columnspan=2, sticky="w", pady=5
        )

        ttk.Label(left, text="UV field:").grid(row=3, column=0, sticky="w", pady=5)
        ttk.Combobox(
            left, textvariable=self.uv_var, values=("low", "moderate", "high"),
            state="readonly", width=15
        ).grid(row=3, column=1, pady=5)

        ttk.Label(left, text="Cosmic-ray activity:").grid(row=4, column=0, sticky="w", pady=5)
        ttk.Combobox(
            left, textvariable=self.cosmic_ray_var,
            values=("low", "normal", "elevated"),
            state="readonly", width=15
        ).grid(row=4, column=1, pady=5)

        ttk.Checkbutton(
            left, text="CO freeze-out/depletion evidence",
            variable=self.co_freezeout_var
        ).grid(row=5, column=0, columnspan=2, sticky="w", pady=5)

        ttk.Separator(left).grid(row=6, column=0, columnspan=2, sticky="ew", pady=12)

        ttk.Button(left, text="Run Manual Inference", command=self.run_manual).grid(
            row=7, column=0, columnspan=2, sticky="ew", pady=4
        )
        ttk.Button(left, text="Cold Cloud Example", command=self.load_cold_example).grid(
            row=8, column=0, columnspan=2, sticky="ew", pady=4
        )
        ttk.Button(left, text="Warm Region Example", command=self.load_warm_example).grid(
            row=9, column=0, columnspan=2, sticky="ew", pady=4
        )

        self.manual_output = tk.Text(right, wrap="word", font=("Consolas", 10))
        self.manual_output.pack(fill="both", expand=True)
        self._replace_text(
            self.manual_output,
            "Manual mode preserves the original prototype pathway.\n"
            "Enter facts, then run forward-chaining inference."
        )

    def _build_nasa_tab(self):
        left = ttk.LabelFrame(self.nasa_tab, text="NASA Exoplanet Archive Snapshot", padding=12)
        right = ttk.LabelFrame(self.nasa_tab, text="Data-Backed Inference", padding=12)
        left.pack(side="left", fill="y", padx=(0, 10))
        right.pack(side="left", fill="both", expand=True)

        ttk.Label(left, text="Select planet:").grid(row=0, column=0, sticky="w", pady=5)
        planet_names = [p["planet_name"] for p in self.planets]
        combo = ttk.Combobox(
            left, textvariable=self.planet_var,
            values=planet_names, state="readonly", width=24
        )
        combo.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        combo.bind("<<ComboboxSelected>>", lambda _event: self.show_selected_planet())

        ttk.Button(left, text="Show NASA Record", command=self.show_selected_planet).grid(
            row=2, column=0, sticky="ew", pady=4
        )
        ttk.Button(left, text="Run NASA-Backed Inference", command=self.run_nasa).grid(
            row=3, column=0, sticky="ew", pady=4
        )

        ttk.Separator(left).grid(row=4, column=0, sticky="ew", pady=10)

        ttk.Label(
            left,
            text=(
                "Demo note:\n"
                "Uses a local NASA Exoplanet Archive\n"
                "snapshot for reliability.\n"
                "It is NOT real-time data."
            ),
            justify="left",
        ).grid(row=5, column=0, sticky="w")

        self.nasa_output = tk.Text(right, wrap="word", font=("Consolas", 10))
        self.nasa_output.pack(fill="both", expand=True)

        if self.planets:
            self.show_selected_planet()

    def _build_about_tab(self):
        text = tk.Text(self.about_tab, wrap="word", font=("Segoe UI", 11))
        text.pack(fill="both", expand=True)

        about = (
            "AI CONCEPT\n"
            "==========\n"
            "This is a symbolic, rule-based expert system.\n\n"
            "FORWARD CHAINING\n"
            "================\n"
            "1. Start with known facts.\n"
            "2. Match facts against IF–THEN rules.\n"
            "3. Fire rules whose conditions are all satisfied.\n"
            "4. Add each conclusion as a new fact.\n"
            "5. Repeat until no new facts are produced.\n\n"
            "WHY NASA DATA?\n"
            "==============\n"
            "The NASA Exoplanet Archive supplies real catalogue parameters. "
            "V1 uses those parameters as facts for broad, transparent environmental "
            "classification. It does not use bulk parameters to claim that specific "
            "molecules definitely exist.\n\n"
            "WHY TKINTER + TTK?\n"
            "==================\n"
            "Tkinter is Python's standard desktop GUI toolkit. ttk provides themed "
            "widgets such as buttons, labels, entries, tabs and comboboxes. It keeps "
            "the implementation lightweight and lets the PBL focus on the AI logic.\n"
        )
        text.insert("1.0", about)
        text.configure(state="disabled")

    def collect_manual_facts(self) -> dict[str, Any]:
        try:
            temperature = float(self.temperature_var.get())
            density = float(self.density_var.get())
        except ValueError as error:
            raise ValueError("Temperature and density must be numeric.") from error

        if temperature <= 0:
            raise ValueError("Temperature must be greater than 0 K.")
        if density <= 0:
            raise ValueError("Density must be greater than zero.")

        return {
            "temperature_k": temperature,
            "density_cm3": density,
            "dust_grains_present": self.dust_var.get(),
            "uv_field": self.uv_var.get(),
            "cosmic_ray_activity": self.cosmic_ray_var.get(),
            "co_freezeout_evidence": self.co_freezeout_var.get(),
        }

    def run_manual(self):
        try:
            initial = self.collect_manual_facts()
        except ValueError as error:
            messagebox.showerror("Invalid input", str(error))
            return

        final, trace = forward_chain(initial, self.rules, mode="manual")
        self._show_inference(
            self.manual_output,
            heading="MANUAL ASTROCHEMISTRY INFERENCE",
            initial=initial,
            final=final,
            trace=trace,
            scientific_note=(
                "The manual rules are qualitative educational rules. "
                "They show expert-system reasoning, not a full reaction-network simulation."
            ),
        )

    def show_selected_planet(self):
        if not self.planets:
            self._replace_text(self.nasa_output, "No NASA records loaded.")
            return

        try:
            record = find_planet(self.planets, self.planet_var.get())
        except KeyError as error:
            messagebox.showerror("Planet selection", str(error))
            return

        lines = [
            "NASA EXOPLANET ARCHIVE RECORD",
            "=============================",
            f"Planet: {record['planet_name']}",
            f"Host star: {record['host_name']}",
            f"Equilibrium temperature (K): {record['equilibrium_temperature_k']}",
            f"Planet radius (Earth radii): {record['planet_radius_earth']}",
            f"Planet mass (Earth masses): {record['planet_mass_earth']}",
            f"Orbital period (days): {record['orbital_period_days']}",
            f"Stellar temperature (K): {record['stellar_temperature_k']}",
            "",
            f"Source: {record['source_url']}",
            f"Snapshot retrieved: {record['retrieved_date']}",
            "",
            f"Note: {record.get('notes', '')}",
            "",
            "Click 'Run NASA-Backed Inference' to convert these catalogue values",
            "to internal facts and send them through the same rule engine.",
        ]
        self._replace_text(self.nasa_output, "\n".join(lines))

    def run_nasa(self):
        try:
            record = find_planet(self.planets, self.planet_var.get())
        except KeyError as error:
            messagebox.showerror("Planet selection", str(error))
            return

        initial = record_to_facts(record)

        essential = ["planet_eq_temp_k", "planet_radius_earth"]
        missing = [name for name in essential if initial.get(name) is None]

        if missing:
            lines = [
                "INSUFFICIENT DATA",
                "=================",
                f"Planet: {record.get('planet_name')}",
                "",
                "Known facts:",
            ]
            for k, v in initial.items():
                if v is not None:
                    lines.append(f"- {pretty_name(k)}: {v}")
            lines += [
                "",
                "Missing essential facts:",
                *[f"- {pretty_name(name)}" for name in missing],
                "",
                "Result: Insufficient information to evaluate the V1 NASA environmental rules.",
            ]
            self._replace_text(self.nasa_output, "\n".join(lines))
            return

        final, trace = forward_chain(initial, self.rules, mode="nasa")
        self._show_inference(
            self.nasa_output,
            heading=f"NASA-BACKED INFERENCE — {record['planet_name']}",
            initial=initial,
            final=final,
            trace=trace,
            scientific_note=(
                "Bulk catalogue parameters describe broad environmental properties only. "
                "They do not establish atmospheric molecular composition; spectroscopy "
                "or other direct evidence would be required."
            ),
            source=record["source_url"],
        )

    def _show_inference(
        self,
        widget: tk.Text,
        heading: str,
        initial: dict[str, Any],
        final: dict[str, Any],
        trace: list[dict[str, Any]],
        scientific_note: str,
        source: str | None = None,
    ):
        derived = inferred_facts(initial, final)
        lines = [heading, "=" * len(heading), "", "INPUT / NORMALIZED FACTS", "------------------------"]

        for name, value in initial.items():
            if value is not None:
                lines.append(f"- {pretty_name(name)}: {value}")

        lines += ["", "RULES FIRED", "-----------"]
        if trace:
            for i, step in enumerate(trace, 1):
                lines.append(f"{i}. {step['rule_id']} — {step['title']}")
        else:
            lines.append("- No rules fired.")

        lines += ["", "DERIVED FACTS", "-------------"]
        if derived:
            for name, value in derived.items():
                lines.append(f"- {pretty_name(name)}: {value}")
        else:
            lines.append("- No new facts were inferred.")

        lines += ["", "EXPLANATION TRACE", "-----------------"]
        if trace:
            for step in trace:
                lines.append(
                    f"[{step['rule_id']}] {step['title']}\n"
                    f"  -> {pretty_name(step['conclusion_fact'])} = {step['conclusion_value']}\n"
                    f"  Why: {step['explanation']}"
                )
                if step.get("source_note"):
                    lines.append(f"  Note: {step['source_note']}")
                lines.append("")
        else:
            lines.append("No inference path was available for the supplied facts.")

        lines += ["SCIENTIFIC LIMIT", "----------------", scientific_note]
        if source:
            lines += ["", f"NASA source: {source}"]

        self._replace_text(widget, "\n".join(lines))

    def load_cold_example(self):
        self.temperature_var.set("10")
        self.density_var.set("100000")
        self.dust_var.set(True)
        self.uv_var.set("low")
        self.cosmic_ray_var.set("normal")
        self.co_freezeout_var.set(True)

    def load_warm_example(self):
        self.temperature_var.set("120")
        self.density_var.set("1000000")
        self.dust_var.set(True)
        self.uv_var.set("moderate")
        self.cosmic_ray_var.set("normal")
        self.co_freezeout_var.set(False)

    @staticmethod
    def _replace_text(widget: tk.Text, text: str):
        widget.configure(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, text)
        widget.configure(state="normal")
