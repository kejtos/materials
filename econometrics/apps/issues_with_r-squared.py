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
    layout_file="layouts/issues_with_r-squared.grid.json",
)


@app.cell
def _():
    import altair as alt
    return (alt,)


@app.cell
def _(alt):
    _ = alt.theme.enable('dark')
    return


@app.cell
def _():
    import marimo as mo
    import numpy as np
    from numpy.random import normal, randint, seed
    from numpy import ones, exp, repeat, sum, mean
    from numpy.linalg import inv
    import pandas as pd

    ORANGE = '#E69F00'
    TEAL = '#56B4E9'
    GREEN = '#009E73'
    return (
        GREEN,
        ORANGE,
        TEAL,
        exp,
        inv,
        mean,
        mo,
        normal,
        np,
        ones,
        pd,
        randint,
        repeat,
        seed,
        sum,
    )


@app.cell
def _():
    GRAPH_WIDTH = 1100
    GRAPH_HEIGHT = 500
    space = "&nbsp;"
    return GRAPH_HEIGHT, GRAPH_WIDTH, space


@app.cell
def _(mo):
    main_menu = mo.Html(
        f'<a href="https://kejtos.github.io/materials/" target="_parent" '
        f'style="display: inline-block; border: 1px solid #ccc; border-radius: 8px; padding: 4px 8px; font-size: 11px;">'
        f'{mo.icon("carbon:return")} Back to the menu</a>'
    )
    return (main_menu,)


@app.cell
def _(mo, space):
    headline = mo.md('<font size="7">Issues with R-squared</font>')

    headline_1 = mo.md(
        f'<font size="7">1. {space*4} Non-decreasing in parameters</font>'
    )
    headline_2 = mo.md(
        f"""<font size="7">
    2. {space*4} Using very strong ('too obvious') variables
    </font>"""
    )
    headline_2a = mo.md(f'<font size="7">(a) {space*4} Deterministic trend</font>')
    headline_2b = mo.md(
        f'<font size="7">(b) {space*4} Obvious relationships</font>'
    )
    intuition = mo.md(
        f"""<font size="7">Intuition:{space*3} Each new variable give us at worst no new information.</font>"""
    )
    return (
        headline,
        headline_1,
        headline_2,
        headline_2a,
        headline_2b,
        intuition,
    )


@app.cell
def _(mo):
    n_reg = mo.ui.slider(
        start=1,
        stop=98,
        debounce=False,
        value=1,
        label="Number of regressors",
        show_value=True,
        full_width=True,
    )
    return (n_reg,)


@app.cell
def _(inv, mean, mo, normal, np, ones, seed, sum):
    seed(11)  #  Changing the number generates different pseudorandom numbers
    rs_squared = []
    ars_squared = []
    N = 100
    X = ones(N)  #  Constant
    y = normal(2, 2, N)  #  Randomly generated normal variable!

    for _i in range(100):
        xi = normal(1, 2, N)  #  Randomly generated normal variable!
        X = np.column_stack((X, xi))
        k = X.shape[1] - 1

        beta_hat = inv(X.T @ X) @ X.T @ y  #  Coefficients
        y_hat = X @ beta_hat  #  Fitted_values
        SSR = sum((y_hat - y) ** 2)  #  Unexplained variance
        SST = sum((y - mean(y)) ** 2)  #  Total variance
        SSE = SST - SSR  #  Explained variance
        R_squared = SSE / SST  #  R_squared
        R_adj = 1 - (
            ((1 - R_squared) * (N - 1)) / (N - k - 1)
        )  #  Adjusted R_squared
        rs_squared.append(R_squared)
        ars_squared.append(R_adj)

    o_ = mo.show_code()
    return (
        N,
        R_adj,
        R_squared,
        SSE,
        SSR,
        SST,
        X,
        ars_squared,
        beta_hat,
        k,
        o_,
        rs_squared,
        xi,
        y,
        y_hat,
    )


@app.cell
def _(
    GRAPH_HEIGHT,
    GRAPH_WIDTH,
    GREEN,
    ORANGE,
    alt,
    ars_squared,
    mo,
    n_reg,
    pd,
    rs_squared,
):
    df_rs = pd.DataFrame(
        {"R-Squared": rs_squared, "Adj R-Squared": ars_squared}
    ).reset_index()[: n_reg.value]

    chart1 = (
        alt.Chart(df_rs)
        .mark_line(color=ORANGE)
        .encode(
            x=alt.X(
                "index",
                title="Number of regressors",
                scale=alt.Scale(domain=(0, 100)),
            ),
            y=alt.Y(
                "R-Squared", title="R-Squared", scale=alt.Scale(domain=(-1, 1))
            ),
        )
        .properties(width=GRAPH_WIDTH, height=GRAPH_HEIGHT / 2)
    )

    chart2 = (
        alt.Chart(df_rs)
        .mark_line(color=GREEN)
        .encode(
            x=alt.X(
                "index",
                title="Number of regressors",
                scale=alt.Scale(domain=(0, 100)),
            ),
            y=alt.Y(
                "Adj R-Squared",
                title="Adj R-Squared",
                scale=alt.Scale(domain=(-1, 1)),
            ),
        )
        .properties(width=GRAPH_WIDTH, height=GRAPH_HEIGHT / 2)
    )

    chart_rs = mo.ui.altair_chart(
        alt.vconcat(chart1, chart2)
        .configure_title(fontSize=16, anchor='middle')
        .configure_axis(titleFontSize=12, labelFontSize=10, grid=False)
        .configure_legend(titleFontSize=12, labelFontSize=10),
        chart_selection=False
    )
    return chart1, chart2, chart_rs, df_rs


@app.cell
def _(
    GRAPH_HEIGHT,
    GRAPH_WIDTH,
    GREEN,
    N,
    ORANGE,
    TEAL,
    alt,
    normal,
    np,
    pd,
    seed,
):
    seed(11)
    t = np.linspace(0, 300, num=N)

    b0 = 2.5
    b1 = 5.0

    x1 = b0 + b1 * t + normal(0, 100, N)
    x2 = b0 + normal(0, 100, N)
    y1 = b0 + b1 * t + normal(0, 100, N)

    df = pd.DataFrame(
        {"Time": t, "X1": x1, "X2": x2, "Y": y1, "Trend": b0 + b1 * t}
    ).melt(id_vars="Time", var_name="Variable", value_name="Value")


    custom_colors = {
        "X1": ORANGE,
        "X2": GREEN,
        "Y": TEAL,
    }

    variables = df.loc[df["Variable"] != "Trend", "Variable"].unique().tolist()

    custom_scale = alt.Scale(
        domain=variables, range=[custom_colors[var] for var in variables]
    )

    selection = alt.selection_point(fields=["Variable"], bind="legend")

    trend_vars_scatter = (
        alt.Chart(df[df["Variable"] != "Trend"])
        .mark_circle(size=40)
        .encode(
            x=alt.X(
                "Time:Q",
                axis=alt.Axis(title="Time"),
            ),
            y=alt.Y(
                "Value:Q",
                axis=alt.Axis(title="Value"),
            ),
            color=alt.Color(
                "Variable:N",
                scale=custom_scale,
                legend=alt.Legend(title="Variables", orient="top-left"),
            ),
            opacity=alt.condition(selection, alt.value(1.0), alt.value(0.5)),
            tooltip=["Variable:N", "Time:Q", "Value:Q"],
            stroke=alt.value("black"),
            strokeWidth=alt.value(1),
        )
        .properties(
            title=alt.TitleParams(
                text="Scatter Plot of Variables with Common Linear Trend",
            ),
            width=GRAPH_WIDTH,
            height=GRAPH_HEIGHT,
        )
        .add_params(selection)
        .transform_filter(selection)
        .configure_title(fontSize=16, anchor='middle')
        .configure_axis(titleFontSize=12, labelFontSize=10, grid=False)
        .configure_legend(titleFontSize=12, labelFontSize=10)
    )
    return (
        b0,
        b1,
        custom_colors,
        custom_scale,
        df,
        selection,
        t,
        trend_vars_scatter,
        variables,
        x1,
        x2,
        y1,
    )


@app.cell
def _(N, inv, mean, np, ones, sum, x1, y1):
    _X = ones(N)
    _X = np.column_stack((_X, x1))
    _y = y1
    _beta = inv(_X.T @ _X) @ +_X.T @ _y
    _y_hat = _X @ (_beta)
    _SSR = sum((_y_hat - _y) ** 2)
    _SST = sum((_y - mean(_y)) ** 2)
    _SSE = _SST - _SSR
    R_squared1 = _SSE / _SST
    return (R_squared1,)


@app.cell
def _(N, inv, mean, np, ones, sum, t, x2, y1):
    _X = ones(N)
    _X = np.column_stack((_X, x2, t))
    _y = y1
    _beta = inv(_X.T @ _X) @ +_X.T @ _y
    _y_hat = _X @ (_beta)
    _SSR = sum((_y_hat - _y) ** 2)
    _SST = sum((_y - mean(_y)) ** 2)
    _SSE = _SST - _SSR
    R_squared2 = _SSE / _SST
    return (R_squared2,)


@app.cell
def _(N, R_squared1, R_squared2, inv, mean, mo, np, ones, sum, x2, y1):
    _X = ones(N)
    _X = np.column_stack((_X, x2))
    _y = y1
    _beta = inv(_X.T @ _X) @ _X.T @ _y
    _y_hat = _X @ (_beta)
    _SSR = sum((_y_hat - _y) ** 2)
    _SST = sum((_y - mean(_y)) ** 2)
    _SSE = _SST - _SSR
    R_squared3 = _SSE / _SST

    models = mo.md(
        f"""

    | Model                                                      | R-squared        |
    |------------------------------------------------------------|------------------|
    | \\( Y = \\beta_0 + \\beta_1 X_1 + u \\)                    | {R_squared1:.4f} |
    | \\( Y = \\beta_0 + \\beta_1 X_2 + \\beta_2 t + u \\)       | {R_squared2:.4f} |
    | \\( Y = \\beta_0 + \\beta_1 X_2 + u \\)                    | {R_squared3:.4f} |
    """
    )
    return R_squared3, models


@app.cell
def _(N, inv, mean, mo, np, ones, randint, space, sum):
    np.random.seed(11)
    I = randint(48_000, 50_000, 100)
    C = I - randint(2_000, 4_000, N)
    waste = randint(0, 250, N)
    S = I - C - waste

    _X = np.column_stack((ones(N), C, S))
    _y = I
    _beta = inv(_X.T @ _X) @ +_X.T @ _y
    _y_hat = _X @ (_beta)
    _SSR = sum((_y_hat - _y) ** 2)
    _SST = sum((_y - mean(_y)) ** 2)
    _SSE = _SST - _SSR
    _R_squared = _SSE / _SST

    model_cons_md = mo.md(
        f"""

    {space*3} Economics: {space*10} \\( I = C + S \\)

    Econometrics: {space*9} \\( I_i = \\beta_0 + \\beta_1 C_i + \\beta_2 S_i + u_i \\)

    {space*4} R-squared: {space*10} {_R_squared:.4f}
    """
    )
    return C, I, S, model_cons_md, waste


@app.cell
def _(mo):
    trend_md = mo.md(
    """
    \\( Y \\) is randomly generated trending variable

    \\( X_1 \\) is randomly generated trending variable

    \\( X_2 \\) is randomly generated non-trending variable

    <br>

    This is called **spurious regression**.
    """
    )
    return (trend_md,)


@app.cell
def _(mo, models, trend_md, trend_vars_scatter):
    trend_graph = mo.hstack(
        [trend_vars_scatter, mo.vstack([models, trend_md], gap=5)]
    )
    return (trend_graph,)


@app.cell
def _(mo):
    r_sq_not_useful_md = mo.md(
        "The R-squared of the model is unsurprisingly high -> savings and consumption are able to estimate ones invome very well. This does not make the model really that useful."
    )
    return (r_sq_not_useful_md,)


@app.cell
def _(chart_rs, mo, n_reg, o_):
    r_sq_nondec = mo.hstack([o_, mo.vstack([n_reg, chart_rs])], align="center")
    return (r_sq_nondec,)


@app.cell
def _(
    headline,
    headline_1,
    headline_2,
    headline_2a,
    headline_2b,
    intuition,
    main_menu,
    mo,
    model_cons_md,
    r_sq_nondec,
    r_sq_not_useful_md,
    trend_graph,
):
    mo.vstack([main_menu.right(),
    mo.carousel(
        [
            headline,
            headline_1,
            intuition,
            r_sq_nondec,
            headline_2,
            headline_2a,
            trend_graph,
            headline_2b,
            model_cons_md,
            r_sq_not_useful_md,
        ]
    )
    ])
    return


if __name__ == "__main__":
    app.run()
