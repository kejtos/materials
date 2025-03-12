# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///

import marimo

__generated_with = "0.11.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # Residuals sum to zero

        Let's imagine a linear regression model with one regressor:

        \[
        y_i = \beta_0 + \beta_1 x_i + u_i
        \]

        OLS minimizes the sum of squares of residuals

        \[
        RSS = \sum_{i=1}^{n} \bigl(y_i - (\hat{\beta}_0 + \hat{\beta}_1 x_i)\bigr)^2
        \]

        For RSS to be at the \(\displaystyle \min_{\hat{\beta}_0, \hat{\beta}_1}\{\text{RSS}\} \), both derivatives of RSS with respect to \(\hat{\beta}_0\) and \(\hat{\beta}_1\) have to be 0. In the case of \(\hat{\beta}_0\):

        \[
        \begin{align*}
        \frac{\partial RSS}{\partial \hat{\beta}_0} 
        = -2 \sum_{i=1}^{n} \left(y_i - \hat{\beta}_0 - \hat{\beta}_1 x_i\right) &= 0 \\
        \sum_{i=1}^{n} \left(y_i - \hat{\beta}_0 - \hat{\beta}_1 x_i\right) &= 0 \\
        \sum_{i=1}^{n} \left(y_i - \left(\hat{\beta}_0 + \hat{\beta}_1 x_i\right)\right) &= 0 \\
        \sum_{i=1}^{n} \left(y_i - \hat{y}_i\right) &= 0 \\
        \sum_{i=1}^{n} \hat{u}_i &= 0
        \end{align*}
        \]
        ---
        # Mean of y and $\hat{y}$ are the same

        \[
        \begin{align*}
        \sum_{i=1}^{n} \left(y_i - \hat{y}_i\right) &= 0 \\
        \sum_{i=1}^{n} y_i &= \sum_{i=1}^{n} \hat{y_i} \\
        \frac{1}{n} \sum_{i=1}^{n} y_i &= \frac{1}{n}\sum_{i=1}^{n} \hat{y_i} \\
        \overline{y} &= \overline{\hat{y}}
        \end{align*}
        \]
        """
    )
    return


if __name__ == "__main__":
    app.run()
