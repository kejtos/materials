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
    layout_file="layouts/estimator_distribution.grid.json",
)


@app.cell
def _(alt):
    _ = alt.theme.enable('dark')
    return


@app.cell
def _():
    N = 10000
    return (N,)


@app.cell
def _(N, mo):
    n_samples = mo.ui.slider(50, N, 50, full_width=True, debounce=True, label='Samples')
    run_button = mo.ui.run_button(label='Change sample')
    return n_samples, run_button


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
    mo.md(r"""# Estimator distribution""")
    return


@app.cell
def _(np, pl):
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
    return create_line_df, df, ols_regression


@app.cell
def _(alt, create_line_df, df, mo, ols_regression, run_button):
    run_button.value
    _df_subset = df.sample(50)

    _intercept, _slope = ols_regression(_df_subset)

    _line_df = create_line_df(_df_subset, _intercept, _slope)

    points = alt.Chart(_df_subset).mark_point(size=20, filled=True).encode(
        x=alt.X('x'),
        y=alt.Y('y'),
        color=alt.value('#56B4E9'),
        stroke=alt.value("black"),
        strokeWidth=alt.value(1),
    )

    line = alt.Chart(_line_df).mark_line(size=3).encode(
        x='x',
        y='y',
        color=alt.value('#56B4E9'),
    )

    eq_one = mo.md(f"\\( \\widehat{{\\text{{y}}}} = {_intercept:.2f}{_slope:+.2f} \\text{{x}} \\)")
    return eq_one, line, points


@app.cell
def _(N, df, np, ols_regression, pl):
    _intercepts = np.zeros(N)
    _slopes = np.zeros(N)
    for _i in range(N):
        _df_subset = df.sample(50)
        _intercepts[_i], _slopes[_i] = ols_regression(_df_subset)

    df_to_plot = pl.from_numpy(np.column_stack([_intercepts, _slopes]), ['intercept', 'slope'])
    return (df_to_plot,)


@app.cell
def _(alt, df_to_plot, mo, n_samples):
    hist_intercepts = mo.ui.altair_chart(
        alt.Chart(df_to_plot[:n_samples.value]).mark_bar().encode(
            alt.X('intercept:Q', bin=alt.Bin(maxbins=50), title='Intercepts'),
            y=alt.Y('count()', title='Frequency')
        )
        .properties(
            title='Histogram of Intercepts'
        )
        .configure_axis(titleFontSize=12, labelFontSize=10, grid=False)
        .configure_title(fontSize=16)
        .properties(width=500, height=300),
        chart_selection=False
    )
    return (hist_intercepts,)


@app.cell
def _(alt, df_to_plot, mo, n_samples):
    hist_slopes = mo.ui.altair_chart(
        alt.Chart(df_to_plot[:n_samples.value]).mark_bar().encode(
            alt.X('slope:Q', bin=alt.Bin(maxbins=50), title='Slopes'),
            y=alt.Y('count()', title='Frequency')
        )
        .properties(
            title='Histogram of Slopes'
        )
        .configure_axis(titleFontSize=12, labelFontSize=10, grid=False)
        .configure_title(fontSize=16)
        .properties(width=500, height=300),
        chart_selection=False
    )
    return (hist_slopes,)


@app.cell
def _(n_samples):
    n_samples
    return


@app.cell
def _(hist_intercepts):
    hist_intercepts
    return


@app.cell
def _(hist_slopes):
    hist_slopes
    return


@app.cell
def _(alt, df, line, mo, points):
    base = alt.Chart(df)
    layers = []
    layers.append(points)
    layers.append(line)

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
def _(eq_one):
    eq_one
    return


@app.cell
def _(final_chart):
    final_chart
    return


@app.cell
def _(run_button):
    run_button
    return


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
