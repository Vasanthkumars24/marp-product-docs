# 22f3001685@ds.study.iitm.ac.in
# analysis.py — Marimo-style interactive analysis notebook
# This file is written as a plain Python script with cell markers ("# %%") so
# it can be opened in editors that recognize code cells (VS Code, Jupyter, Marimo).

# %%
# Cell 1 — Imports and base dataset creation
# Data flow: this cell builds `base_df` which downstream cells will read and
# transform. Keep this cell lightweight so other cells can re-run quickly.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display, Markdown, clear_output
import ipywidgets as widgets

np.random.seed(42)

# Create a synthetic dataset: two correlated features (x, y) and a group label
n = 200
x = np.linspace(0, 10, n)
noise = np.random.normal(scale=1.0, size=n)
y = 2.5 * x + 5 + noise  # baseline linear relationship

base_df = pd.DataFrame({
    "x": x,
    "y": y,
})

# Show first rows (useful when running interactively)
print("base_df sample:")
display(base_df.head())

# %%
# Cell 2 — Derived variables and transformation (depends on `base_df`)
# Data flow: reads `base_df` and creates `derived_df`. Downstream widgets will
# modify parameters that change `derived_df` on-the-fly (via callback functions).

# A derived feature: a smoothed version of y using a moving average window.
# Window size will be controlled by a slider widget in the next cell.

def moving_average(series, window):
    if window <= 1:
        return series.copy()
    return series.rolling(window=window, center=True, min_periods=1).mean()

# Precompute a default derived dataframe with window=5
derived_df = base_df.copy()
derived_df["y_smooth"] = moving_average(base_df["y"], window=5)

print("derived_df columns:", derived_df.columns.tolist())

# %%
# Cell 3 — Interactive widgets and dynamic markdown output
# This cell creates the interactive slider widget and registers callbacks to
# update plots and markdown text. It depends on `derived_df` / `base_df`.

# Slider controls the smoothing window and a threshold that highlights points.
window_slider = widgets.IntSlider(value=5, min=1, max=31, step=2, description='MA window')
threshold_slider = widgets.FloatSlider(value=0.0, min=-5.0, max=15.0, step=0.1, description='y threshold')

# Output area for dynamic plot and markdown
out = widgets.Output()

# Helper: update function that recomputes derived variables and updates UI

def update(window, threshold):
    # Documenting data flow in comments:
    # 1. Read `base_df` (source of truth)
    # 2. Compute `y_smooth` using moving_average(window)
    # 3. Compute `above_thresh` boolean mask derived from `y` and `threshold`
    # 4. Render plot and dynamic markdown reflecting the current widget state

    df = base_df.copy()
    df["y_smooth"] = moving_average(df["y"], window=window)
    df["above_thresh"] = df["y"] > threshold

    # Compute simple summary statistics used for Markdown
    total = len(df)
    n_above = int(df["above_thresh"].sum())
    pct_above = 100.0 * n_above / total

    # Update UI
    with out:
        clear_output(wait=True)
        # Dynamic markdown that changes based on widget state
        md = f"### Interactive summary\n- Moving-average window: **{window}**\n- Threshold: **{threshold:.2f}**\n- Points above threshold: **{n_above}/{total} ({pct_above:.1f}%)**"
        display(Markdown(md))

        # Plot raw y and smoothed y; highlight points above threshold
        plt.figure(figsize=(8, 4))
        plt.scatter(df['x'], df['y'], alpha=0.6, label='y (raw)')
        plt.plot(df['x'], df['y_smooth'], linewidth=2, label='y (smoothed)')
        plt.scatter(df.loc[df['above_thresh'], 'x'], df.loc[df['above_thresh'], 'y'],
                    s=40, edgecolor='k', linewidth=0.6, label='above threshold')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

# Connect widgets to the update function using interactive_output
controls = widgets.HBox([window_slider, threshold_slider])
ui = widgets.VBox([controls, out])

# register callback
widgets.interactive_output(update, {'window': window_slider, 'threshold': threshold_slider})

# Display UI when run in a notebook environment
print("Interactive controls:")
ui

# %%
# Cell 4 — Example: programmatic access to current widget state
# This cell shows how another analysis cell could read the widget state and
# produce a table or export. It depends on the widget values defined above.

# Note: in a notebook, reading widget.value gives the current setting.
current_window = window_slider.value
current_threshold = threshold_slider.value

print(f"Current widget settings -> window={current_window}, threshold={current_threshold}")

# Recompute a small report dataframe showing first 10 rows with flags
report_df = base_df.copy()
report_df['y_smooth'] = moving_average(report_df['y'], window=current_window)
report_df['above_threshold'] = report_df['y'] > current_threshold

# The following display is useful during exploratory analysis.
display(report_df.head(10))

# End of notebook
# Comments: The cells were arranged so that base_df is computed once (Cell 1),
# Cell 2 defines transformation helpers and a default derived_df, Cell 3 is the
# interactive layer that recomputes derived variables on widget change, and
# Cell 4 demonstrates programmatic use of the current widget state for further
# analysis or export.
