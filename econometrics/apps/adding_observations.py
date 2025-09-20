# /// script
# requires-python = '>=3.12'
# dependencies = [
#     "marimo",
#     "altair==5.5.0",
#     "pandas==2.2.3",
#     "numpy==2.2.3",
# ]
#
# [tool.marimo.display]
# theme = "dark"
# ///

import marimo

__generated_with = "0.11.5"
app = marimo.App(
    width="medium",
    layout_file="layouts/adding_observations.grid.json",
)


@app.cell
def _():
    import marimo as mo
    import altair as alt
    import pandas as pd
    return alt, mo, pd


@app.cell
def _(alt):
    _ = alt.theme.enable('dark')
    return


@app.cell
def _(mo):
    import numpy as np

    mo.show_code()
    return (np,)


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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Least square regression""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""$$ \\hat{\\beta}_{ols} = (X^TX)^{-1}X^Ty $$""")
    return


@app.cell
def _(np):
    np.random.seed(11)
    N = 1_000
    x_min, x_max = 140, 210
    return N, x_max, x_min


@app.cell
def _(mo):
    N_slider = mo.ui.slider(
        start=3,
        stop=1_000,
        # debounce=True,
        value=10,
        label="Number of observations",
        full_width=True,
        show_value=True,
    )

    slider_width = mo.ui.slider(
        start=100,
        stop=2560,
        step=10,
        value=940,
        label="Width",
        debounce=True,
        show_value=True,
        full_width=True,
    )

    slider_height = mo.ui.slider(
        start=50,
        stop=1440,
        step=10,
        value=460,
        label="Height",
        debounce=True,
        show_value=True,
        full_width=True,
    )
    return N_slider, slider_height, slider_width


@app.cell
def _(N, np):
    height = np.floor(np.random.normal(loc=180, scale=10, size=N))
    weight = height // 3 + np.random.randint(low=0, high=50, size=N)
    const = np.ones(N)
    return const, height, weight


@app.cell
def _(N_slider, const, height, np, pd, weight):
    x = height[: N_slider.value]
    y = weight[: N_slider.value]
    c = const[: N_slider.value]
    X = np.column_stack((c, x))
    df = pd.DataFrame({"Height (cm)": x, "Weight (kg)": y})
    df["Height (cm)"] = df["Height (cm)"].astype(int)
    df["Weight (kg)"] = df["Weight (kg)"].astype(int)
    return X, c, df, x, y


@app.cell
def _(X, mo, np, y):
    intercept, slope = np.linalg.inv(X.T @ X) @ X.T @ y

    mo.show_code()
    return intercept, slope


@app.cell
def _(
    alt,
    df,
    intercept,
    mo,
    pd,
    slider_height,
    slider_width,
    slope,
    x_max,
    x_min,
):
    chart = (
        alt.Chart(df)
        .mark_circle(size=20)
        .encode(
            x=alt.X(
                "Height (cm)",
                axis=alt.Axis(format="d"),
                scale=alt.Scale(domain=(x_min, x_max)),
            ),
            y=alt.Y(
                "Weight (kg)",
                axis=alt.Axis(format="d"),
                scale=alt.Scale(domain=(50, 115)),
            ),
            tooltip=["Height (cm)", "Weight (kg)"],
            color=alt.value("#56B4E9"),
            stroke=alt.value("black"),
            strokeWidth=alt.value(1),
        )
    )

    abline_data = pd.DataFrame(
        {
            "Height (cm)": [x_min, x_max],
            "Weight (kg)": [slope * x_min + intercept, slope * x_max + intercept],
        }
    )

    abline = (
        alt.Chart(abline_data)
        .mark_line(color="#E69F00")
        .encode(x="Height (cm)", y="Weight (kg)")
    )

    final_chart = (
        (chart + abline)
        .configure_axis(titleFontSize=12, labelFontSize=10, grid=False)
        .properties(width=slider_width.value, height=slider_height.value)
    )

    final_altair_chart = mo.ui.altair_chart(final_chart, chart_selection=False)
    return abline, abline_data, chart, final_altair_chart, final_chart


@app.cell
def _(df, mo):
    weight_height_table = mo.ui.table(
        data=df,
        pagination=True,
        label="Dataframe with heights and weights",
        # selection=None,
        show_column_summaries=False,
    )
    return (weight_height_table,)


@app.cell
def _(weight_height_table):
    weight_height_table
    return


@app.cell
def _(mo):
    mo.md("""# Adding observations""")
    return


@app.cell
def _(mo):
    mo.md("""Number of observations""")
    return


@app.cell(hide_code=True)
def _(N_slider):
    N_slider
    return


@app.cell(hide_code=True)
def _(slider_width):
    slider_width
    return


@app.cell(hide_code=True)
def _(slider_height):
    slider_height
    return


@app.cell(hide_code=True)
def _(intercept, mo, slope):
    equation_ols = mo.md(
        f"""$$ \\widehat{{\\text{{Weight}}}} = {intercept:.2f}{slope:+.2f} \\text{{Height}} $$"""
    )
    return (equation_ols,)


@app.cell
def _(equation_ols):
    equation_ols
    return


@app.cell(hide_code=True)
def _(final_altair_chart):
    final_altair_chart
    return


if __name__ == "__main__":
    app.run()
