# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "altair==5.5.0",
#     "marimo",
#     "matplotlib==3.10.1",
#     "numpy==2.2.4",
#     "polars==1.26.0",
#     "scipy==1.15.2",
#     "statsmodels==0.14.4",
# ]
# ///

import marimo

__generated_with = "0.11.5"
app = marimo.App(
    width="medium",
    layout_file="layouts/multiple_testing.grid.json",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Multiple tests""")
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import numpy as np
    from numpy.linalg import inv
    import polars as pl
    import altair as alt
    from scipy.stats import t
    return alt, inv, np, pl, t


@app.cell
def _(alt):
    _ = alt.theme.enable('dark')
    return


@app.cell
def _():
    reps = 10_000
    return (reps,)


@app.cell
def _(mo, np):
    slider_steps = np.concatenate([np.array([2, 3, 4, 5]), np.logspace(1, 4, 4)]).astype(int)
    curr_reps = mo.ui.slider(steps=slider_steps, label='Number of tests', full_width=True)
    return curr_reps, slider_steps


@app.cell
def _(mo):
    alpha = mo.ui.number(start=0, stop=1, step=0.001, value=0.1, label='Alpha', full_width=True)
    return (alpha,)


@app.cell
def _(alpha):
    alpha
    return


@app.cell
def _(curr_reps):
    curr_reps
    return


@app.cell
def _(alpha, curr_reps, inv, np, pl, reps, t):
    betas = []
    std_errors = []
    t_ratios = []
    p_vals = []
    for i in range(reps):
        N = int(100)
        c = np.ones(N)
        x = np.random.normal(0, 10, N)
        x = np.column_stack([c, x])
        y = np.random.normal(0, 10, N)
        k = x.shape[1]
        dof = N - k

        beta = inv(x.T @ x) @ x.T @ y
        residuals = y - x @ beta
        sigma_squared = np.sum(residuals ** 2) / (N - k)
        var_beta = sigma_squared * inv(x.T @ x)
        std_error = np.sqrt(np.diag(var_beta))
        t_ratio = beta / std_error
        p_val = 1 - t.cdf(t_ratio[1], df=dof)

        betas.append(beta[1])
        std_errors.append(std_error[1])
        t_ratios.append(t_ratio[1])
        p_vals.append(p_val)

    df = (
        pl.DataFrame({
            'iteration': range(1, curr_reps.value+1),
            'beta': betas[:curr_reps.value],
            'std_error': std_errors[:curr_reps.value],
            't_ratio': t_ratios[:curr_reps.value],
            'p_val': p_vals[:curr_reps.value],
        })
        .with_columns(
            color=(
                pl.when(pl.col('p_val') >= alpha.value)
                .then(pl.lit('#F0E442'))
                .otherwise(pl.lit('#56B4E9'))
            )
        )
    )
    return (
        N,
        beta,
        betas,
        c,
        df,
        dof,
        i,
        k,
        p_val,
        p_vals,
        residuals,
        sigma_squared,
        std_error,
        std_errors,
        t_ratio,
        t_ratios,
        var_beta,
        x,
        y,
    )


@app.cell
def _(alpha, df, mo, pl):
    rejected = df.filter(pl.col('p_val') < alpha.value)['p_val'].len()
    not_rejected = df.shape[0] - rejected
    proportion_rejected = rejected / df.shape[0]

    mo.md(f'Rejected hypotheses: {proportion_rejected:.2%}')
    return not_rejected, proportion_rejected, rejected


@app.cell
def _(alpha, alt, curr_reps, df, mo):
    scatter = alt.Chart(df).mark_point().encode(
        x=alt.X('iteration:Q', axis=alt.Axis(title='Iteration', format='d', tickMinStep=1), scale=alt.Scale(domain=[0, curr_reps.value+1])),
        y=alt.Y('p_val:Q', title='p-value'),
        color=alt.Color('color:N', scale=None)
    )

    rule = (
        alt.Chart(df)
        .mark_rule(strokeDash=[5,5])
        .encode(
            y=alt.datum(alpha.value),
            color=alt.value('#D55E00')
        )
    )

    mo.ui.altair_chart(
        (rule + scatter)
        .configure_axis(titleFontSize=12, labelFontSize=10, grid=False)
        .configure_title(fontSize=16)
        .properties(width=950, height=400),
        chart_selection=False
    )
    return rule, scatter


if __name__ == "__main__":
    app.run()
