# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "altair==5.5.0",
#     "numpy==2.2.3",
#     "pandas==2.2.3",
# ]
# [tool.marimo.display]
# theme = "dark"
# ///

import marimo

__generated_with = "0.11.5"
app = marimo.App(layout_file="layouts/estimator_properties.grid.json")


@app.cell
def _():
    # dodelat consistency. pridat ty unbiased tak, aby byl vzdycky vygenerovanej ten nejvic a dynamicky se to menilo
    # dodelat to sampl,e tlacitko
    return


@app.cell
def _(alt):
    _ = alt.theme.enable('dark')
    return


@app.cell
def _(mo):
    mo.md(r"""# Estimator properties""")
    return


@app.cell
def _(slider_cons):
    slider_cons
    return


@app.cell
def _(slider_sample):
    slider_sample
    return


@app.cell
def _(mo, slider_height, slider_width):
    mo.vstack([slider_height, slider_width])
    return


@app.cell
def _(slider_cons):
    slider_cons
    return


@app.cell
def _(mo):
    main_menu = mo.Html(
        f'<a href="https://kejtos.github.io/materials/" target="_parent" '
        f'style="display: inline-block; border: 1px solid #ccc; border-radius: 8px; padding: 4px 8px; font-size: 11px;">'
        f'{mo.icon("carbon:return")} Back to the menu</a>'
    )
    return (main_menu,)


@app.cell
def _(main_menu):
    main_menu.right()
    return


@app.cell
def _(b_reset, b_sample, b_show_e, mo):
    mo.hstack([b_sample, b_reset, b_show_e], justify="start")
    return


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import altair as alt
    return alt, mo, np, pd


@app.cell
def _(alt):
    _ = alt.theme.enable('dark')
    return


@app.cell
def _(np):
    heights = [
        190,
        173,
        174,
        178,
        163,
        163,
        163,
        184,
        173,
        178,
        180,
        185,
        158,
        182,
        190,
        185,
        190,
        180,
        173,
        185,
        174,
    ]

    population_heights = np.array(heights)
    population_mean = population_heights.mean()
    return heights, population_heights, population_mean


@app.cell
def _(mo, sample_sizes_full):
    slider_width = mo.ui.slider(
        start=100,
        stop=2560,
        step=10,
        value=920,
        label="Width",
        show_value=True,
        full_width=True,
    )

    slider_height = mo.ui.slider(
        start=50,
        stop=1440,
        step=10,
        value=350,
        label="Height",
        show_value=True,
        full_width=True,
    )

    slider_sample = mo.ui.slider(
        start=1,
        stop=500,
        step=1,
        value=1,
        show_value=True,
        full_width=True,
        debounce=True,
    ).form(label="Number of samples", bordered=False, submit_button_label='OK')

    slider_cons = mo.ui.slider(
        label="Number of distributions",
        start=1,
        stop=len(sample_sizes_full),
        step=1,
        value=1,
        show_value=True,
        full_width=True,
        debounce=True,
    )
    return slider_cons, slider_height, slider_sample, slider_width


@app.cell
def _(mo):
    mo.md(r"""Choose the number of samples first""")
    return


@app.cell
def _(mo):
    b_reset = mo.ui.run_button(label="Reset")

    b_show_e = mo.ui.button(
        label="Show E[X]", value=False, on_click=lambda value: not value
    )
    return b_reset, b_show_e


@app.cell
def _(b_reset, mo):
    b_reset
    b_sample = mo.ui.run_button(label="Sample")

    means_list = []
    means_list_2 = []
    return b_sample, means_list, means_list_2


@app.cell
def _(
    b_sample,
    means_list,
    means_list_2,
    mo,
    np,
    pd,
    population_heights,
    slider_sample,
):
    b_sample
    try:
        mo.stop(not b_sample.value)
        for _i in range(slider_sample.value):
            _sample_heights = np.random.choice(population_heights, 5, replace=True)
            _sum_heights = _sample_heights.sum()
            _N = _sample_heights.size
            _mean_1 = np.round(_sum_heights / _N, 2)
            _mean_2 = np.round(_sum_heights / (_N + 1), 2)
            means_list.append(_mean_1)
            means_list_2.append(_mean_2)
    except:
        pass

    means = pd.DataFrame(
        {
            "Mean sum/N": means_list,
            "Mean sum/(N+1)": means_list_2,
        }
    )
    mo.ui.table(means, show_column_summaries=False)
    return (means,)


@app.cell
def _(alt, means, slider_height, slider_width):
    base = (
        alt.Chart(
            means.rename(
                columns={"Mean sum/N": "sum/N", "Mean sum/(N+1)": "sum/(N+1)"}
            )
        )
        .transform_fold(["sum/N", "sum/(N+1)"], as_=["Calculation", "Estimates"])
        .transform_bin(field="Estimates", as_="bin_mean", bin=alt.Bin(maxbins=100))
        .encode(alt.Color("Calculation:N"))
        .properties(width=slider_width.value - 50, height=slider_height.value)
    )

    hist = base.mark_bar(opacity=0.5, binSpacing=0).encode(
        alt.X("bin_mean:Q", axis=alt.Axis(title="x̄")),
        alt.Y("count()", axis=alt.Axis(title="Count of x̄"), stack=None),
    )

    # rule = base.mark_rule(size=2).encode(alt.X('mean(Estimates):Q'),)
    return base, hist


@app.cell
def _(alt, b_show_e, hist, mo, population_mean):
    if b_show_e.value:
        rule = exp_value_line = (
            alt.Chart()
            .mark_rule(color="green", strokeWidth=3)
            .encode(x=alt.datum(population_mean))
        )
    else:
        rule = exp_value_line = (
            alt.Chart()
            .mark_rule(color="green", strokeWidth=0)
            .encode(x=alt.datum(population_mean))
        )

    plotos = (
        (hist + rule).configure_title(fontSize=16, anchor='middle')
        .configure_axis(titleFontSize=12, labelFontSize=10, grid=False)
        .configure_legend(titleFontSize=12, labelFontSize=10)
    )

    mo.output.replace(plotos)
    return exp_value_line, plotos, rule


@app.cell
def _(population_heights):
    means_list_cons = []
    population_std = population_heights.std()
    sample_sizes_full = [10, 20, 30, 50, 100]
    n_simulations = 10000

    colors = ["#115f9a", "#1984c5", "#22a7f0", "#48b5c4", "#76c68f"]
    # colors.reverse()
    return (
        colors,
        means_list_cons,
        n_simulations,
        population_std,
        sample_sizes_full,
    )


@app.cell
def _(
    n_simulations,
    np,
    pd,
    population_mean,
    population_std,
    sample_sizes_full,
    slider_cons,
):
    results = {}

    sample_sizes = sample_sizes_full[: slider_cons.value]
    for n in sample_sizes:
        biased_estimates = []
        unbiased_estimates = []

        for _ in range(n_simulations):
            sample = np.random.normal(
                loc=population_mean, scale=population_std, size=n
            )
            biased_estimate = np.sum(sample) / (n + 1)
            biased_estimates.append(biased_estimate)

        results[n] = biased_estimates

    _unbiased_estimates = []
    for _ in range(n_simulations):
        _sample = np.random.normal(
            loc=population_mean, scale=population_std, size=100
        )
        _unbiased_estimate = np.sum(_sample) / 100
        _unbiased_estimates.append(_unbiased_estimate)
        results["unbiased"] = _unbiased_estimates

    dictos = {f"{n} sampled": results[n] for n in sample_sizes}
    dictos["unbiased"] = results["unbiased"]
    df_biased = pd.DataFrame(dictos)
    return (
        biased_estimate,
        biased_estimates,
        df_biased,
        dictos,
        n,
        results,
        sample,
        sample_sizes,
        unbiased_estimates,
    )


@app.cell
def _(
    alt,
    colors,
    df_biased,
    sample_sizes,
    slider_cons,
    slider_height,
    slider_width,
):
    (
        alt.Chart(df_biased)
        .transform_fold(
            [f"{n} sampled" for n in sample_sizes] + ["unbiased"],
            as_=["Experiment", "Measurement"],
        )
        .mark_bar(opacity=0.5, binSpacing=0)
        .encode(
            alt.X(
                "Measurement:Q",
                axis=alt.Axis(title="x̄"),
                sort=[f"{n} sampled" for n in sample_sizes] + ["unbiased"],
            ).bin(maxbins=100),
            alt.Y("count()").stack(None),
            alt.Color("Experiment:N").scale(
                domain=[f"{n} sampled" for n in sample_sizes] + ["unbiased"],
                range=[*colors[: slider_cons.value], "orange"],
            ),
        )
        .configure_title(fontSize=16, anchor='middle')
        .configure_axis(titleFontSize=12, labelFontSize=10, grid=False)
        .configure_legend(titleFontSize=12, labelFontSize=10)
        .properties(width=slider_width.value - 70, height=slider_height.value)
    )
    # testos2 = alt.Chart().mark_rule(color="green", strokeWidth=3).encode(x=alt.datum(population_mean))

    # (testos+testos2)
    return


if __name__ == "__main__":
    app.run()
