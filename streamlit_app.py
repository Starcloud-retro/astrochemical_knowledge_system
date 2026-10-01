
"""Streamlit web interface for the Rule-Based Astrochemical Knowledge System.

This is an optional frontend. It reuses the same:
- data/rules.json
- src/knowledge_base.py
- src/engine.py
- src/nasa_data.py

No separate AI logic is implemented here.
"""

from pathlib import Path

import streamlit as st

from src.engine import forward_chain, inferred_facts
from src.knowledge_base import load_rules
from src.nasa_data import load_exoplanet_snapshot, find_planet, record_to_facts


ROOT = Path(__file__).resolve().parent


@st.cache_data
def get_rules():
    return load_rules(ROOT / "data" / "rules.json")


@st.cache_data
def get_planets():
    return load_exoplanet_snapshot(ROOT / "data" / "nasa_exoplanet_snapshot.csv")


def pretty_name(name: str) -> str:
    return name.replace("_", " ").title()


def show_inference(initial, final, trace, scientific_note):
    """Display the output produced by the existing inference engine."""
    derived = inferred_facts(initial, final)

    st.subheader("Input / Normalized Facts")
    for name, value in initial.items():
        if value is not None:
            st.write(f"**{pretty_name(name)}:** {value}")

    st.subheader("Rules Fired")
    if trace:
        for index, step in enumerate(trace, start=1):
            st.write(f"{index}. **{step['rule_id']} — {step['title']}**")
    else:
        st.info("No rules fired for the supplied facts.")

    st.subheader("Derived Facts")
    if derived:
        for name, value in derived.items():
            st.write(f"- **{pretty_name(name)}:** {value}")
    else:
        st.info("No new facts were inferred.")

    st.subheader("Explanation Trace")
    if trace:
        for step in trace:
            with st.expander(f"{step['rule_id']} — {step['title']}", expanded=False):
                st.write(
                    f"**Conclusion:** {pretty_name(step['conclusion_fact'])} "
                    f"= {step['conclusion_value']}"
                )
                st.write(f"**Why:** {step['explanation']}")
                if step.get("source_note"):
                    st.caption(step["source_note"])
    else:
        st.write("No inference path was available.")

    st.warning(scientific_note)


def manual_mode(rules):
    st.header("Manual Astrochemistry")
    st.caption(
        "Enter environmental facts. The same forward-chaining engine used by the desktop app "
        "checks the JSON rules and derives new facts."
    )

    left, right = st.columns([1, 1])

    with left:
        temperature = st.number_input(
            "Temperature (K)", min_value=1.0, value=15.0, step=1.0
        )
        density = st.number_input(
            "Gas density (cm⁻³)", min_value=1.0, value=100000.0, step=1000.0
        )
        dust = st.checkbox("Dust grains present", value=True)
        uv = st.selectbox("UV field", ["low", "moderate", "high"], index=0)
        cosmic = st.selectbox(
            "Cosmic-ray activity", ["low", "normal", "elevated"], index=1
        )
        co_freezeout = st.checkbox("CO freeze-out/depletion evidence", value=True)

        run = st.button("Run Manual Inference", type="primary")

    with right:
        st.markdown(
            """
            **AI method**

            `Facts → IF–THEN rules → Forward chaining → Derived facts → Explanation`

            This is a **symbolic expert system**, not a machine-learning model.
            """
        )

    if run:
        initial = {
            "temperature_k": float(temperature),
            "density_cm3": float(density),
            "dust_grains_present": bool(dust),
            "uv_field": uv,
            "cosmic_ray_activity": cosmic,
            "co_freezeout_evidence": bool(co_freezeout),
        }

        final, trace = forward_chain(initial, rules, mode="manual")
        show_inference(
            initial,
            final,
            trace,
            (
                "The manual rules are qualitative educational rules. "
                "They demonstrate expert-system reasoning and are not a complete "
                "astrochemical reaction-network simulation."
            ),
        )


def nasa_mode(rules, planets):
    st.header("NASA Exoplanet Data")
    st.caption(
        "Uses the project's local NASA Exoplanet Archive snapshot for a reliable, "
        "reproducible classroom demonstration. It is NASA-data-backed, not real-time."
    )

    names = [p["planet_name"] for p in planets]
    selected_name = st.selectbox("Select planet", names)

    record = find_planet(planets, selected_name)

    st.subheader("NASA Record")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Equilibrium Temp.", f"{record['equilibrium_temperature_k']} K")
    c2.metric("Radius", f"{record['planet_radius_earth']} R⊕")
    c3.metric(
        "Mass",
        "Missing" if record["planet_mass_earth"] is None
        else f"{record['planet_mass_earth']} M⊕",
    )
    c4.metric("Orbital Period", f"{record['orbital_period_days']} d")

    st.write(f"**Host star:** {record['host_name']}")
    st.write(f"**Source:** {record['source_url']}")
    st.write(f"**Snapshot retrieved:** {record['retrieved_date']}")
    if record.get("notes"):
        st.caption(record["notes"])

    if st.button("Run NASA-Backed Inference", type="primary"):
        initial = record_to_facts(record)

        required = ["planet_eq_temp_k", "planet_radius_earth"]
        missing = [name for name in required if initial.get(name) is None]

        if missing:
            st.error(
                "Insufficient data for the V1 NASA environmental rules. Missing: "
                + ", ".join(pretty_name(name) for name in missing)
            )
            return

        final, trace = forward_chain(initial, rules, mode="nasa")
        show_inference(
            initial,
            final,
            trace,
            (
                "Bulk catalogue parameters describe broad environmental properties only. "
                "They do not establish atmospheric molecular composition; spectroscopy "
                "or other direct evidence would be required."
            ),
        )


def method_scope():
    st.header("Method & Scope")
    st.markdown(
        """
        ### AI concept
        Classical **symbolic AI / expert system** using explicit IF–THEN production rules.

        ### Forward chaining
        1. Start with known facts.
        2. Check which rules are satisfied.
        3. Add each rule's conclusion as a new fact.
        4. Repeat until no new facts are produced.

        ### Knowledge representation
        The rules are stored in `data/rules.json`, while the reasoning algorithm is in
        `src/engine.py`. This keeps **domain knowledge separate from program logic**.

        ### Scientific scope
        The NASA pathway classifies only broad environmental regimes from catalogue
        parameters. It does **not** infer actual atmospheric molecular composition from
        bulk planet parameters.

        ### Frontends
        - **Tkinter + ttk:** primary desktop implementation
        - **Streamlit:** optional Python web interface
        - **Static Vercel demo:** lightweight browser mirror
        """
    )


def main():
    st.set_page_config(
        page_title="Rule-Based Astrochemical Knowledge System",
        page_icon="🌌",
        layout="wide",
    )

    st.title("Rule-Based Astrochemical Knowledge System")
    st.caption(
        "Facts → IF–THEN rules → forward chaining → explainable inference"
    )

    rules = get_rules()
    planets = get_planets()

    tab_manual, tab_nasa, tab_method = st.tabs(
        ["Manual Astrochemistry", "NASA Exoplanet Data", "Method & Scope"]
    )

    with tab_manual:
        manual_mode(rules)

    with tab_nasa:
        nasa_mode(rules, planets)

    with tab_method:
        method_scope()


if __name__ == "__main__":
    main()
