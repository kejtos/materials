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
app = marimo.App()


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
    import pandas as pd
    from scipy.stats import norm
    from numpy.linalg import inv
    from scipy import stats
    import math
    return inv, math, mo, norm, np, pd, stats


@app.cell
def _():
    GRAPTH_WIDTH = 600
    GRAPTH_HEIGHT = 200
    return GRAPTH_HEIGHT, GRAPTH_WIDTH


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
    mo.md("""# Multicollinearity""")
    return


@app.cell
def _(alt, inv, mo, norm, np, pd):
    np.random.seed(55)

    _N = 100_000
    _IQ = np.random.normal(100, 7, _N)
    _wage = np.random.normal(35, 2, _N)
    _educ = (np.random.uniform(9, 20, _N)/10) + np.sqrt(50.5 * _IQ)
    _u = np.random.normal(0, 16, _N)
    _expert = np.random.uniform(0, 20, _N)
    _wage = 2.5 + 1.5*_educ + 2*_expert + 3.5*_IQ + _u

    _pop = pd.DataFrame({
        'const': 1,
        'wage': _wage,
        'educ': _educ,
        'expert': _expert,
        'IQ': _IQ})

    _x = np.arange(-20, 20, 0.1)
    _norm_dens = norm.pdf(_x)
    _t_ratio = []

    _seq = np.arange(40, 1000, 10)
    _i = 1

    for _i in range(len(_seq)):
        _sample = _pop.sample(_seq[_i])
        _X = _sample[['const', 'educ', 'expert', 'IQ']].to_numpy()
        _y = _sample['wage'].to_numpy()
        _beta = inv(_X.T @ _X) @ _X.T @ _y
        _res = _y - _X @ _beta
        _sigma_sq = _res.T @ _res / (_X.shape[0] - _X.shape[1])
        _var_beta = inv(_X.T @_X) * _sigma_sq
        _std_err = np.sqrt(np.diag(_var_beta))
        _t_values = _beta / _std_err
        _t_ratio.append(_t_values[3])
        _norm_df = pd.DataFrame({'x': _x, 'norm_dens': _norm_dens})
        _t_stat_df = pd.DataFrame({'t_ratio': [_t_ratio[_i]], 'y': [0]})
        _chart1 = alt.Chart(_norm_df).mark_line().encode(x='x', y='norm_dens')
        _chart2 = alt.Chart(_t_stat_df).mark_point().encode(x='t_ratio', y='y')
        _chart = _chart1 + _chart2

    _t_ratio_df = pd.DataFrame({'t_ratio': _t_ratio, 'Number of observations': _seq})

    mo.ui.altair_chart(alt.Chart(_t_ratio_df).mark_line(color='blue').encode(
        x='Number of observations',
        y='t_ratio'
    ).properties(
        title='Evolution of t-statistic depending on the number of observations in multicollinearity'
    ).configure_axis(grid=False)
    )
    return


if __name__ == "__main__":
    app.run()
