# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# [tool.marimo.display]
# theme = "dark"
# ///

import marimo

__generated_with = "0.11.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ---
        # Proof of Gauss-Markov theorem
        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        Given the linear model:

        $$
        y = X\\beta + u
        $$

        where:

        - \\(y\\) is the vector of observed values,
        - \\(X\\) is the matrix of regressors (including a column of ones for the intercept),
        - \\(\\beta\\) is the vector of coefficients,
        - \\(u\\) is the vector of errors

        The OLS estimator for \\(\\beta\\) 

        $$
        \\hat{\\beta} = (X'X)^{-1} X'y
        $$

        is the best (has the lowest variance) among all linear unbiased estimators of \\(\\beta\\), iff

        $$
        E(u | X) = 0 \\quad \\text{(mean independence, MLR.3)}
        $$

        and

        $$
        \\text{Var}(u) = \\sigma^2 I \\quad \\text{(homoscedasticity, MLR.5)}
        $$
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ---

        ## 1. **Possibility to calculate the estimates**

        For \\(\\hat{\\beta}\\) to be computable, \\((X'X)\\) must be **invertible**, which requires that the columns of \\(X\\) are linearly independent, ensuring that \\(X'X\\) has full rank. In other words, variables cannot be perfectly colinear (MLR.4).

        ### **Proof that \\(X'X\\) is invertible if and only if \\(X\\) has full rank**

        Let \\(X\\) be an \\(n \\times k\\) matrix. We will show that \\(X'X\\) is invertible if and only if \\(X\\) has full column rank.

        #### 1. **Sufficiency**: If \\(X\\) has full column rank, then \\(X'X\\) is invertible.

        **Full column rank** means that the columns of \\(X\\) are linearly independent, implying that the rank of \\(X\\) is \\(k\\).
        Consider an arbitrary non-zero vector \\(v \\in \\mathbb{R}^k\\). The quadratic form \\(v'(X'X)v\\) can be written as:

        $$
        v'(X'X)v = (Xv)'(Xv) = \\| Xv \\|^2
        $$

        Since \\(X\\) has full column rank, \\(Xv\\) is non-zero for any non-zero \\(v\\), meaning:

        $$
        \\| Xv \\|^2 > 0 \\quad \\text{for all non-zero } v
        $$

        Thus, \\(v'(X'X)v > 0\\), which means that \\(X'X\\) is **positive definite**. A positive definite matrix is always invertible.

        #### 2. **Necessity**: If \\(X'X\\) is invertible, then \\(X\\) must have full column rank.

        If \\(X\\) does **not** have full column rank, the columns of \\(X\\) are linearly dependent. There exists a non-zero vector \\(v \\in \\mathbb{R}^k\\) such that:

        $$
        Xv = 0
        $$

        Now, consider the quadratic form \\(v'(X'X)v\\):

        $$
        v'(X'X)v = (Xv)'(Xv) = 0
        $$

        For a non-zero vector \\(v\\), this implies that \\(X'X\\) is **not positive definite**. A matrix that is not positive definite is not invertible (it is singular).

        ---

        ## 2. **\\(E(u) = 0\\)**

        We need to show that \\(E(u) = 0\\). Let's take mean independence (MLR.3):

        $$
        E(u | X) = 0
        $$

        Using the **law of iterated expectations**, we have:

        $$
        E(u) = E(E(u | X)) = E(0) = 0
        $$

        ---

        ## 3. **Linearity of \\(\\hat{\\beta}\\)**:

        The OLS estimator \\(\\hat{\\beta}\\) is linear in \\(y\\), as it can be written as:

        $$
        \\hat{\\beta} = A y \\quad \\text{where} \\quad A = (X'X)^{-1} X'
        $$

        Since \\(A\\) is a matrix depending only on \\(X\\), \\(\\hat{\\beta}\\) is a linear function of \\(y\\).

        ---

        ## 4. **Unbiasedness of \\(\\hat{\\beta}\\)**:

        The expected value of \\(\\hat{\\beta}\\) is:

        $$
        E(\\hat{\\beta}) = E((X'X)^{-1} X'y)
        $$

        Substitute \\(y = X\\beta + u\\):

        $$
        E(\\hat{\\beta}) = (X'X)^{-1} X' E(X\\beta + u)
        $$

        Distribute the parentheses:

        $$
        E(\\hat{\\beta}) = (X'X)^{-1} X'X\\beta + (X'X)^{-1} X'E(u)
        $$

        Since \\(E(u) = 0\\) and \\((X'X)^{-1} X'X = 1\\), we have:

        $$
        E(\\hat{\\beta}) = \\beta
        $$

        Hence, \\(\\hat{\\beta}\\) is an unbiased estimator of \\(\\beta\\).

        ---

        ## 5. **Variance of \\(\\hat{\\beta}\\)**:

        The variance of \\(\\hat{\\beta}\\) is:

        $$
        \\begin{align*}
        \\text{Var}(\\hat{\\beta}) &= \\text{Var}((X'X)^{-1} X'y) \\\\
        &= (X'X)^{-1} X' \\text{Var}(y) X (X'X)^{-1} \\quad &&\\text{since} \\quad \\text{Var}(ay) = a\\text{Var}(y)a' \\\\
        &= (X'X)^{-1} X' \\sigma^2 X (X'X)^{-1} \\quad &&\\text{since} \\quad \\text{Var}(y) = \\sigma^2 I \\\\
        &= (X'X)^{-1} X'X \\sigma^2 (X'X)^{-1} \\quad &&\\text{since} \\quad (X'X)^{-1} X'X = 1 \\\\
        &= \\sigma^2 (X'X)^{-1}
        \\end{align*}
        $$

        ---

        ## 6. **Minimum Variance (Best)**:

        Let \\(\\tilde{\\beta} = C y\\) be another linear unbiased estimator, where \\(C\\) is a matrix. Since \\(\\tilde{\\beta}\\) is unbiased, we have:

        $$
        E( \\tilde{\\beta}) = C X \\beta = \\beta \\quad \\Rightarrow \\quad C X = I
        $$

        The variance of \\(\\tilde{\\beta}\\) is:

        $$
        \\text{Var}(\\tilde{\\beta}) = C \\text{Var}(y) C' = C \\sigma^2 I C' = \\sigma^2 C C'
        $$

        The variance of \\(\\hat{\\beta}\\) (the OLS estimator) is:

        $$
        \\text{Var}(\\hat{\\beta}) = \\sigma^2 (X'X)^{-1}
        $$

        We now compute the difference in variance between \\(\\tilde{\\beta}\\) and \\(\\hat{\\beta:

        $$
        \\text{Var}(\\tilde{\\beta}) - \\text{Var}(\\hat{\\beta}) = \\sigma^2 (C C' - (X'X)^{-1})
        $$

        Substitute \\(C = (X'X)^{-1} X' + D\\), since it must differ from the OLS estimator, where \\(D X = 0\\), which ensures it is still unbiased:

        $$
        \\begin{align*}
        \\text{Var}(\\tilde{\\beta}) - \\text{Var}(\\hat{\\beta}) &= \\sigma^2 ((X'X)^{-1} X' + D)((X'X)^{-1} X' + D)' - (X'X)^{-1})  \\\\
        &= \\sigma^2 ((X'X)^{-1} X'X (X'X)^{-1} + DX(X'X)^{-1} + (X'X)^{-1} (DX)' + DD') \\\\
        &= \\sigma^2 ((X'X)^{-1} + DD')
        \\end{align*}
        $$

        Since \\(D D'\\) is positive semi-definite, it follows that:

        $$
        \\begin{align*}
        \\sigma^2 ( (X'X)^{-1} + DD' ) &\\geq \\sigma^2 (X'X)^{-1}  \\\\
        \\text{Var}(\\tilde{\\beta}) &\\geq \\text{Var}(\\hat{\\beta})
        \\end{align*}
        $$


        Therefore, \\(\\hat{\\beta}\\) has the minimum variance among all linear unbiased estimators, proving that \\(\\hat{\\beta}\\) is **BLUE** (Best Linear Unbiased Estimator)[^1].

        [^1]: [Hansen (2022)](https://www.econometricsociety.org/publications/econometrica/2022/05/01/modern-gauss%E2%80%93markov-theorem) showed, that if OLS is BLUE, then it may automatically be BUE.
        """
    )
    return


if __name__ == "__main__":
    app.run()
