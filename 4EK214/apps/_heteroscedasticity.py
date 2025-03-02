# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "altair==5.5.0",
#     "numpy==2.2.3",
#     "pandas==2.2.3",
#     "scipy==1.15.2",
#     "statsmodels==0.14.4",
# ]
# [tool.marimo.display]
# theme = "dark"
# ///

import marimo

__generated_with = "0.11.5"
app = marimo.App(width="medium", app_title="Heteroscedasticity")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import altair as alt
    return alt, mo


@app.cell
def _(alt):
    _ = alt.theme.enable('dark')
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ---
        # Heteroscedasticity
        ---
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        Heteroskedasticity occurs when the variance for all observations in a data set are not the same. Let's examine

        1. what are the consequences of heteroscedasticity,
        2. how to detect it, and
        3. how to deal with it.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""The analysis is done in python. It is not necessary to understand the code. You can ignore it, but it is a great way to get a hands on experience. If you want to follow, you need to install some packages first."""
    ).style(text_align="justify")
    return


@app.cell(hide_code=True)
def _(mo):
    import pandas as pd
    import numpy as np
    import statsmodels.api as sm
    from statsmodels.stats.diagnostic import het_breuschpagan
    from scipy.stats import chi2, t

    mo.show_code()
    return chi2, het_breuschpagan, np, pd, sm, t


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        <div style="height: 0.5em;"></div>

        We will use a simple dataset with 2 variables, so 1 dependent variable and 1 regressor:

        - \\( y \\) = household monthly food expenditures
        - \\( x \\) = household monthly income

        This dataset is available in the statsmodels package. Let's load it and look at the data.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo, sm):
    food = sm.datasets.engel.load_pandas().data
    food
    mo.show_code()
    return (food,)


@app.cell(hide_code=True)
def _(food, mo):
    mo.ui.table(food)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        <div style="height: 0.5em;"></div>

        Now, we can estimate a simple linear regression model

        \\[
        \\text{{Food expeditures}} = \\beta_0 + \\beta_1 \\times \\text{{Income}} + u
        \\]

        In python, we can use statsmodels to estimate the coefficients.
        """
    )
    return


@app.cell(hide_code=True)
def _(food, mo, sm):
    X = sm.add_constant(food["income"])
    y = food["foodexp"]
    model_ols = sm.OLS(y, X).fit()

    beta_ols = model_ols.params
    r2_ols = model_ols.rsquared
    bse_ols = model_ols.bse
    resid = model_ols.resid
    fitted_values = model_ols.fittedvalues
    N = int(model_ols.nobs)
    k = beta_ols.count() - 1
    print(model_ols.summary())
    mo.show_code()
    return (
        N,
        X,
        beta_ols,
        bse_ols,
        fitted_values,
        k,
        model_ols,
        r2_ols,
        resid,
        y,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        <div style="height: 0.5em;"></div>

        We can look at the output below of the model. While it is possible to begin by interpreting the F-test and R\\( ^2 \\), it is wise to first check for heteroscedasticity. If heteroscedasticity is present, we may need to re-estimate the model.

        <div style="height: 0.5em;"></div>
        """
    ).style({"text-align": "justify"})
    return


@app.cell(hide_code=True)
def _(mo, model_ols):
    with mo.redirect_stdout():
        print(model_ols.summary())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ---
        ## 1. **Consequences of Heteroskedasticity**
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        Heteroskedasticity (homoscedasticity) of the error term occurs when the variance for all observations in a data set are not (are) the same. It therefore makes the variance of the error term differ between observations, which is a vialoation of the Gauss-Markov thoerem. Specifically, it violates the assumption (MLR.5) that the conditional variance of the error term is constant, therefore

        \\[
        \\text{var}(u|X) \\neq \\sigma^2
        \\]

        When heteroskedasticity of the error term is present, then:

        1. \\( \\hat{\\beta}_{ols} \\) no longer have the smallest variance \\(\\rightarrow\\) \\( \\hat{\\beta}_{ols} \\) is **inefficient** \\(\\rightarrow\\) \\( \\hat{\\beta}_{ols} \\) is no longer BLUE as it is **no longer the best** linear unbiased estimator \\(\\rightarrow\\) there exists another linear unbiased estimator with smaller variance.

        2. Standard errors calculated by the standard formula \\( SE(\\hat{\\beta}) = \\sqrt{\\hat{\\sigma}^2 \\cdot (X'X)^{-1}} \\) are biased and inconsistent. Therefore, everything that uses standard errors may be invalid, such as t-test, F-test, or confidence intervals.

        Most real-world data will probably be heteroskedastic. (1.) is usually not a problem for large samples, and OLS is good enough, but (2.) needs to be dealt with even for large samples.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ---
        ## 2. **Detecting Heteroskedasticity**
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""### 2.1 **Residual Plots**""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """One (mostly flawed) way of detecting heteroskedasticity is by visually analyzing plot of residuals (since residuals are estimates of the error term) against the fitted values (\\( \\hat{y} \\)). If there is an evident pattern in the plot, then residuals are heteroskedastic."""
    ).style({"text-align": "justify"})
    return


@app.cell(hide_code=True)
def _(alt, fitted_values, food, mo, resid):
    food_plot = food.copy()
    food_plot["fitted_values"] = fitted_values
    food_plot["resi"] = resid

    chart = alt.Chart(food_plot).mark_circle(size=20).encode(
        x=alt.X("fitted_values", axis=alt.Axis(title="Fitted values")),
        y=alt.Y("resi", axis=alt.Axis(title="Residuals")),
        tooltip=["income", "foodexp"],
        color=alt.value("#56B4E9"),
        stroke=alt.value("black"),
        strokeWidth=alt.value(1),
    ).properties(
        width=950, height=400, title="Residuals vs. Fitted values"
    ) + alt.Chart(
        food
    ).mark_rule(
        color="#D55E00", strokeDash=[5, 5]
    ).encode(
        y=alt.datum(0)
    )

    final_chart = mo.ui.altair_chart(
        chart.configure_axis(
            titleFontSize=12, labelFontSize=10, grid=False
        ).configure_title(fontSize=16),
        chart_selection=False
    )
    return chart, final_chart, food_plot


@app.cell(hide_code=True)
def _(final_chart, mo):
    mo.md(
        f"""
    One (mostly flawed) way of detecting heteroskedasticity is by visually analyzing plot of residuals (since residuals are estimates of the error term) against the fitted values (\\( \\hat{{y}} \\)). If there is an evident pattern in the plot, then residuals are heteroskedastic.

    {mo.as_html(final_chart)}

    In our case, there is a clear pattern. The variance of residuals steadily increases as the fitted values increases.
    """
    ).style(text_align="justify")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""### 2.2 **The Breusch-Pagan test**""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        A more formal (and safer) way of detecting heteroskedasticity is by using statistical tests. Breusch-Pagan test is one such test. It involves using a variance function and using a \\( \\chi^2 \\)-test to test the null hypothesis that the residuals (and therefore the error term) are homoscedastic. 

        To start, we need a variance function, a function that relates the variance to a set of explanatory variables \\( z_{1}, z_{2}, \\ldots, z_{s} \\) that are potentially different from \\( x_{1}, x_{2}, \\ldots, x_{s} \\). For example, income might explain the average consumption (mean), but education level, location, or age might explain the variability (variance) in consumption for different income levels. However, usually, all the regressors \\( \\boldsymbol{x} \\) are used at the place of \\( \\boldsymbol{z} \\). Nevertheless, a more general form of the variance function is 

        \\[
        \\text{var}(y_i|\\boldsymbol{z_i}) = E(u_i^2|\\boldsymbol{z_i})= h(\\alpha_0 + \\alpha_1 z_{i1} + \\alpha_2 z_{i2} + \\ldots + \\alpha_s z_{is})
        \\]

        Notice in the above equation that the variance of \\( y_i \\) changes for each observation depending on the values of \\( \\boldsymbol{z_i} \\). If \\( \\alpha_1 = \\alpha_2 = \\ldots = \\alpha_s = 0 \\), then the variance is constant, and thus the error term is homoscedastic. Recall that we are testing the following null and alternative hypotheses: 

        \\[
        H_0: \\alpha_1 = \\alpha_2 = \\ldots = \\alpha_s = 0 \\\\
        H_1: \\text{At least one of the } \\alpha_1, \\alpha_2, \\ldots, \\alpha_s \\text{ is not zero}
        \\]

        To obtain a test statistic for our hypothesis test, we consider the linear variance function \\( h(\\alpha_0 + \\alpha_1 z_{2} + \\ldots + \\alpha_s z_{s}) \\). Let's drop the index i and use vectors for clarity. We would like to estimate the following model 

        \\[
        u^2 = \\alpha_0 + \\alpha_1 z_{1} + \\ldots + \\alpha_s z_{s} + v
        \\]

        However, since the error term \\( u^2 \\) is unobservable, we have to use their estimates, that is residuals \\( \\hat{u}^2 \\). We then get

        \\[
        \\hat{u}^2 = \\alpha_0 + \\alpha_1 z_{1} + \\ldots + \\alpha_s z_{s} + v
        \\]

        We are interested in figuring out whether the variables \\( z_{1}, z_{2}, \\ldots, z_{s} \\) help explain the variation in the residual \\( \\hat{u}^2 \\), and since \\( R^2 \\) measures the proportion of variance in \\( \\hat{u}_i^2 \\) explained by the \\( \\boldsymbol{z} \\), it is a natural candidate for a test statistic. When \\( H_0 \\) is true, the sample size \\( N \\) multiplied by \\( R^2 \\) has a \\( \\chi^2 \\) distribution with \\( k-1 \\) ( # of estimated coefficients \\( - \\) 1) degrees of freedom. Since we have only 1 regressor and a constant, the test statistic is then

        \\[
        \\chi^2 = N \\times R^2 \\sim \\chi^2_{1}
        \\]

        which then gets used to test the following hypothesis

        \\[
        H_0: \\alpha_1 = 0 \\\\
        H_1: \\alpha_1 \\neq 0
        \\]

        The test effectively compares two models:

        \\begin{align*}
        u^2 &= \\alpha_0 + \\alpha_1 z_{1} + \\ldots + \\alpha_s z_{s} + v \\\\
        u^2 &= \\alpha_0 + v
        \\end{align*}

        We will conduct the Breusch-Pagan test 'by hand' first, and with the help of statsmodels second.
        """
    ).style({"text-align": "justify"})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""#### 2.2.1 **The Breusch-Pagan test by hand**""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""To do the Breusch-Pagan test by hand, we need to square the residuals from the ols model we estimated before. Then, we simply estimate the model above, where we try to fit the regressors (Income in this case) to the squared residuals."""
    ).style({"text-align": "justify"})
    return


@app.cell(hide_code=True)
def _(food, mo, resid, sm):
    resid_sq = resid**2
    X_var = sm.add_constant(food["income"])
    model_var = sm.OLS(resid_sq, X_var).fit()

    mo.show_code()
    return X_var, model_var, resid_sq


@app.cell
def _(mo):
    mo.md(r"""<div style="height: 0.5em;"></div>""")
    return


@app.cell(hide_code=True)
def _(mo, model_var):
    with mo.redirect_stdout():
        print(model_var.summary())
    return


@app.cell
def _(mo):
    mo.md(r"""<div style="height: 0.5em;"></div>""")
    return


@app.cell(hide_code=True)
def _(mo, model_var):
    r_sq_bp = model_var.rsquared
    alpha = 0.05

    mo.show_code()
    return alpha, r_sq_bp


@app.cell(hide_code=True)
def _(N, alpha, mo, r_sq_bp):
    mo.md(
        f"""
    <div style="height: 0.5em;"></div>

    Looking at the output, we have got

    \\[
    R_{{BP}}^2 = {r_sq_bp:.2f} \\\\
    N_{{BP}} = {N}
    \\]

    Therefore

    \\[
    \\chi_{{BP}}^2 = {N} \\times {r_sq_bp:.2f} = {N*r_sq_bp:.2f}
    \\]

    Let’s get the critical value at {1-alpha} for \\( \\chi^2\\) with 1 degree of freedom and the p-value.
    """
    )
    return


@app.cell(hide_code=True)
def _(N, chi2, mo, r_sq_bp):
    chi2_stat = N * r_sq_bp
    critical_value = chi2.ppf(0.95, df=1)
    p_val_bp = chi2.sf(chi2_stat, df=1)

    mo.show_code()
    return chi2_stat, critical_value, p_val_bp


@app.cell(hide_code=True)
def _(chi2_stat, critical_value, p_val_bp):
    if chi2_stat > critical_value:
        reject_hand = f"Since the p-value = {p_val_bp:.4f} < \\( \\alpha \\) = 0.05, or alternatively, since the observed statistic = {chi2_stat:.4f} > critical value = {critical_value:.4f}, we **reject** the null hypothesis and conclude that the error term is heteroskedastic."
    else:
        reject_hand = f"Since the p-value = {p_val_bp:.4f} > \\( \\alpha \\) = 0.05, or alternatively, since the observed statistic = {chi2_stat:.4f} < critical value = {critical_value:.4f}, we **fail to reject** the null hypothesis and conclude that the error term is homoskedastic."
    return (reject_hand,)


@app.cell(hide_code=True)
def _(chi2_stat, critical_value, mo, p_val_bp):
    mo.md(
        f"""
    | **Metric**                                     | **Value**            |
    |------------------------------------------------|----------------------|
    | **Test Statistic (\\( \\chi^2\\))**             | {chi2_stat:.4f}      |
    | **Critical Value (\\( \\chi^2\\), 95%, df=1)** | {critical_value:.4f} |
    | **P-value (P( \\( \\chi^2\\) > Test Statistic \\| df=1))**| {p_val_bp:.4f} |
    """
    ).center()
    return


@app.cell(hide_code=True)
def _(mo, reject_hand):
    mo.md(
        f"""
    {reject_hand}
    """
    ).style(text_align="justify")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        <div style="height: 0.5em;"></div>

        #### 2.2.2 **The Breusch-Pagan test using statsmodels**
        """
    )
    return


@app.cell(hide_code=True)
def _(X, het_breuschpagan, mo, model_ols):
    bp_test = het_breuschpagan(model_ols.resid, X)
    labels = ["LM Statistic", "LM-Test p-value", "F-Statistic", "F-Test p-value"]
    bp_results = dict(zip(labels, bp_test))
    lm_stat = bp_results["LM Statistic"]
    lm_pval = bp_results["LM-Test p-value"]
    f_stat = bp_results["F-Statistic"]
    f_pval = bp_results["F-Test p-value"]
    mo.show_code()
    return bp_results, bp_test, f_pval, f_stat, labels, lm_pval, lm_stat


@app.cell(hide_code=True)
def _(alpha, lm_pval, p_val_bp):
    if lm_pval < alpha:
        reject_test = f"Since the p-value = {p_val_bp:.4f} < \\( \\alpha \\) = 0.05, we **reject** the null hypothesis and conclude that the error term is heteroskedastic."
    else:
        reject_test = f"Since the p-value = {p_val_bp:.4f} is > \\( \\alpha \\) = 0.05, we **fail to reject** the null hypothesis and conclude that the error term is homoskedastic."
    return (reject_test,)


@app.cell(hide_code=True)
def _(lm_pval, lm_stat, mo, reject_test):
    mo.md(
        f"""
    The Breusch-Pagan test results:
    {
    mo.md(
        f"""
    | **Metric**                     | **Value**      |
    |--------------------------------|----------------|
    | **LM Statistic (\\(\\chi^2\\))** | {lm_stat:.4f}  |
    | **LM-Test p-value**           | {lm_pval:.4f}  |
    """
    ).center()
    }

    {reject_test} You can see, that both tests have the same test statistics.
    """
    ).style({"text-align": "justify"})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ---
        ## 3. Resolving Heteroskedasticity
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        Now that we have identified that our residuals are heteroscedastic, what can we do about it? Recall that the two main consequences of heteroskedasticity are:

        1. Ordinary least squares no longer produces the best estimators. 
        2. Standard errors computed using least squares can be incorrect and misleading.
        """
    ).style({"text-align": "justify"})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""### 3.1 **Regression With Robust Standard Errors**""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        If we are willing to accept the fact that OLS is no longer BLUE, we can still perform our regression analysis to correct the issue of incorrect standard errors so that our confidence intervals and hypothesis tests are valid. We do this by using heteroskedasticity-consistent standard errors or simply robust standard errors. The concept of robust standard errors was suggested by Halbert White.

        #### a) Matrix version

        The standard errors of the OLS estimator in a simple linear regression model is given by:

        \\[
        \\text{SE}(\\hat{\\beta}) = \\sqrt{\\text{diag}\\left( (X'X)^{-1} X' \\Omega X (X'X)^{-1} \\right)} = \\sqrt{\\text{diag}\\left( (X'X)^{-1} X' \\sigma^2 I X (X'X)^{-1} \\right)} = \\sqrt{\\text{diag}\\left( \\sigma^2 (X'X)^{-1} \\right)}
        \\]

        White's robust standard errors get adjusted for heteroskedasticity by replacing \\(\\sigma_i^2\\) with the squared OLS residuals \\(\\hat{u}_i^2\\) and includes a degrees of freedom adjustment:

        \\[
        \\text{SE}(\\hat{\\beta})^{\\text{Robust}} = \\sqrt{\\text{diag}\\left( \\frac{N}{N - K} \\cdot (X'X)^{-1} X' \\Omega X (X'X)^{-1} \\right)} = \\sqrt{\\text{diag}\\left( \\frac{N}{N - K} \\cdot (X'X)^{-1} \\left( \\sum_{i=1}^{N} \\hat{u}_i^2 \\cdot X_i X_i' \\right) (X'X)^{-1} \\right)}
        \\]

        #### b) Algebraic version

        The standard error of the OLS estimator \\(\\beta_1\\) in a simple linear regression model is given by:

        \\[
        \\text{SE}(\\hat{\\beta}_1) = \\sqrt{\\text{Var}(\\hat{\\beta}_1)} = \\sqrt{\\frac{\\sum_{i=1}^{N} (x_i - \\bar{x})^2 \\sigma^2}{\\left(\\sum_{i=1}^{N} (x_i - \\bar{x})^2\\right)^2}} = \\sqrt{\\frac{\\sigma^2}{\\sum_{i=1}^{N} (x_i - \\bar{x})^2}}
        \\]

        White's robust standard errors get adjusted for heteroskedasticity by replacing \\(\\sigma_i^2\\) with the squared OLS residuals \\(\\hat{u}_i^2\\) and includes a degrees of freedom adjustment:

        \\[
        \\text{SE}(\\hat{\\beta}_1)^{\\text{robust}} = \\sqrt{\\text{Var}(\\hat{\\beta}_1)^{\\text{robust}}} = \\sqrt{\\frac{N}{N - K} \\cdot \\frac{\\sum_{i=1}^{N} \\left[(x_i - \\bar{x})^2 \\hat{u}_i^2\\right]}{\\left(\\sum_{i=1}^{N} (x_i - \\bar{x})^2\\right)^2}}
        \\]

        #### c) Other estimators
        Few examples of heteroscedasticity-consistent estimators of \\( \\text{Var}(\\hat{\\beta})^{\\text{robust}} \\):

        \\begin{align*}
        \\text{HC0}&: \\quad \\text{Var}(\\hat{\\beta})^{\\text{robust}} = (X'X)^{-1} X' \\text{diag}(u_i^2) X (X'X)^{-1} \\\\
        \\text{HC1}&: \\quad \\text{Var}(\\hat{\\beta})^{\\text{robust}} = \\frac{N}{N - K} \\cdot (X'X)^{-1} X' \\text{diag}(u_i^2) X (X'X)^{-1} \\\\
        \\text{HC2}&: \\quad \\text{Var}(\\hat{\\beta})^{\\text{robust}} = (X'X)^{-1} X' \\text{diag}\\left( \\frac{u_i^2}{1 - h_i} \\right) X (X'X)^{-1} \\\\
        \\text{HC3}&: \\quad \\text{Var}(\\hat{\\beta})^{\\text{robust}} = (X'X)^{-1} X' \\text{diag}\\left( \\frac{u_i^2}{(1 - h_i)^2} \\right) X (X'X)^{-1} \\
        \\end{align*}

        where \\(h_i \\) is the leverage of the \\( i \\)-th observation, indicating its influence on the regression model, and can be calculated as \\( h_i = \\mathbf{x}_i (X'X)^{-1} \\mathbf{x}_i' \\).

        Let’s check the standard errors of our estimators for our original model.

        <div style="height: 0.5em;"></div>
        """
    ).style({"text-align": "justify"})
    return


@app.cell(hide_code=True)
def _(mo, model_ols):
    robust_cov = model_ols.get_robustcov_results(cov_type="HC1")
    std_err_rob = robust_cov.bse
    mo.show_code()
    return robust_cov, std_err_rob


@app.cell
def _(mo):
    mo.md(r"""<div style="height: 0.5em;"></div>""")
    return


@app.cell(hide_code=True)
def _(mo, robust_cov):
    with mo.redirect_stdout():
        print(robust_cov.summary())
    return


@app.cell
def _(mo):
    mo.md(r"""<div style="height: 0.5em;"></div>""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        We also need the t-statistic for 95% confidence intervals.

        <div style="height: 0.5em;"></div>
        """
    )
    return


@app.cell
def _(N, alpha, k, mo, t):
    t_975 = t.ppf(1 - alpha / 2, N - k - 1)
    mo.show_code()
    return (t_975,)


@app.cell(hide_code=True)
def _(beta_ols, bse_ols, mo, std_err_rob, t_975):
    mo.md(
        f"""
    <div style="height: 0.5em;"></div>

    Notice that the standard errors changed (quite a lot). Our robust standard errors for \\( \\beta_0 \\) and \\( \\beta_0 \\) are {beta_ols['const']:.2f} and {beta_ols['income']:.2f}, respectively. Everything that is calculated from standard erros changed (e.g., t-ratio or p-values), everything that is not calculated from standard errors stayed the same (e.g., coefficients or R\\( ^2 \\)), since we still estimated the coefficients using OLS. 

    Using a confidence level of 0.95, notice the discrepancy in our confidence intervals for \\( \\beta_1 \\): 

    **White:** \\( \\beta_1 \\pm t_{{cse}}(\\beta_1) = {beta_ols['income']:.2f} \\pm {t_975:.2f} \\times {std_err_rob[1]:.2f} = [{beta_ols['income']-std_err_rob[1]*2.024:.2f}, {beta_ols['income']+std_err_rob[1]*2.024:.2f}] \\)

    **OLS:** \\( \\beta_1 \\pm t_{{cse}}(\\beta_1) = {beta_ols['income']:.2f} \\pm {t_975:.2f} \\times {bse_ols['income']:.2f} = [{beta_ols['income']-bse_ols['income']*2.024:.2f}, {beta_ols['income']+bse_ols['income']*2.024:.2f}] \\)

    Regressing with robust standard errors addresses the issue of computing incorrect interval estimates or incorrect values for our test statistics. However, it doesn’t address the issue of the second consequence of heteroskedasticity, which is the least squares estimators no longer being best. However, this may not be too consequential. Again, if you have a sufficiently large enough sample size (which is generally the case in real-world applications), the variance of your estimators may still be small enough to get precise estimates.
    """
    ).style({"text-align": "justify"})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""### 3.3 Generalized Least Squares with known form of variance (GLS)""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    When the error term is heteroscedastic, and the OLS estimator is therefore no longer BLUE, we can use a different estimator that depends on the variance \\( \\sigma_i^2 \\). This estimator is referred to as the **Generalized Least Squares (GLS)** estimator. Leaving the structure of the model intact, it is possible to turn the heteroskedastic model into a homoskedastic one. When we know the structure of the variance (rarely happens, close to never in social sciences), we can use use that structure and apply GLS.

    The main idea behind this procedure is to weight observations based on their variance. Observations with higher variance (with higher level of uncertainty) have lower weight than those with lower variance (with lower uncertainty). The most important step is the assumption of the type of variance structure.

    When we know the variance structure and therefore know \\( \\sigma_i^2 \\), we can divide the model by \\( \\sigma_i \\) to get a model with homoscedastic error term:

    \\begin{align*}
    \\frac{y_i}{\\sigma_i} &= \\frac{\\beta_0}{\\sigma_i} + \\beta_1 \\frac{x_i}{\\sigma_i} + \\frac{u_i}{\\sigma_i} \\\\
    y_i^* &= \\alpha_0 + \\alpha_1 x_{i}^* + u_i^*
    \\end{align*}

    The error term \\( u_i^* \\) is homoscedastic since

    \\[
    \\text{Var}\\left( \\frac{u_i}{\\sigma_i} \\right) = \\frac{\\text{Var}(u_i)}{\\sigma_i^2} = \\frac{\\sigma_i^2}{\\sigma_i^2} = 1
    \\]

    As an example, let's assume that the variance structure can be expressed as \\( \\sigma^2 x_i^2 \\). We can then remove the heteroscedasticity:

    \\begin{align*}
    \\frac{y_i}{\\sigma_ix_i} &= \\frac{\\beta_0}{\\sigma_ix_i} + \\beta_1 \\frac{x_i}{\\sigma_ix_i} + \\frac{u_i}{\\sigma_ix_i} \\\\
    y_i^* &= \\alpha_0 x_{i}^* + \\alpha_1 + u_i^*
    \\end{align*}

    or

    \\begin{align*}
    \\frac{y_i}{x_i} &= \\frac{\\beta_0}{x_i} + \\beta_1 \\frac{x_i}{x_i} + \\frac{u_i}{x_i} \\\\
    y_i^* &= \\alpha_0 x_{i}^* + \\alpha_1 + u_i^*
    \\end{align*}

    since \\( \\sigma^2 \\) is a constant.
        """
    ).style(text_align="justify")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""### 3.2 **Generalized Least Squares With Unknown Form of Variance (FGLS)**""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        However, we usually do not know the variance structure. When we do not know the structure, we have to estimate it first. This procedure is called **Feasible Generalized Least Squares (FGLS)**. Below is a flowchart of the procedure.

        <div style="height: 0.5em;"></div>
        """
    ).style({"text-align": "justify"})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.mermaid(
        """
    flowchart TD
        B[Fit OLS regression]
        B --> C[Obtain OLS residuals]
        C --> D[Estimate variance structure of the residuals]
        D --> E[Regress the estimated variance structure on original regressors]
        E --> F[Compute weights]
        F --> G[Multiply all the variables by the weights]
        G --> H[Estimate OLS model with the weighted variables]

        %% Define a class for rounded rectangles with transparent fill
        classDef roundedRect fill:transparent, stroke:#333, stroke-width:3px, rx:10, ry:10;

        %% Apply the class to all nodes
        class A,B,C,D,E,F,G,H roundedRect;
    """
    ).center()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        <div style="height: 0.5em;"></div>

        Let's try a general specification of the variance structure of the following form 

        \\[
        \\text{var}(u_i) = \\sigma_i^2 = \\sigma^2 x_i^{\\gamma}
        \\]

        where \\( \\gamma \\) is an unknown parameter. Notice that the variance function depends on a constant term \\( \\sigma^2 \\) and increases as \\( x_i \\) increases. Let’s start by taking the natural logs of both sides of the above equations so that we get 

        \\[
        \\ln(\\sigma_i^2) = \\ln(\\sigma^2) + \\gamma \\ln(x_i) 
        \\]

        Then, we can exponetiate both sides

        \\[
        \\sigma_i^2 = \\exp\\left[\\ln(\\sigma^2) + \\gamma \\ln(x_i)\\right] = \\exp(\\alpha_0 + \\alpha_1 z_i) 
        \\]

        where \\( \\alpha_0 = \\ln(\\sigma^2) \\), \\( \\alpha_1 = \\gamma \\), and \\( z_i = \\ln(x_i) \\). The exponential function is convenient because it ensures that we will get non-negative values for the variances \\( \\sigma_i^2 \\) for all possible values of the parameters \\( \\alpha_0, \\alpha_1, \\ldots, \\alpha_s \\). Returning to the equation \\( \\sigma_i^2 = \\exp(\\alpha_0 + \\alpha_1 z_i) \\), we can rewrite it as 

        \\[
        \\ln(\\sigma_i^2) = \\alpha_0 + \\alpha_1 z_i
        \\]

        We now have an equation in which we can estimate the unknown parameters \\( \\alpha_0 \\) and \\( \\alpha_1 \\). We can do this the same way we obtain estimates for the parameters \\( \\beta_0 \\) and \\( \\beta_1 \\) in a simple regression model \\( y_i = \\beta_0 + \\beta_1 x_i + u_i \\) using ordinary least squares. We can do this by using the squares of our least squares residuals \\( u_i^2 = y_i - \\hat{\\beta}_0 - \\hat{\\beta}_1 x_i \\) as our observations. That is, we can write the above equation as 

        \\[
        \\ln(\\hat{u}_i^2) = \\alpha_0 + \\alpha_1 z_i + v_i
        \\]

        We can now apply least squares to get our parameter estimates. Let’s use our food expenditure data that we’ve been working with so far.

        <div style="height: 0.5em;"></div>
        """
    ).style({"text-align": "justify"})
    return


@app.cell(hide_code=True)
def _(food, mo, np, resid_sq, sm):
    log_income = np.log(food["income"])
    log_resid_sq = np.log(resid_sq)
    model_var_log = sm.OLS(log_resid_sq, sm.add_constant(log_income)).fit()
    beta_white = model_var_log.params

    mo.show_code()
    return beta_white, log_income, log_resid_sq, model_var_log


@app.cell
def _(mo):
    mo.md(r"""<div style="height: 0.5em;"></div>""")
    return


@app.cell(hide_code=True)
def _(mo, model_var_log):
    with mo.redirect_stdout():
        print(model_var_log.summary())
    return


@app.cell
def _(mo):
    mo.md(r"""<div style="height: 0.5em;"></div>""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        The next step is to transform the observations in such a way that the transformed model has a constant error variance. To do so, we can obtain variance estimates from 

        \\[ 
        \\hat{\\sigma}_i^2 = \\exp(\\alpha_0 + \\alpha_1 z_i)
        \\] 

        and then divide both sides of the regression model \\( y_i = \\beta_0 + \\beta_1 x_i + u_i \\) by \\( \\sigma_i \\). Doing so yields the following equation 

        \\[ 
        \\frac{y_i}{\\sigma_i} = \\beta_0 \\left( \\frac{1}{\\sigma_i} \\right) + \\beta_1 \\left( \\frac{x_i}{\\sigma_i} \\right) + \\frac{u_i}{\\sigma_i} 
        \\] 

        The variance of the transformed error is homoskedastic because 

        \\[ 
        \\text{Var}\\left( \\frac{u_i}{\\sigma_i} \\right) = \\frac{1}{\\sigma_i^2} \\text{Var}(u_i) = \\frac{1}{\\sigma_i^2} \\sigma_i^2 = 1 
        \\] 

        Using the estimates of our variance function \\( \\sigma_i^2 \\) in place of \\( \\sigma_i^2 \\) to obtain the generalized least squares estimators of \\( \\beta_0 \\) and \\( \\beta_1 \\), we define the transformed variables and apply weighted least squares to the equation 

        \\begin{align*}
        \\frac{Y_i}{\\sigma_i} &= \\frac{\\beta_0}{\\sigma_i} + \\beta_1 \\frac{X_{i1}}{\\sigma_i} + \\frac{u_i}{\\sigma_i} \\\\
        Y_i^* &= \\alpha_0 + \\alpha_1 X_{i1}^* + u_i^*
        \\end{align*}

        While we used weights to mean \\( \\sqrt{\\frac{1}{\\text{Var Structure}}} \\), a lot of packages and sofware (Gretl and Statsmodels included) use weights to mean \\( \\frac{1}{\\text{Var Structure}} \\), therefore, one have to supply the latter version, if the procedure asks for weigths. Here’s how we can do it using Python.

        <div style="height: 0.5em;"></div>
        """
    ).style(text_align="justify")
    return


@app.cell(hide_code=True)
def _(X_var, food, mo, model_var_log, np, sm):
    varfunc = np.exp(model_var_log.fittedvalues)

    weights = 1 / varfunc
    model_gls = sm.WLS(food["foodexp"], X_var, weights=weights).fit()
    beta_gls = model_gls.params
    bse_gls = model_gls.bse
    r2_gls = model_gls.rsquared
    mo.show_code()
    return beta_gls, bse_gls, model_gls, r2_gls, varfunc, weights


@app.cell
def _(mo):
    mo.md(r"""<div style="height: 0.5em;"></div>""")
    return


@app.cell(hide_code=True)
def _(mo, model_gls):
    with mo.redirect_stdout():
        print(model_gls.summary())
    return


@app.cell
def _(mo):
    mo.md(r"""<div style="height: 0.5em;"></div>""")
    return


@app.cell(hide_code=True)
def _(beta_gls, beta_ols, mo):
    mo.md(
        f"""
    Our fitted models are: 

    \\begin{{align*}}
    \\textbf{{OLS}}: \\hat{{Y}} &= {beta_ols["const"]:.2f} + {beta_ols["income"]:.2f} \\times \\text{{Income}} \\\\
    \\textbf{{GLS}}: \\hat{{Y}} &= {beta_gls["const"]:.2f} + {beta_gls["income"]:.2f} \\times \\text{{Income}} 
    \\end{{align*}}
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        <div style="height: 0.5em;"></div>

        And below is the comparison of standard errors and R\\(^2\\) of the two models:
        """
    )
    return


@app.cell(hide_code=True)
def _(bse_gls, bse_ols, mo, r2_gls, r2_ols):
    mo.md(
        f"""
    Metric         | OLS                     | WLS                     |
    -------------- | ----------------------- | ----------------------- |
    \\( R^2 \\)      | {r2_ols:.4f}            | {r2_gls:.4f}            |
    \\( SE(\\hat{{\\beta}}) \\) | {bse_ols['income']:.4f} | {bse_gls['income']:.4f} |
    """
    ).center()
    return


@app.cell(hide_code=True)
def _(alt, beta_gls, beta_ols, food, mo, pd):
    line_data = pd.DataFrame(
        {
            "income": food["income"],
            "OLS": beta_ols["const"] + beta_ols["income"] * food["income"],
            "GLS": beta_gls["const"] + beta_gls["income"] * food["income"],
        }
    )

    line_data = line_data.melt("income", var_name="model", value_name="foodexp")

    scatter = (
        alt.Chart(food)
        .mark_circle(size=20)
        .encode(
            x=alt.X("income", axis=alt.Axis(title="Income")),
            y=alt.Y("foodexp", axis=alt.Axis(title="Food Expenditure")),
            tooltip=["income", "foodexp"],
            color=alt.value("#56B4E9"),
            stroke=alt.value("black"),
            strokeWidth=alt.value(1),
        )
    )

    line_plot = (
        alt.Chart(line_data)
        .mark_line()
        .encode(
            x="income:Q",
            y="foodexp:Q",
            color=alt.Color(
                "model:N",
                scale=alt.Scale(range=["#009E73", "#E69F00"]),
                legend=alt.Legend(title="Model", orient="top-left"),
            ),
            strokeDash=alt.StrokeDash("model:N", legend=None),
            tooltip=["income", "foodexp", "model"],
        )
    )

    final_chart_2 = mo.ui.altair_chart(
        (scatter + line_plot)
        .configure_axis(titleFontSize=12, labelFontSize=10, grid=False)
        .configure_title(fontSize=16)
        .properties(title="OLS vs. GLS", width=950, height=400),
        chart_selection=False
    )
    return final_chart_2, line_data, line_plot, scatter


@app.cell(hide_code=True)
def _(final_chart_2, mo):
    mo.md(
        f"""
    Finally, we can look at how the fitted values between the modesl differ on the graph below.

    {mo.as_html(final_chart_2)}

        The green line represents the fitted GLS regression line, and the orange dashed line represents the fitted OLS regression line. Based on the comparisons of the models, the GLS model fits slightly better, as it has a higher \\( R^2 \\). Since observations with higher variance are weighted less, the two observations [2551.66, 863.92] and [4957.81, 1827.20] are not able to pull the line down unlike with regular OLS.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ---

        1. [White's paper](https://www.jstor.org/stable/1912934), which was [the most cited paper in economics at least during 1970-2006](https://www.aeaweb.org/articles?id=10.1257/jep.20.4.189), and still might be.
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


if __name__ == "__main__":
    app.run()
