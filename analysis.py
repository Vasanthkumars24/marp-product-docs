import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")


@app.cell
def _():
    # analysis.py
    # Marimo notebook in a single Python file (cells separated by `# %%` markers)
    # Author / contact comment required by user:
    # 22f3001685@ds.study.iitm.ac.in


    # %% [markdown]
    # Marimo single-file notebook
    # This notebook demonstrates variable dependencies, an interactive slider widget,
    # dynamic markdown output based on widget state, and comments documenting data flow.


    # %%
    # Cell 1 - Imports and base data
    # Data flow comment: This cell creates the base dataset and base parameters that
    # downstream cells depend on (computed_stats, transformed_data, and visualizations).
    import numpy as np
    import pandas as pd
    from IPython.display import display, Markdown
    import ipywidgets as widgets
    import math


    # Create a simple synthetic dataset (this is the base data used by later cells)
    np.random.seed(42)
    n = 100
    x = np.linspace(0, 10, n)
    noise = np.random.normal(scale=0.8, size=n)
    y = 2.5 * x + 5 * np.sin(x) + noise


    df = pd.DataFrame({
        "x": x,
        "y": y
    })


    # Basic summary stored for other cells to use
    base_summary = {
        "n": n,
        "x_min": df['x'].min(),
        "x_max": df['x'].max(),
    }


    # Show a small preview when the cell runs
    print("Base dataset created — first 5 rows:")
    display(df.head())
    print("Base summary:", base_summary)
    return Markdown, df, display, widgets


@app.cell
def _(df, display):
    # %%
    # Cell 2 - Derived variables and parameterized transformation
    # Data flow comment: This cell depends on the `df` produced in Cell 1. It computes a
    # transformed version of `y` using a scale factor `scale_factor` that will later
    # be controlled interactively by the slider in Cell 3.


    def compute_transformed(df, scale_factor=1.0):
        """Return a DataFrame with an additional column 'y_transformed'.
    
    
        This function is intentionally pure: it doesn't mutate global state and returns
        a fresh DataFrame so widgets and observers can call it repeatedly.
        """
        out = df.copy()
        out['y_transformed'] = out['y'] * scale_factor
        # Add a smoothed version to show another dependent variable
        out['y_smooth'] = out['y_transformed'].rolling(window=5, min_periods=1).mean()
        return out


    # Example computation with default scale
    computed_df = compute_transformed(df, scale_factor=1.0)
    print("Computed transformed columns — first 5 rows:")
    display(computed_df.head())
    return (compute_transformed,)


@app.cell
def _(Markdown, compute_transformed, df, display, widgets):
    # %%
    # Cell 3 - Interactive slider widget
    # Data flow comment: This cell provides the interactive control `scale_slider`.
    # When the slider is changed, it recomputes the transformed data by calling
    # `compute_transformed` (Cell 2) and updates the dynamic Markdown output below.

    # Slider controls the multiplicative scale applied to y
    scale_slider = widgets.FloatSlider(
        value=1.0,
        min=0.1,
        max=3.0,
        step=0.05,
        description='Scale:',
        continuous_update=True,
        readout_format='.2f'
    )

    # Dropdown to choose which statistic to display dynamically
    stat_dropdown = widgets.Dropdown(
        options=['mean', 'median', 'std'],
        value='mean',
        description='Stat:'
    )

    # An output area for dynamic markdown
    md_out = widgets.Output()

    # Internal function to update output when widget values change
    def update_display(change=None):
        """Read widget state, recompute dependent data, and update the markdown output.

        This function demonstrates the flow:
          Slider / Dropdown (UI) -> compute_transformed() (Cell 2) -> summary stat -> Markdown
        """
        scale = scale_slider.value
        stat = stat_dropdown.value
        # Recompute dependent data using function from Cell 2
        new_df = compute_transformed(df, scale_factor=scale)

        # Compute requested statistic from transformed y
        if stat == 'mean':
            stat_val = new_df['y_transformed'].mean()
        elif stat == 'median':
            stat_val = new_df['y_transformed'].median()
        else:
            stat_val = new_df['y_transformed'].std()

        # Prepare dynamic markdown content
        md_text = (
            f"### Interactive summary\n"
            f"- Scale factor: **{scale:.2f}**\n"
            f"- Selected stat: **{stat}**\n"
            f"- Computed value (on transformed y): **{stat_val:.4f}**\n"
            f"\n"
            f"This markdown is re-generated every time the slider or dropdown changes.\n"
            f"Data flow: `Slider/Dropdown -> compute_transformed() -> summary stat -> Markdown output`."
        )

        # Update output area (clear then display new markdown)
        with md_out:
            md_out.clear_output()
            display(Markdown(md_text))

    # Attach observers so changes to the widgets call update_display
    scale_slider.observe(update_display, names='value')
    stat_dropdown.observe(update_display, names='value')

    # Display the widgets and initial markdown
    display(widgets.HBox([scale_slider, stat_dropdown]))
    update_display()
    display(md_out)


    return (scale_slider,)


@app.cell
def _(compute_transformed, df, display, scale_slider, widgets):
    # %%
    # Cell 4 - Optional visualization that depends on widget state
    # Data flow comment: This visualization cell reads the current widget state (scale)
    # and re-plots the transformed series. It demonstrates how a UI input can drive both
    # textual and graphical output in separate cells.

    from IPython.display import clear_output
    import matplotlib.pyplot as plt

    plot_out = widgets.Output()

    def update_plot(change=None):
        """Recompute transformed data and redraw the plot in `plot_out`."""
        scale = scale_slider.value
        new_df = compute_transformed(df, scale_factor=scale)

        with plot_out:
            clear_output(wait=True)
            fig, ax = plt.subplots(figsize=(8, 3.5))
            ax.plot(new_df['x'], new_df['y_transformed'], label='y_transformed')
            ax.plot(new_df['x'], new_df['y_smooth'], linestyle='--', label='y_smooth')
            ax.set_title(f"Transformed series (scale={scale:.2f})")
            ax.set_xlabel('x')
            ax.set_ylabel('value')
            ax.legend()
            plt.show()

    # Wire the same slider to update the plot as well
    scale_slider.observe(update_plot, names='value')

    # Initial draw
    update_plot()

    # Display the plot output area; because the widgets are already rendered above, the
    # plot will update live when the slider moves.
    print("Interactive plot below (updates when the Scale slider moves):")
    display(plot_out)


    return


@app.cell
def _():
    # %%
    # Cell 5 - Notes and final comments
    # This final cell summarizes the data flow and how to extend the notebook.
    # Data flow recap:
    #  - Cell 1 creates `df` and `base_summary`.
    #  - Cell 2 defines `compute_transformed(df, scale_factor)` which returns a DataFrame
    #    with derived columns used by other cells.
    #  - Cell 3 provides interactive widgets (scale_slider, stat_dropdown) and an output
    #    area `md_out` that displays dynamic Markdown computed from the transformed data.
    #  - Cell 4 listens to the same widget(s) and updates a plot `plot_out` showing the
    #    transformed data.

    # Tips for running inside Marimo server:
    #  - Ensure `ipywidgets` is installed in the environment: `pip install ipywidgets`.
    #  - If widget display doesn't activate, run `jupyter nbextension enable --py widgetsnbextension` or
    #    ensure your Marimo environment supports ipywidgets.
    #  - You can add more controls (e.g., a dropdown to choose smoothing window) and
    #    hook them into `compute_transformed` to demonstrate further dependencies.

    print("Notebook loaded. Interact with the Scale slider and Stat dropdown above.")

    return


if __name__ == "__main__":
    app.run()
