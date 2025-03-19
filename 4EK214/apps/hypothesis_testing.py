# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "altair==5.5.0",
#     "marimo",
#     "numpy==2.2.3",
#     "pandas==2.2.3",
#     "scipy==1.15.2",
# ]
# [tool.marimo.display]
# theme = "dark"
# ///

import marimo

__generated_with = "0.11.5"
app = marimo.App(
    width="medium",
    layout_file="layouts/hypothesis_testing.grid.json",
)


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import altair as alt
    from scipy.stats import norm, t, f
    from numpy.linalg import inv
    from scipy import stats
    return alt, f, inv, mo, norm, np, pd, stats, t


@app.cell
def _(alt):
    _ = alt.theme.enable('dark')
    return


@app.cell
def _():
    str_2s_t = "Two-sided t-test"
    str_1s_t = "One-sided t-test"
    str_2s_f = "F-test"
    str_bp = "Breusch-Pagan test"
    return str_1s_t, str_2s_f, str_2s_t, str_bp


@app.cell(hide_code=True)
def _(mo, str_1s_t, str_2s_t):
    distribution = mo.ui.dropdown(
        options=[
            str_2s_t,
            str_1s_t,
            # str_2s_f,
            # str_bp,
        ],
        value=str_2s_t,
        label="Test",
        # full_width=True
    )
    return (distribution,)


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
def _(distribution):
    distribution
    return


@app.cell
def _(mo):
    two_sided_t = mo.md(
        """
        \\begin{align*}
        H_0&: \\beta = 0 \\\\
        H_a&: \\beta \\neq 0
        \\end{align*}
        """
    )

    one_sided_t = mo.md(
        """
        \\begin{align*}
        H_0&: \\beta = 0 \\\\
        H_a&: \\beta > 0
        \\end{align*}
        """
    )
    return one_sided_t, two_sided_t


@app.cell(hide_code=True)
def _(header):
    header
    return


@app.cell(hide_code=True)
def _(hypotheses):
    hypotheses
    return


@app.cell(hide_code=True)
def _(md_p_val):
    md_p_val
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Slidery""")
    return


@app.cell
def _(mo):
    slider_width = mo.ui.slider(
        start=100,
        stop=2560,
        step=10,
        value=900,
        label="Width",
        debounce=True,
        show_value=True,
        full_width=True,
    )

    slider_height = mo.ui.slider(
        start=50,
        stop=1440,
        step=10,
        value=360,
        label="Height",
        debounce=True,
        show_value=True,
        full_width=True,
    )
    return slider_height, slider_width


@app.cell
def _(np):
    se_steps = np.linspace(0.1, 10, 100).tolist()
    alpha_steps = [0.9, 0.5, 0.1, 0.05, 0.01]
    n_obs_steps = (
        np.linspace(20, 40, 21).tolist()
        + np.linspace(45, 100, 12).tolist()
        + np.linspace(150, 1000, 18).tolist()
    )
    return alpha_steps, n_obs_steps, se_steps


@app.cell
def _(alpha_steps, mo, n_obs_steps, se_steps):
    beta_slider = mo.ui.slider(
        start=-5,
        stop=5,
        step=0.1,
        debounce=False,
        value=0.3,
        label="Coefficient",
        show_value=True,
        full_width=True,
    )

    se_slider = mo.ui.slider(
        steps=se_steps,
        debounce=False,
        value=0.5,
        label="Standard error",
        show_value=True,
        full_width=True,
    )

    alpha_slider = mo.ui.slider(
        steps=alpha_steps,
        debounce=False,
        value=0.05,
        label="Level of significance",
        show_value=True,
        full_width=True,
    )

    n_obs_slider = mo.ui.slider(
        steps=n_obs_steps,
        debounce=False,
        value=20,
        label="Number of observations",
        show_value=True,
        full_width=True,
    )

    df_slider = mo.ui.slider(
        start=1,
        stop=100,
        step=1,
        debounce=False,
        value=1,
        label="Degrees of freedom",
        full_width=True,
    )
    return alpha_slider, beta_slider, df_slider, n_obs_slider, se_slider


@app.cell
def _(alpha_slider):
    N = 1_000
    alpha = alpha_slider.value
    return N, alpha


@app.cell
def _(mo):
    n_vars_slider = mo.ui.slider(
        start=1,
        stop=15,
        step=1,
        debounce=False,
        value=1,
        label="Number of variables",
        show_value=True,
        full_width=True,
    )
    return (n_vars_slider,)


@app.cell
def _(distribution, n_vars_slider, str_1s_t, str_2s_f, str_2s_t):
    if distribution.value == str_2s_f:
        _ = n_vars_slider.value
    elif distribution.value in (str_2s_t, str_1s_t):
        max_for_ftest = n_vars_slider.value
    return (max_for_ftest,)


@app.cell
def _(max_for_ftest):
    max_for_ftest
    return


@app.cell
def _(distribution, mo, n_vars_slider, str_2s_f):
    if distribution.value == str_2s_f:
        f_coefs_slider = mo.ui.slider(
            start=1,
            stop=n_vars_slider.value,
            step=0.1,
            debounce=False,
            value=0.3,
            label="Coefficient",
            show_value=True,
            full_width=True,
        )
    return (f_coefs_slider,)


@app.cell
def _(slider_height):
    slider_height
    return


@app.cell
def _(slider_width):
    slider_width
    return


@app.cell
def _(beta_slider):
    beta_slider
    return


@app.cell
def _(se_slider):
    se_slider
    return


@app.cell
def _(n_vars_slider):
    n_vars_slider
    return


@app.cell
def _(n_obs_slider):
    n_obs_slider
    return


@app.cell
def _(alpha_slider):
    alpha_slider
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""# Markdowny""")
    return


@app.cell
def _(mo, test_stat):
    md_stat_t = mo.md(
        f"""
    \\[
    \\text{{t-stat}} = \\frac{{ \\hat{{ \\beta }} }}{{ SE( \\hat{{ \\beta }} ) }} = {test_stat:.2f}
    \\]
    """
    )
    return (md_stat_t,)


@app.cell
def _(md_stat_t):
    md_stat_t
    return


@app.cell
def _(dof, mo):
    md_dof_t = mo.md(
        f"""
    \\[
    \\text{{Degrees of freedom}} = N - k - 1 = {dof:.0f}
    \\]
    """
    )
    return (md_dof_t,)


@app.cell
def _(md_dof):
    md_dof
    return


@app.cell
def _(alpha, mo):
    md_alpha = mo.md(f"""\\[ \\alpha = {alpha:.2f} \\]""")
    return (md_alpha,)


@app.cell(hide_code=True)
def _(model_eq):
    model_eq
    return


@app.cell
def _(md_alpha, md_stat, mo):
    mo.hstack(
        [md_stat, md_alpha],
        align="center",
        justify="space-around",
    )
    return


@app.cell
def _(mo, p_val):
    p_val_2s_t_eq = mo.md(
        f"""
    \\[
    \\text{{p-value}} = 2(1 - \\text{{CDF}}(\\text{{t-stat}}_{{\\text{{df}}}})) = {p_val:.4f} 
    \\]
    """
    )

    p_val_1s_t_eq = mo.md(
        f"""
    \\[
    \\text{{p-value}} = 1 - \\text{{CDF}}(\\text{{t-stat}}_{{\\text{{df}}}}) = {p_val:.4f} 
    \\]
    """
    )
    return p_val_1s_t_eq, p_val_2s_t_eq


@app.cell
def _(mo):
    md_regression = mo.md(
        """\\[y = \\beta_0 + \\beta_1 x_1 + \\dots + \\beta_n x_n + u\\]"""
    )
    return (md_regression,)


@app.cell
def _(
    alt,
    crit_value,
    df_test_stat,
    dof,
    mo,
    slider_height,
    slider_width,
    test_stat,
):
    _base = alt.Chart(df_test_stat).encode(
        x=alt.X(
            "x",
            axis=alt.Axis(title="t-value"),
            scale=alt.Scale(
                domain=(min(-5, test_stat), max(5, test_stat)),
                padding=0,
                nice=False,
            ),
        ),
        y=alt.Y(
            "y",
            axis=alt.Axis(title="Probability Density"),
            scale=alt.Scale(domain=(0, 0.4)),
        ),
    )

    _distribution = (
        _base.mark_line(color="blue")
        .encode(strokeWidth=alt.value(3))
        .transform_calculate(Interval=f"'pdf_x of t with {dof:.0f} df'")
    )

    _critical_interval1 = mo.ui.altair_chart(
        _base.mark_area()
        .encode(color=alt.value("#009E73"))
        .transform_filter(f"datum.x < -{crit_value}")
    )

    _critical_interval2 = (
        _base.mark_area()
        .encode(color=alt.value("#009E73"))
        .transform_filter(f"datum.x > {crit_value}")
    )

    _non_critical_interval = (
        _base.mark_area()
        .encode(color=alt.value("#56B4E9"))
        .transform_filter(
            f"(datum.x >= -{crit_value}) & (datum.x <= {crit_value})"
        )
    )

    _test_statistic_line = _base.mark_rule().encode(
        color=alt.value("#D55E00"),
        strokeWidth=alt.value(3),
        x=alt.datum(test_stat),
    )

    chart_2s_t = (
        (
            _critical_interval1
            + _critical_interval2
            + _non_critical_interval
            + _distribution
            + _test_statistic_line
        )
        .encode(
            color=alt.Color(
                "Interval:N",
                scale=alt.Scale(
                    domain=[
                        "Critical interval",
                        "Non-critical interval",
                        "t-statistic",
                        f"PDF of t with {dof:.0f} df",
                    ],
                    range=["#009E73", "#56B4E9", "#D55E00", "blue"],
                ),
                legend=alt.Legend(title="", orient="top-left"),
            )
        )
        .configure_axis(titleFontSize=12, labelFontSize=10, grid=False)
        .properties(
            width=slider_width.value,
            height=slider_height.value,
            title="Student's t-distribution",
        )
    )
    return (chart_2s_t,)


@app.cell
def _(
    N,
    alt,
    crit_value,
    distribution,
    dof,
    np,
    pd,
    slider_height,
    slider_width,
    str_2s_t,
    t,
    test_stat,
    title,
):
    if distribution.value == str_2s_t:
        if test_stat > 0:
            _x = np.linspace(crit_value - 0.2, max(test_stat, crit_value + 3.2), N)
            _y = t.pdf(_x, dof)
            _df = pd.DataFrame({"x": _x, "y": _y})
            _t_dist = t.pdf(_x, df=dof)

            _base = alt.Chart(_df).encode(
                x=alt.X(
                    "x",
                    axis=alt.Axis(title="t-value"),
                    scale=alt.Scale(
                        domain=(
                            crit_value - 0.2,
                            max(test_stat, crit_value + 3.2),
                        ),
                        padding=0,
                        nice=False,
                    ),
                ),
                y=alt.Y(
                    "y",
                    axis=alt.Axis(title="Probability Density", format=".2f"),
                    scale=alt.Scale(domain=(0, _y.max())),
                ),
            )

            _critical_interval = (
                _base.mark_area()
                .encode(color=alt.value("#009E73"))
                .transform_filter(f"datum.x > {crit_value}")
            )

            _non_critical_interval = (
                _base.mark_area()
                .encode(color=alt.value("#56B4E9"))
                .transform_filter(
                    f"(datum.x >= {crit_value} - 0.2) & (datum.x <= {crit_value})"
                )
            )

            _test_statistic_line = _base.mark_rule().encode(
                color=alt.value("#D55E00"),
                strokeWidth=alt.value(3),
                x=alt.datum(max(test_stat, crit_value - 0.2)),
            )

            _distribution = (
                _base.mark_line(color="blue")
                .encode(strokeWidth=alt.value(3))
                .transform_calculate(Interval=f"'pdf_x of t with {dof:.0f} df'")
            )

            chart_2s_t_zoom = (
                (
                    _critical_interval
                    + _non_critical_interval
                    + _distribution
                    + _test_statistic_line
                )
                .configure_axis(titleFontSize=12, labelFontSize=10, grid=False)
                .properties(
                    width=slider_width.value,
                    height=slider_height.value,
                    title=f"{title} (zoomed-in)",
                )
            ).encode(
                color=alt.Color(
                    "Interval:N",
                    scale=alt.Scale(
                        domain=[
                            "Critical interval",
                            "Non-critical interval",
                            "t-statistic",
                            f"PDF of t with {dof:.0f} df",
                        ],
                        range=["#009E73", "#56B4E9", "#D55E00", "blue"],
                    ),
                    legend=alt.Legend(title="", orient="top-right"),
                )
            )
        else:
            _x = np.linspace(
                min(test_stat, -crit_value - 3.2), -crit_value + 0.2, N
            )
            _y = t.pdf(_x, dof)
            _df = pd.DataFrame({"x": _x, "y": _y})
            _t_dist = t.pdf(_x, df=dof)

            _base = alt.Chart(_df).encode(
                x=alt.X(
                    "x",
                    axis=alt.Axis(title="t-value"),
                    scale=alt.Scale(
                        domain=(
                            min(test_stat, -crit_value - 3.2),
                            -crit_value + 0.2,
                        ),
                        padding=0,
                        nice=False,
                    ),
                ),
                y=alt.Y(
                    "y",
                    axis=alt.Axis(title="Probability Density", format=".2f"),
                    scale=alt.Scale(domain=(0, _y.max())),
                ),
            )

            _critical_interval = (
                _base.mark_area()
                .encode(color=alt.value("#009E73"))
                .transform_filter(f"datum.x < -{crit_value}")
            )

            _non_critical_interval = (
                _base.mark_area()
                .encode(color=alt.value("#56B4E9"))
                .transform_filter(
                    f"(datum.x >= -{crit_value}) & (datum.x <= -{crit_value} + 0.2)"
                )
            )

            _test_statistic_line = _base.mark_rule().encode(
                color=alt.value("#D55E00"),
                strokeWidth=alt.value(3),
                x=alt.datum(min(test_stat, -crit_value + 0.2)),
            )

            _distribution = (
                _base.mark_line(color="blue")
                .encode(strokeWidth=alt.value(3))
                .transform_calculate(Interval=f"'pdf_x of t with {dof:.0f} df'")
            )

            chart_2s_t_zoom = (
                (
                    _critical_interval
                    + _non_critical_interval
                    + _distribution
                    + _test_statistic_line
                )
                .configure_axis(titleFontSize=12, labelFontSize=10, grid=False)
                .properties(
                    width=slider_width.value,
                    height=slider_height.value,
                    title=f"{title} (zoomed-in)",
                )
            ).encode(
                color=alt.Color(
                    "Interval:N",
                    scale=alt.Scale(
                        domain=[
                            "Critical interval",
                            "Non-critical interval",
                            "t-statistic",
                            f"PDF of t with {dof:.0f} df",
                        ],
                        range=["#009E73", "#56B4E9", "#D55E00", "blue"],
                    ),
                    legend=alt.Legend(title="", orient="top-left"),
                )
            )
    return (chart_2s_t_zoom,)


@app.cell
def _(
    N,
    alt,
    crit_value,
    distribution,
    dof,
    np,
    pd,
    pdf_x,
    pdf_y,
    slider_height,
    slider_width,
    str_1s_t,
    t,
    test_stat,
    title,
):
    if distribution.value == str_1s_t:
        _df = pd.DataFrame({"x": pdf_x, "y": pdf_y})

        _base = alt.Chart(_df).encode(
            x=alt.X(
                "x",
                axis=alt.Axis(title="t-value"),
                scale=alt.Scale(
                    domain=(min(-5, test_stat), max(5, test_stat)),
                    padding=0,
                    nice=False,
                ),
            ),
            y=alt.Y(
                "y",
                axis=alt.Axis(title="Probability Density"),
                scale=alt.Scale(domain=(0, 0.4)),
            ),
        )

        _distribution = (
            _base.mark_line(color="blue")
            .encode(strokeWidth=alt.value(3))
            .transform_calculate(Interval=f"'pdf_x of t with {dof:.0f} df'")
        )

        _critical_interval = (
            _base.mark_area()
            .encode(color=alt.value("#009E73"))
            .transform_filter(f'datum.x > {crit_value}')
        )

        _non_critical_interval = (
            _base.mark_area()
            .encode(color=alt.value("#56B4E9"))
            .transform_filter(f'datum.x <= {crit_value}')
        )

        _test_statistic_line = _base.mark_rule().encode(
            color=alt.value("#D55E00"),
            strokeWidth=alt.value(3),
            x=alt.datum(test_stat),
        )

        chart_1s_t = (
            (
                _critical_interval
                + _non_critical_interval
                + _distribution
                + _test_statistic_line
            )
            .encode(
                color=alt.Color(
                    "Interval:N",
                    scale=alt.Scale(
                        domain=[
                            "Critical interval",
                            "Non-critical interval",
                            "t-statistic",
                            f"PDF of t with {dof:.0f} df",
                        ],
                        range=["#009E73", "#56B4E9", "#D55E00", "blue"],
                    ),
                    legend=alt.Legend(title="", orient="top-left"),
                )
            )
            .configure_axis(titleFontSize=12, labelFontSize=10, grid=False)
            .properties(
                width=slider_width.value,
                height=slider_height.value,
                title=title,
            )
        )

        _x = np.linspace(crit_value - 0.2, max(test_stat, crit_value + 3.2), N)
        _y = t.pdf(_x, dof)
        _df = pd.DataFrame({"x": _x, "y": _y})
        _t_dist = t.pdf(_x, df=dof)

        _base = alt.Chart(_df).encode(
            x=alt.X(
                "x",
                axis=alt.Axis(title="t-value"),
                scale=alt.Scale(
                    domain=(crit_value - 0.2, max(test_stat, crit_value + 3.2)),
                    padding=0,
                    nice=False,
                ),
            ),
            y=alt.Y(
                "y",
                axis=alt.Axis(title="Probability Density", format=".2f"),
                scale=alt.Scale(domain=(0, _y.max())),
            ),
        )

        _critical_interval = (
            _base.mark_area()
            .encode(color=alt.value("#009E73"))
            .transform_filter(f'datum.x > {crit_value}')
        )

        _non_critical_interval = (
            _base.mark_area()
            .encode(color=alt.value("#56B4E9"))
            .transform_filter(
                f'(datum.x >= {crit_value} - 0.2) & (datum.x <= {crit_value})'
            )
        )

        _test_statistic_line = _base.mark_rule().encode(
            color=alt.value("#D55E00"),
            strokeWidth=alt.value(3),
            x=alt.datum(max(test_stat, crit_value - 0.2)),
        )

        _distribution = (
            _base.mark_line(color="blue")
            .encode(strokeWidth=alt.value(3))
            .transform_calculate(Interval=f"'pdf_x of t with {dof:.0f} df'")
        )

        chart_1s_t_zoom = (
            (
                _critical_interval
                + _non_critical_interval
                + _distribution
                + _test_statistic_line
            )
            .configure_axis(titleFontSize=12, labelFontSize=10, grid=False)
            .properties(
                width=slider_width.value,
                height=slider_height.value,
                title=f"{title} (zoomed-in)",
            )
        ).encode(
            color=alt.Color(
                "Interval:N",
                scale=alt.Scale(
                    domain=[
                        "Critical interval",
                        "Non-critical interval",
                        "t-statistic",
                        f"PDF of t with {dof:.0f} df",
                    ],
                    range=["#009E73", "#56B4E9", "#D55E00", "blue"],
                ),
                legend=alt.Legend(title="", orient="top-right"),
            )
        )
    return chart_1s_t, chart_1s_t_zoom


@app.cell
def _():
    # f_crit = f.ppf(1 - alpha, df1, df2)

    # # Prepare data for the distribution
    # x_vals = np.linspace(0, max(5, test_stat, f_crit), 500)
    # pdf_vals = f.pdf(x_vals, df1, df2)
    # df_f_stat = pd.DataFrame({"x": x_vals, "y": pdf_vals})

    # # Define base chart for F-distribution
    # _base = alt.Chart(df_f_stat).encode(
    #     x=alt.X(
    #         "x",
    #         axis=alt.Axis(title="F-value"),
    #         scale=alt.Scale(
    #             domain=(0, max(5, test_stat, f_crit)),
    #             padding=0,
    #             nice=False,
    #         ),
    #     ),
    #     y=alt.Y(
    #         "y",
    #         axis=alt.Axis(title="Probability Density"),
    #         scale=alt.Scale(domain=(0, 0.5)),
    #     ),
    # )

    # # Define distribution line for the F-distribution
    # _distribution = (
    #     _base.mark_line(color="blue")
    #     .encode(strokeWidth=alt.value(3))
    #     .transform_calculate(Interval=f"'pdf_x of F with {df1:.0f} and {df2:.0f} df'")
    # )

    # # Define critical interval for the upper tail only
    # _critical_interval = (
    #     _base.mark_area()
    #     .encode(color=alt.value("#009E73"))
    #     .transform_filter(alt.datum.x > f_crit)
    # )

    # # Define non-critical interval for the lower range up to the critical value
    # _non_critical_interval = (
    #     _base.mark_area()
    #     .encode(color=alt.value("#56B4E9"))
    #     .transform_filter(alt.datum.x <= f_crit)
    # )

    # # Add observed test statistic line
    # _test_statistic_line = _base.mark_rule().encode(
    #     color=alt.value("#D55E00"),
    #     strokeWidth=alt.value(3),
    #     x=alt.datum(test_stat),
    # )

    # # Combine all elements
    # chart_f_test = (
    #     (
    #         _critical_interval
    #         + _non_critical_interval
    #         + _distribution
    #         + _test_statistic_line
    #     )
    #     .encode(
    #         color=alt.Color(
    #             "Interval:N",
    #             scale=alt.Scale(
    #                 domain=[
    #                     "Critical interval",
    #                     "Non-critical interval",
    #                     "F-statistic",
    #                     f"PDF of F with {df1:.0f} and {df2:.0f} df",
    #                 ],
    #                 range=["#009E73", "#56B4E9", "#D55E00", "blue"],
    #             ),
    #             legend=alt.Legend(title="", orient="top-left"),
    #         )
    #     )
    #     .configure_axis(titleFontSize=12, labelFontSize=10, grid=False)
    #     .properties(
    #         width=slider_width.value,
    #         height=slider_height.value,
    #         title="F-distribution for Regression F-test",
    #     )
    # )
    return


@app.cell
def _(main_chart, mo):
    mo.ui.altair_chart(main_chart)
    return


@app.cell
def _(zoomed_chart):
    zoomed_chart
    return


@app.cell
def _():
    # chart_f_test
    return


@app.cell
def _(
    N,
    alpha,
    beta_slider,
    distribution,
    f,
    md_regression,
    mo,
    n_obs_slider,
    n_vars_slider,
    np,
    one_sided_t,
    pd,
    se_slider,
    str_1s_t,
    str_2s_f,
    str_2s_t,
    t,
    two_sided_t,
):
    if distribution.value == str_2s_t:
        hypotheses = two_sided_t
        header = mo.md(f"""# {distribution.value} for a regression coefficient""")
        dof = n_obs_slider.value - n_vars_slider.value - 1
        test_stat = beta_slider.value / se_slider.value
        pdf_x = np.linspace(min(-5, test_stat), max(5, test_stat), N)
        pdf_y = t.pdf(pdf_x, dof)
        crit_value = t.ppf(1 - alpha / 2, df=dof)
        p_val = 2 * (1 - t.cdf(test_stat, df=dof))
        df_test_stat = pd.DataFrame({"x": pdf_x, "y": pdf_y})
        title = "Student's t-distribution"
        model_eq = md_regression
    elif distribution.value == str_1s_t:
        hypotheses = one_sided_t
        header = mo.md(f"""# {distribution.value} for a regression coefficient""")
        dof = n_obs_slider.value - n_vars_slider.value - 1
        test_stat = beta_slider.value / se_slider.value
        crit_value = t.ppf(1 - alpha, df=dof)
        p_val = (1 - t.cdf(test_stat, df=dof)) if test_stat > 0 else 0
        pdf_x = np.linspace(min(-5, test_stat), max(5, test_stat), N)
        pdf_y = t.pdf(pdf_x, dof)
        df_test_stat = pd.DataFrame({"x": pdf_x, "y": pdf_y})
        title = "Student's t-distribution"
        model_eq = md_regression
    elif distribution.value == str_2s_f:
        df1 = n_obs_slider.value - n_vars_slider.value - 1
        df2 = n_vars_slider.value - 1
        crit_value = f.ppf(1 - alpha, df1, df2)
    return (
        crit_value,
        df1,
        df2,
        df_test_stat,
        dof,
        header,
        hypotheses,
        model_eq,
        p_val,
        pdf_x,
        pdf_y,
        test_stat,
        title,
    )


@app.cell
def _(
    chart_1s_t,
    chart_1s_t_zoom,
    chart_2s_t,
    chart_2s_t_zoom,
    distribution,
    md_dof_t,
    md_stat_t,
    p_val_1s_t_eq,
    p_val_2s_t_eq,
    str_1s_t,
    str_2s_f,
    str_2s_t,
):
    if distribution.value == str_2s_t:
        main_chart = chart_2s_t
        zoomed_chart = chart_2s_t_zoom
        md_stat = md_stat_t
        md_p_val = p_val_2s_t_eq
        md_dof = md_dof_t
    elif distribution.value == str_1s_t:
        main_chart = chart_1s_t
        zoomed_chart = chart_1s_t_zoom
        md_stat = md_stat_t
        md_p_val = p_val_1s_t_eq
        md_dof = md_dof_t
    elif distribution.value == str_2s_f:
        s = "ads"
    return main_chart, md_dof, md_p_val, md_stat, s, zoomed_chart


if __name__ == "__main__":
    app.run()
