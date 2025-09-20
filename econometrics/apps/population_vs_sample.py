# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "altair==5.5.0",
#     "marimo",
#     "numpy==2.2.3",
#     "pandas==2.2.3",
# ]
# [tool.marimo.display]
# theme = "dark"
# ///

import marimo

__generated_with = "0.11.5"
app = marimo.App(
    width="medium",
    layout_file="layouts/population_vs_sample.grid.json",
)


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    TEAL = '#56B4E9'
    GREEN = '#009E73'
    return GREEN, TEAL, mo, np, pd


@app.cell
def _():
    import altair as alt
    return (alt,)


@app.cell
def _(alt):
    _ = alt.theme.enable('dark')
    return


@app.cell
def _(mo):
    slider_width = mo.ui.slider(
        start=100,
        stop=2560,
        step=10,
        value=1000,
        label="Width",
        debounce=True,
        show_value=True,
        full_width=True,
    )

    slider_height = mo.ui.slider(
        start=50,
        stop=1440,
        step=10,
        value=300,
        label="Height",
        debounce=True,
        show_value=True,
        full_width=True,
    )
    return slider_height, slider_width


@app.cell(hide_code=True)
def _(mo):
    mo.md("""# Population vs sample""")
    return


@app.cell
def _(mo):
    distribution = mo.ui.dropdown(
        options=[
            "Normal",
            "Lognormal",
            "Poisson",
            "Binomial",
            "Exponential",
            "Uniform",
            "Beta",
            "Gamma",
            "Chi-squares",
            "Geometric",
        ],
        value="Normal",
        label="Distribution",
        # full_width=True
    )
    return (distribution,)


@app.cell
def _(distribution, np, pd):
    distribution
    _N = 100_000

    if distribution.value == "Normal":
        population = np.random.normal(0, 1, _N)
    elif distribution.value == "Lognormal":
        population = np.random.lognormal(mean=0, sigma=1, size=_N)
    elif distribution.value == "Poisson":
        population = np.random.poisson(lam=3, size=_N)
    elif distribution.value == "Binomial":
        population = np.random.binomial(n=10, p=0.5, size=_N)
    elif distribution.value == "Exponential":
        population = np.random.exponential(scale=1, size=_N)
    elif distribution.value == "Uniform":
        population = np.random.uniform(low=0, high=1, size=_N)
    elif distribution.value == "Beta":
        population = np.random.beta(a=2, b=5, size=_N)
    elif distribution.value == "Gamma":
        population = np.random.gamma(shape=2, scale=1, size=_N)
    elif distribution.value == "Chi-squares":
        population = np.random.chisquare(df=2, size=_N)
    elif distribution.value == "Geometric":
        population = np.random.geometric(p=0.5, size=_N)

    pop_df = pd.DataFrame({"values": population})
    return pop_df, population


@app.cell
def _(np):
    n_obs_steps = (
        np.linspace(0, 500, 11).tolist() + np.linspace(600, 5000, 45).tolist()
    )
    return (n_obs_steps,)


@app.cell
def _(distribution, mo, n_obs_steps):
    distribution
    n_obs_slider = mo.ui.slider(
        steps=n_obs_steps,
        debounce=True,
        value=0,
        label="Sample size",
        show_value=True,
        full_width=True,
    )
    return (n_obs_slider,)


@app.cell
def _(mo):
    sample_button = mo.ui.run_button(label="Sample")
    return (sample_button,)


@app.cell
def _(n_obs_slider, np, pd, population, sample_button):
    sample_button.value

    sample = int(n_obs_slider.value)
    vyber = np.random.choice(population, sample, replace=False)
    sample_df = pd.DataFrame({"values": vyber})
    return sample, sample_df, vyber


@app.cell
def _(
    GREEN,
    TEAL,
    alt,
    mo,
    pop_df,
    sample_df,
    slider_height,
    slider_width,
):
    num_bins = 60
    bin_width = (pop_df["values"].max() - pop_df["values"].min()) / num_bins
    bin_params = alt.Bin(
        step=bin_width, extent=(pop_df["values"].min(), pop_df["values"].max())
    )

    pop_hist = (
        alt.Chart(pop_df)
        .mark_bar()
        .encode(
            x=alt.X("values", bin=bin_params, title="Values"),
            y=alt.Y("count()", title="Count"),
            color=alt.value(TEAL),
        )
        .properties(
            width=slider_width.value,
            height=slider_height.value,
            title="Population",
        )
    )

    sample_hist = (
        alt.Chart(sample_df)
        .mark_bar()
        .encode(
            x=alt.X("values", bin=bin_params, title="Values"),
            y=alt.Y("count()", title="Count"),
            color=alt.value(GREEN),
        )
        .properties(
            width=slider_width.value, height=slider_height.value, title="Sample"
        )
    )

    combined_chart = mo.ui.altair_chart(
        alt
        .vconcat(pop_hist, sample_hist)
        .resolve_scale(x="shared")
        .configure_title(fontSize=16, anchor='middle')
        .configure_axis(titleFontSize=12, labelFontSize=10, grid=False)
        .configure_legend(titleFontSize=12, labelFontSize=10),
        chart_selection=False
    )
    return (
        bin_params,
        bin_width,
        combined_chart,
        num_bins,
        pop_hist,
        sample_hist,
    )


@app.cell
def _(distribution):
    distribution
    return


@app.cell
def _(n_obs_slider):
    n_obs_slider
    return


@app.cell
def _(sample_button):
    sample_button
    return


@app.cell
def _(combined_chart):
    combined_chart
    return


if __name__ == "__main__":
    app.run()
