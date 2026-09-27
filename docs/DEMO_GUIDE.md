# Tomorrow's Demo Guide

## 2-3 minute implementation explanation

"My project is a Rule-Based Astrochemical Knowledge System. It is a classical symbolic AI expert system.

First I represented domain knowledge as IF-THEN rules in a JSON knowledge base. JSON keeps the knowledge separate from the Python program.

Second I implemented a forward-chaining inference engine. It starts from known facts, checks which rules are satisfied, adds their conclusions as new facts, and repeats until no new facts are produced.

Third I added an explanation trace, so the system shows which rules fired and why each conclusion was reached.

Fourth I built the interface using Python Tkinter with ttk widgets. It is similar in purpose to Java AWT or Swing because it provides desktop windows, fields, buttons, tabs and output panels.

The original manual input pathway is preserved. For V1 I added a NASA Exoplanet Archive data-backed pathway. A small local snapshot of official catalogue parameters is normalized into the same internal fact format and passed to the same rule engine.

Importantly, I do not claim that planet temperature or radius proves that a molecule exists. The NASA rules only infer broad environmental categories, and the output explicitly says that atmospheric composition requires additional observations such as spectroscopy."

## Demo scenario 1 — NASA hot giant

1. Open **NASA Exoplanet Data**.
2. Select **HD 209458 b**.
3. Click **Run NASA-Backed Inference**.

Expected chain:
- equilibrium temperature -> hot
- radius -> giant_size
- hot + giant_size -> hot_giant
- composition -> not determined from bulk parameters

## Demo scenario 2 — NASA moderate intermediate-size

Select **Kepler-22 b**.

Expected:
- moderate thermal bin
- intermediate-size radius bin
- moderate_intermediate_size profile
- composition still not determined

## Demo scenario 3 — Manual cold cloud

Open **Manual Astrochemistry**.
Click **Cold Cloud Example** then **Run Manual Inference**.

Expected:
- grain-surface chemistry favored
- freeze-out plausible
- CO surface hydrogenation favored
- methanol-ice formation plausible
- cold dense shielded environment profile

## If asked why a static NASA snapshot

"Live internet access can fail during a classroom demonstration, so I use a local reproducible snapshot sourced from the NASA Exoplanet Archive. I describe it as NASA data-backed inference, not real-time data."

## If asked what is actually AI

"The AI is the symbolic knowledge representation and inference mechanism. The program derives new facts by applying explicit production rules through forward chaining, and it can explain its reasoning."
