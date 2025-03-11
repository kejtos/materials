# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "altair==5.5.0",
#     "marimo",
#     "numpy==2.2.3",
#     "pandas==2.2.3",
#     "polars==1.23.0",
#     "scipy==1.15.2",
#     "statsmodels==0.14.4",
# ]
# [tool.marimo.display]
# theme = "dark"
# ///

import marimo

__generated_with = "0.11.5"
app = marimo.App(width="medium")


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
    mo.md(
        r"""
        # OLS estimation

        OLS is an estimation method that tries to find a model that would _best_ fit the data by minimizing the sum of squared erros or the sum of squared residuals. Graphically, it tries to minimize the green area in the following chart:
        """
    )
    return


@app.cell(hide_code=True)
def _(alt, np, pl):
    _x = np.array([[1, 1, 1, 1, 1], [10, 6, -9, -1, -2]]).T
    _y = np.array([10, 0, -1, -3, 3])

    beta = np.linalg.inv(_x.T @ _x) @ _x.T @ _y
    df = pl.DataFrame({"x": _x[:, 1], "yhat": _x @ beta, "y": _y})

    df = df.with_columns(
        error=pl.col("y") - pl.col("yhat"),
        x_right=pl.col("x") - pl.col("y") + pl.col("yhat"),
    )

    points_actual = (
        alt.Chart(df)
        .mark_circle(size=80)
        .encode(
            x=alt.X(
                "x:Q", scale=alt.Scale(domain=[-11, 12]), axis=alt.Axis(title="X")
            ),
            y=alt.Y(
                "y:Q", scale=alt.Scale(domain=[-4, 12]), axis=alt.Axis(title="Y")
            ),
            color=alt.value("#56B4E9"),
            stroke=alt.value("black"),
            strokeWidth=alt.value(1),
            tooltip=["x", "y", "yhat"],
        )
    )

    point_pred = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X("x:Q"),
            y=alt.Y("yhat:Q"),
            color=alt.value("#D55E00"),
        )
    )

    eq_df = pl.DataFrame({"eq": [f"ŷ = {beta[0]:.2f} + {beta[1]:.2f}x"]})

    eq_text = (
        alt.Chart(eq_df)
        .mark_text(
            align="right",
            baseline="top",
            fontSize=20,
        )
        .encode(
            x=alt.value(620),
            y=alt.value(280),
            text="eq:N",
            color=alt.value("#D55E00"),
            stroke=alt.value("black"),
            strokeWidth=alt.value(.2)
        )
    )

    squares = []
    for xos in df["x"]:
        squares.append(
            alt.Chart(df)
            .mark_rect(opacity=0.3)
            .encode(
                x=alt.X("x:Q"),
                x2="x_right:Q",
                y=alt.Y("yhat:Q"),
                y2="y:Q",
                color=alt.value("#009E73"),
                stroke=alt.value("black"),
                strokeWidth=alt.value(1),
            )
        )

        squares.append(
            alt.Chart(df)
            .transform_calculate(
                mid_x="(datum.x + datum.x_right) / 2",
                mid_y="(datum.yhat + datum.y) / 2",
                area="abs((datum.x_right - datum.x) * (datum.y - datum.yhat))",
            )
            .mark_text(color="black", fontSize=14)
            .encode(
                x="mid_x:Q",
                y="mid_y:Q",
                text=alt.Text("area:Q", format=".2f")
            )
        )

    chart = (
        alt.layer(*squares, points_actual, point_pred, eq_text)
        .properties(
            width=400,
            height=300,
        )
        .configure_axis(titleFontSize=12, labelFontSize=10, grid=False)
        .properties(width=950, height=600)
    )

    chart
    return (
        beta,
        chart,
        df,
        eq_df,
        eq_text,
        point_pred,
        points_actual,
        squares,
        xos,
    )


@app.cell
def _(mo):
    mo.md(r"""In this particular case case, $\hat{\beta_0}=1.44$ and $\hat{\beta_1}=0.45$, which can be estimated in many different ways. Let's look at two simple ways.""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Calculus-based derivation of OLS

        Let's imagine a linear regression model with one regressor:

        \[
        y_i = \beta_0 + \beta_1 x_i + u_i
        \]

        We try to minimize the sum of squares of residuals.

        \[
        RSS = \sum_{i=1}^{n} \bigl(y_i - (\hat{\beta}_0 + \hat{\beta}_1 x_i)\bigr)^2.
        \]

        Taking the derivative with respect to \(\hat{\beta}_0\):

        \[
        \frac{\partial RSS}{\partial \hat{\beta}_0} 
        = -2 \sum_{i=1}^{n} \Bigl(y_i - \hat{\beta}_0 - \hat{\beta}_1 x_i\Bigr) 
        = 0.
        \]

        This simplifies to:

        \[
        \sum_{i=1}^{n} y_i = n\,\hat{\beta}_0 + \hat{\beta}_1 \sum_{i=1}^{n} x_i.
        \]

        Taking the derivative with respect to \(\hat{\beta}_1\):

        \[
        \frac{\partial RSS}{\partial \hat{\beta}_1} 
        = -2 \sum_{i=1}^{n} x_i\Bigl(y_i - \hat{\beta}_0 - \hat{\beta}_1 x_i\Bigr)
        = 0.
        \]

        This gives:

        \[
        \sum_{i=1}^{n} x_i y_i = \hat{\beta}_0 \sum_{i=1}^{n} x_i + \hat{\beta}_1 \sum_{i=1}^{n} x_i^2.
        \]

        Thus, we get the normal equations:

        \[
        \begin{aligned}
        \sum_{i=1}^{n} y_i &= n\,\hat{\beta}_0 + \hat{\beta}_1 \sum_{i=1}^{n} x_i, \\
        \sum_{i=1}^{n} x_i y_i &= \hat{\beta}_0 \sum_{i=1}^{n} x_i + \hat{\beta}_1 \sum_{i=1}^{n} x_i^2.
        \end{aligned}
        \]

        We have 2 equations with 2 unknonws ($\hat{\beta}_0$, $\hat{\beta}_1$), and we could easily solve them if we substituted for each $y_i$ and $x_i$. 

        ## Matrix derivation of OLS

        Let's imagine a linear regression model:

        \[
        Y = X\beta + u
        \]

        The model could also be depicted like this:

        \[
        \left(\begin{array}{c}
        Y_1 \\[4mm]
        Y_2 \\[4mm]
        \vdots \\[4mm]
        Y_n
        \end{array}\right)_{n \times 1}
        =
        \left[\begin{array}{cccc}
        1 & X_{11} & X_{12} & \cdots & X_{1k} \\[4mm]
        1 & X_{21} & X_{22} & \cdots & X_{2k} \\[4mm]
        \vdots & \vdots & \vdots & \ddots & \vdots \\[4mm]
        1 & X_{n1} & X_{n2} & \cdots & X_{nk}
        \end{array}\right]_{n \times k+1}
        \left(\begin{array}{c}
        \beta_0 \\[4mm]
        \beta_1 \\[4mm]
        \vdots \\[4mm]
        \beta_k
        \end{array}\right)_{k+1 \times 1}
        +
        \left(\begin{array}{c}
        u_1 \\[4mm]
        u_2 \\[4mm]
        \vdots \\[4mm]
        u_n
        \end{array}\right)_{n \times k+1}
        \]

        as we have $n$ observations and $k$ parameters + a constant. We try to minimize the sum of squares of residuals:

        $$
        \begin{aligned}
        \sum_{i=1}^{n} e_i^2 &= e^T e \\
                             &= (Y - \hat{Y})^T (Y - \hat{Y}) \\
                             &= (Y - X\hat{\beta})^T (Y - X\hat{\beta}) \\
                             &= Y^T Y - 2\hat{\beta}^T X^T Y + \hat{\beta}^T X^T X \hat{\beta}
        \end{aligned}
        $$

        We minimize with respect to the unknown values $\hat{\beta}$ as follows:

        $$
        \begin{aligned}
        \frac{\partial RS S}{\partial \hat{\beta}^T} = -2X^TY + 2X^TX\hat{\beta} &= 0 \\
        X^TX\hat{\beta} &= X^TY \\
        \hat{\beta}_{\text{OLS}}    &= (X^TX)^{-1}X^TY
        \end{aligned}
        $$
        """
    )
    return


@app.cell
def _(mo):
    mein_menu2 = mo.Html(
        f'<a href="https://kejtos.github.io/marimo_test/" target="_parent" '
        f'style="display: inline-block; border: 1px solid #ccc; border-radius: 8px; padding: 4px 8px; font-size: 11px;">'
        f'{mo.icon("carbon:return")} Back to the menu</a>'
    )
    return (mein_menu2,)


@app.cell
def _(mein_menu2):
    mein_menu2.right()
    return


@app.cell
def _():
    import altair as alt
    import polars as pl
    import numpy as np
    import statsmodels.api as sm
    return alt, np, pl, sm


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(alt):
    _ = alt.theme.enable('dark')
    return


if __name__ == "__main__":
    app.run()
