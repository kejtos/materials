# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# [tool.marimo.display]
# theme = "dark"
# ///

import marimo

__generated_with = "0.11.5"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    main_menu = mo.Html(f'<a href="https://kejtos.github.io/materials/" target="_parent">{mo.icon('carbon:return')} Back to the menu</a>')
    return (main_menu,)


@app.cell
def _(main_menu):
    main_menu.right()
    return


@app.cell
def _(mo):
    mo.md("""## R-squared""")
    return


@app.cell
def _(mo):
    mo.md(
        """
        When we have no information about an observation, one way to guess a particular value of \\(y\\) is to use its mean \\(\\overline{y}\\). When we use OLS to estimate a model, we try to use information about the observation \\( (\\mathbf{X}) \\) to improve the original guess of \\(y\\). In other words, we try to use \\( (\\mathbf{X}) \\) to explain the variability of \\(y\\) better than the mean does.

        Therefore, we can measure a so-called goodness-of-fit by looking at what portion of variability did the model explain, which is called coefficient of determinatino, or more commonly, \\(R^2\\). Important to note that \\(R^2\\) tells us how well our model explain the variability of \\(y\\), but it **does not** say anything about the quality of the model itself (more in [Issues with R-squared](https://marimo.io/p/@kejtos/issues-with-r-squared)).

        Let's imagine a simple linear model

        \\[
        y_i=\\beta_0 + \\beta_1x_i+u_i
        \\]

        Total variability of the model is measured as the sum of squares of deviations from the mean TSS (Total Sum of Squares). We then define the explained variability as the sum of squares of the difference between the mean and the fit ESS (Explained Sum of Squares). Last, we define the unexplained variability as the sum of squares of deviations from the fit RSS (Resisual Sum of Squares)(You can find different combinations of abbreviations). Thus, we get:

        \\[
        \\text{TSS} = \\sum_{i=1}^{n} (y_i-\\overline{y}_i)^2 \\\\
        \\text{ESS} = \\sum_{i=1}^{n} (\\hat{y}_i-\\overline{y}_i)^2 \\\\
        \\text{RSS} = \\sum_{i=1}^{n} (y_i-\\hat{y}_i)^2
        \\]

        Using the previous paragraph, since \\(R^2\\) is defined as the portion of variability explained by the model, we can obtained it as

        \\[
        R^2 = \\frac{\\text{ESS}}{\\text{TSS}} = 1-\\frac{\\text{RSS}}{\\text{TSS}}
        \\]
        """
    )
    return


@app.cell
def _(mo):
    mo.md("""You can visualize all the squares and in the following GeoGebra tool. It is likely too blurry, fullscreen recommended (sorry for the flashbang, GeoGebra does not have dark mode).""")
    return


@app.cell
def _(mo):
    mo.iframe('<iframe src="https://www.geogebra.org/material/iframe/id/xxrvsmat/width/1980/height/1080/border/888888/sfsb/true/smb/false/stb/false/stbh/false/ai/false/asb/false/sri/false/rc/true/ld/false/sdz/true/ctl/false" width="1020" height="556" allowfullscreen></iframe>', height=700)
    return


@app.cell
def _(mo):
    main_menu2 = mo.Html(f'<a href="https://kejtos.github.io/marimo_test/" target="_parent">{mo.icon('carbon:return')} Back to the menu</a>')
    return (main_menu2,)


@app.cell
def _(main_menu2):
    main_menu2.right()
    return


if __name__ == "__main__":
    app.run()
