# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "altair==5.5.0",
#     "marimo",
#     "numpy==2.2.3",
#     "polars==1.24.0",
# ]
# [tool.marimo.display]
# theme = "dark"
# ///

import marimo

__generated_with = "0.11.5"
app = marimo.App(
    width="medium",
    layout_file="layouts/changing_samples.grid.json",
)


@app.cell
def _(alt):
    _ = alt.theme.enable('dark')
    return


@app.cell
def _(mo):
    n_slider = mo.ui.slider(20, 500, 20, value=100, label='Sampled observations', full_width=True)
    sample_button = mo.ui.run_button(label='Change population')
    run_button = mo.ui.run_button(label='Run changes')
    return n_slider, run_button, sample_button


@app.cell
def _(n_slider):
    n_slider
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
def _(mo):
    mo.md(r"""# Changing samples""")
    return


@app.cell
def _(sample_button):
    sample_button
    return


@app.cell
def _(colors, samples):
    table_rows = [
        "| Sample | Points | Lines |",
        "| :---: | :--: | :--: |"
    ]

    for _color in colors:
        _, _, _, _cb_points, _cb_lines = samples[_color]
        table_rows.append(f'| <span style="color: {_color};">Sample</span> | {_cb_points} | {_cb_lines} |')

    table_str = "\n".join(table_rows)
    return table_rows, table_str


@app.cell
def _(mo, table_str):
    sample_table = mo.md(table_str)
    return (sample_table,)


@app.cell
def _(alt, mo, np, pl, sample_button):
    sample_button
    _n = 3000
    _x = np.random.normal(0, 5, _n)
    _noise = np.random.normal(0, 200, _n)
    _y = 10 * _x + _noise
    df = pl.DataFrame({'x': _x, 'y': _y, 'c': 1})

    def ols_regression(df):
        x = df.select('c', 'x').to_numpy()
        y = df['y'].to_numpy()
        return np.linalg.inv(x.T @ x) @ x.T @ y


    def create_line_df(df, intercept, slope):
        x_min = df['x'].min()
        x_max = df['x'].max()

        x_line = np.array([x_min*np.abs(np.sign(x_min)-0.1), x_max*np.abs(np.sign(x_max)+0.1)])
        y_line = intercept + slope * x_line
        return pl.DataFrame({'x': x_line, 'y': y_line})


    def subset_regression(df, n, color):
        df_subset = df.sample(n)

        intercept, slope = ols_regression(df_subset)

        line_df = create_line_df(df_subset, intercept, slope)

        points = alt.Chart(df_subset).mark_point(size=20, filled=True).encode(
            x=alt.X('x'),
            y=alt.Y('y'),
            color=alt.value(color),
            stroke=alt.value("black"),
            strokeWidth=alt.value(1),
        )

        line = alt.Chart(line_df).mark_line(size=2).encode(
            x='x',
            y='y',
            color=alt.value(color),
        )
        
        eq = mo.md(f"\\( \\widehat{{\\text{{y}}}} = {intercept:.2f}{slope:+.2f} \\text{{x}} \\)")

        return points, line, eq
    return create_line_df, df, ols_regression, subset_regression


@app.cell
def _(df, mo, n_slider, subset_regression):
    final_points = []
    final_lines = []
    final_eqs = []
    samples = {}
    colors = ("#56B4E9", "#009E73", "#E69F00", "#D55E00", "#F0E442", "#CC79A7")
    for _i, _color in enumerate(colors):
        points, line, eq = subset_regression(df, n_slider.value, _color)
        samples[_color] = (points, line, eq, mo.ui.checkbox(), mo.ui.checkbox())
    return (
        colors,
        eq,
        final_eqs,
        final_lines,
        final_points,
        line,
        points,
        samples,
    )


@app.cell
def _(alt, colors, df, mo, run_button, samples):
    run_button.value
    base = alt.Chart(df)
    layers = []
    for _color in colors:
        if samples[_color][3].value:
            layers.append(samples[_color][0])
        if samples[_color][4].value:
            layers.append(samples[_color][1])

    if layers:
        base = alt.Chart(df).mark_point(size=20, filled=True).encode(
            x='x',
            y='y',
            color=alt.value("grey"),
            opacity=alt.value(0.3)
        )
    else:
        base = alt.Chart(df).mark_point(size=20, filled=True).encode(
            x='x',
            y='y',
            color=alt.value("grey")
        )

    layers.insert(0, base)

    final_chart = mo.ui.altair_chart(
        alt.layer(*layers)
        .configure_axis(titleFontSize=12, labelFontSize=10, grid=False)
        .configure_title(fontSize=16)
        .properties(width=950, height=400),
        chart_selection=False
    )
    return base, final_chart, layers


@app.cell
def _(final_chart):
    final_chart
    return


@app.cell
def _(sample_table):
    sample_table
    return


@app.cell
def _(run_button):
    run_button
    return


@app.cell
def _(colors, mo, run_button, samples):
    run_button.value
    html_str = "<div style='text-align: left;'>\n"
    for _color in colors:
        if samples[_color][4].value:
            html_str += f'<span style="color: {_color};">{samples[_color][2]}</span>\n'
    html_str += "</div>"

    mo.Html(html_str)
    return (html_str,)


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import polars as pl
    import numpy as np
    import altair as alt
    return alt, np, pl


if __name__ == "__main__":
    app.run()
