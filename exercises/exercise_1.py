# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "numpy==2.4.0",
#     "pandas==2.3.3",
# ]
# ///

import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium", app_title="Exercise 1")

with app.setup:
    # Initialization code that runs before all other cells
    import marimo as mo
    import pandas as pd
    import numpy as np
    import pathlib

    data_path = pathlib.Path(__file__).parent.parent / "data"


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Exercise 1 - Exploratory Analysis & Data Cleaning

    > Q1 (1 pt). Which are the top 5 languages in which the industry generates the most net income, approximated by the proposed data? And which are the bottom 5? $(\text{net income} = \text{profit} - \text{investment})$

    Since I do not have the investment data, I will approximate it using `budget`, and for the profit, I will use `revenue`.

    That means that I must calculate:

    \[
        \text{net\_income} = \text{revenue} - \text{budget}
    \]

    The movie language will be `original_language`.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Exploratory Analysis
    """)
    return


@app.cell
def _():
    pd.read_csv(data_path/"movies.csv", low_memory=False).info()
    return


@app.cell
def _():
    movies = pd.read_csv(data_path/"movies.csv", low_memory=False)

    mo.vstack([
        mo.md("### Dataset Preview"),
        movies.head(),
        mo.md("### Summary Statistics"),
        movies.describe()
    ])
    return (movies,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Handle repeated and Null IDs

    The definition of an ID and an analysis on the rows with duplicated IDs confirm that two rows with the same ID must be exactly equal. Therefore, keeping only one of such rows will be enough, and it's not important which one it is.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Are there repeated IDs?
    """)
    return


@app.cell
def _(movies):
    any(movies['id'].duplicated())
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### These are the duplicated IDs:
    """)
    return


@app.cell
def _(movies):
    movies[movies['id'].duplicated(keep=False)].sort_values(by='id')
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Make a deduped dataset by dropping duplicates
    """)
    return


@app.cell
def _(movies):
    movies_deduped = movies.drop_duplicates(subset=['id'])
    movies_deduped
    return (movies_deduped,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Are there null or empty IDs?
    """)
    return


@app.cell
def _(movies_deduped):
    any(movies_deduped['id'].isnull() | movies_deduped['id'].str.strip() == "")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Are all remaining IDs numeric?

    The `head` performed during the exploratory analysis would suggest that all IDs are numeric, but the `info` shows that the datatype is `object`.
    """)
    return


@app.cell
def _(movies_deduped):
    all(movies_deduped['id'].str.strip().str.isnumeric())
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### These are the non-numeric IDs:
    """)
    return


@app.cell
def _(movies_deduped):
    movies_deduped[~movies_deduped['id'].str.isnumeric()]
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Remove invalid IDs and cast ID to numeric

    The movies shown above seem to be corrupted. It's decided to remove such films since they cannot be recovered.
    """)
    return


@app.cell
def _(movies_deduped):
    _non_numeric_ids_index = movies_deduped[~movies_deduped['id'].str.isnumeric()].index
    movies_id_clean = movies_deduped.drop(_non_numeric_ids_index)
    movies_id_clean["id"] = pd.to_numeric(movies_id_clean["id"])

    movies_id_clean.head(10)
    return (movies_id_clean,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Analizing Budget and Revenue

    The info of the file shows that `revenue` is of type `float64`, but `budget` is not of numeric type (it's of `object` datatype). The exploratory analysis shows that `budget` seems to be numeric, so there must be anomalies.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Search for anomalies
    """)
    return


@app.cell
def _(movies_id_clean):
    # Find non numeric budgets
    _non_numeric_budgets = movies_id_clean.loc[movies_id_clean['budget'].str.isnumeric() == False, 'budget'].index

    movies_id_clean.loc[_non_numeric_budgets, :]
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    The fact that there are no results, seems to indicate that the cases where the budget was not a number was due to the corruption shown above.

    With this decission taken, I proceed to convert the budget into numeric.
    """)
    return


@app.cell
def _(movies_id_clean):
    movies_clean = movies_id_clean.copy()
    movies_clean["budget"] = pd.to_numeric(movies_id_clean["budget"])
    return (movies_clean,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Analyzing Original Language
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    I'll start by assuming that there are not many possible languages. I'll list all the unique ones and see where that leads me.
    """)
    return


@app.cell
def _(movies_clean):
    movies_clean["original_language"].unique()
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    There are no anomalies. Given that I won't add more rows, and that there are few languages for so many movies, I'll convert it to a categorical in the next section.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Making a clean dataset for the exercise

    Now that I have all the columns that I need for the exercise clean (`id`, `budget`, `revenue`, `original_language`), I proceed to create a trimmed dataset to work on.

    Furthermore, I delete all the movies for which I don't there is no `id`, `budget` or `revenue`, meaning they are either `NaN` or `0`. Knowing that there won't be any more `NaN`s, I also use `convert_dtypes` to convert them to `int`.
    """)
    return


@app.cell
def _(movies_clean):
    movies_ex = movies_clean[["id", "budget", "revenue", "original_language"]].copy().dropna()
    movies_ex = movies_ex[(movies_ex['budget'] > 0) & (movies_ex['revenue'] > 0)]
    movies_ex = movies_ex.convert_dtypes()
    movies_ex["original_language"] = movies_ex["original_language"].astype("category")

    movies_ex
    return (movies_ex,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Calculate Net Income
    """)
    return


@app.cell
def _(movies_ex):
    movies_ex['net_income'] = movies_ex['revenue'] - movies_ex['budget']
    movies_ex.head(5)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    In order to determine the languages with greater/lesser net income, I'll take the sum of the net income by each language.
    """)
    return


@app.cell
def _(movies_ex):
    net_income_sum_per_language = (
        movies_ex[['original_language', 'net_income']]
            .groupby('original_language', observed=True) # Only show observed values
            .aggregate('sum')
            .sort_values(by='net_income', ascending=False)
    )
    net_income_sum_per_language
    return (net_income_sum_per_language,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Results
    """)
    return


@app.cell
def _(net_income_sum_per_language):
    top_movie_languages_by_income = net_income_sum_per_language.head(5)
    bottom_movie_languages_by_income = net_income_sum_per_language.tail(5).sort_values(by='net_income', ascending=True)

    mo.vstack([
        mo.md("### Top 5 movie languages by net income"),
        top_movie_languages_by_income,
        mo.md("### Bottom 5 movie languages by net income"),
        bottom_movie_languages_by_income,
    ])
    return


if __name__ == "__main__":
    app.run()
