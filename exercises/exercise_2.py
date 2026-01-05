# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib==3.10.8",
#     "numpy==2.4.0",
#     "pandas==2.3.3",
#     "scipy==1.16.3",
#     "seaborn==0.13.2",
# ]
# ///

import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import pathlib

    data_path = pathlib.Path(__file__).parent.parent / "data"
    return data_path, mo, np, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Exercise 2

    P21 (2 pt). For the top one thousand most common keywords, obtain the correlation matrix between keywords.
    """)
    return


@app.cell
def _(data_path, mo, pd):
    keywords = pd.read_csv(data_path / "keywords.csv")
    mo.vstack(
        [
            keywords.info(),
            keywords,
        ]
    )
    return (keywords,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cleaning the dataset

    From the previous `.info()` it can be read that while all the `id`s are non-null, there are a couple of null keywords. Given that I cannot operate on null keywords, I decide to remove them.

    Furthermore
    """)
    return


@app.cell
def _(keywords):
    cleaned_keywords = keywords.drop_duplicates().dropna()
    cleaned_keywords
    return (cleaned_keywords,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## "Exploding" the keywords

    The dataset comes with they keywords for each `id` as a comma-separated string. In order to solve the exercise, I don't need `id` to be unique in the dataframe, but I do need each keyword in its own row.
    """)
    return


@app.cell
def _(cleaned_keywords):
    # Split the keywords
    keywords_splitted = cleaned_keywords.copy()
    keywords_splitted['keywords'] = keywords_splitted['keywords'].str.split(',')
    keywords_splitted
    return (keywords_splitted,)


@app.cell
def _(keywords_splitted):
    keywords_exploded = keywords_splitted.explode('keywords').rename(columns={'keywords': 'keyword'})
    keywords_exploded['keyword'] = keywords_exploded['keyword'].str.strip()
    keywords_exploded
    return (keywords_exploded,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Find the 1000 highest ranking keywords

    `id`s are no longer relevant at this point, and count is not necessary.
    """)
    return


@app.cell
def _(keywords_exploded):
    highest_ranking_keywords = (
        keywords_exploded
          .groupby('keyword', as_index=False)
          .count()
          .rename(columns={'id': 'count'})
          .nlargest(1000, 'count')
          [['keyword']]
    )
    highest_ranking_keywords
    return (highest_ranking_keywords,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Get the words for the correlation

    The exercise explicitly asks for correlation matrix **of the 1000 most used keywords**, so I need to remove from `keywords_exploded` all the unused words.

    For that, there were two options:

    1. Performing an *"inner join"* between `keywords_exploded` and `highest_ranking_keywords` on the keywords, and then discarding the unncessary columns.

    2. Taking advantage that the dataset is "small", to use `np.isin`, which is a performant and vectorized operation, to check whether each `keywords_exploded['keyword']` is also in `highest_ranking_keywords['keyword']`.

    For simplicity sake, the second option was taken, also using the optimisation that `highest_ranking_keywords['keyword']` is unique because it comes from a `groupby` on that column.

    The `present` column is added and set to `1` in preparation for the next step.
    """)
    return


@app.cell
def _(highest_ranking_keywords, keywords_exploded, np):
    keywords_filter = np.isin(
        keywords_exploded['keyword'],
        highest_ranking_keywords['keyword'],
        assume_unique=True)

    filtered_keywords = keywords_exploded[keywords_filter].copy()
    filtered_keywords['present'] = 1
    filtered_keywords
    return (filtered_keywords,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    How many films do we still have?
    """)
    return


@app.cell
def _(filtered_keywords):
    filtered_keywords_unique_films_count = len(filtered_keywords['id'].unique())
    filtered_keywords_unique_films_count
    return (filtered_keywords_unique_films_count,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Prepare the dataframe for correlation

    In order to compute the correlation, it's necessary to represent which keywords were present for each film. This is achieved through a *pivot table*.
    """)
    return


@app.cell
def _(filtered_keywords):
    pivoted_filtered_keywords = filtered_keywords.pivot_table(
        index="id",
        columns="keyword",
        values="present",
        fill_value=0,
    )
    pivoted_filtered_keywords
    return (pivoted_filtered_keywords,)


@app.cell(hide_code=True)
def _(filtered_keywords_unique_films_count, mo):
    mo.md(rf"""
    ## Perform the correlation

    Given that we are doing a correlation between 1000 columns and {filtered_keywords_unique_films_count} films, this is going to take some time.

    On my computer it usually takes around half a minute.
    """)
    return


@app.cell
def _(pivoted_filtered_keywords):
    # Beware, it's really slow...
    correlation_matrix = pivoted_filtered_keywords.corr()
    return (correlation_matrix,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Final result
    """)
    return


@app.cell
def _(correlation_matrix):
    correlation_matrix
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Extra (Plots)

    This section was added later, as a practice for plots and an exploration of scipy and KDE plots.
    """)
    return


@app.cell
def _():
    import seaborn as sns
    import matplotlib.pyplot as plt
    return plt, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The following heatmap shows us that the dataset is very sparse (a lot of blackness).
    """)
    return


@app.cell
def _(correlation_matrix, sns):
    sns.heatmap(data=correlation_matrix)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Why so much blackness?

    In order to explain the blackness, I'll try to plot the amount of keywords every film uses.
    """)
    return


@app.cell
def _(keywords_splitted):
    keywords_per_movie = keywords_splitted.copy()[['id']]
    keywords_per_movie['keywords_count'] = keywords_splitted['keywords'].str.len()
    keywords_per_movie
    return (keywords_per_movie,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Histogram (y-axis using logarithmic scale)
    """)
    return


@app.cell
def _(keywords_per_movie, plt, sns):
    _log_plot_df = keywords_per_movie[keywords_per_movie["keywords_count"] > 0]
    _grid_common_config = {"visible": True, "color":"gray", "axis": "y"}

    plt.yscale("log")
    plt.grid(
        **_grid_common_config,
        which="major",
        linestyle="-",
        alpha= 0.5,
    )
    plt.grid(
        **_grid_common_config,
        which="minor",
        linestyle=":",
        alpha= 0.3
    )
    plt.xlabel("amount of keywords used")
    plt.ylabel("amount of movies")
    sns.despine()  # Removes the top and right box lines
    sns.histplot(x=_log_plot_df["keywords_count"], bins=30)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Boxen plot
    """)
    return


@app.cell
def _(keywords_per_movie, plt, sns):
    _grid_common_config = {"visible": True, "color":"gray", "axis": "x"}

    plt.minorticks_on()
    plt.grid(
        **_grid_common_config,
        which="major",
        linestyle="-",
        alpha= 0.5,
    )
    plt.grid(
        **_grid_common_config,
        which="minor",
        linestyle=":",
        alpha= 0.3
    )
    plt.xlabel("amount of keywords used")
    sns.boxenplot(x=keywords_per_movie['keywords_count'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Custom KDE
    """)
    return


@app.cell
def _():
    import seaborn.objects as so
    from scipy import stats
    return so, stats


@app.cell
def _(keywords_per_movie, stats):
    kde = stats.gaussian_kde(keywords_per_movie["keywords_count"])
    return (kde,)


@app.cell
def _(keywords_per_movie):
    min_keywords_count = keywords_per_movie["keywords_count"].min()
    max_keyword_count =  keywords_per_movie["keywords_count"].max()
    return (max_keyword_count,)


@app.cell(hide_code=True)
def _(max_keyword_count, mo):
    xlim_slider = mo.ui.slider(
        start=20,
        stop=max_keyword_count,
        value=40,
        full_width=True,
        label="xlim value:",
        show_value=True,
    )

    xlim_slider
    return (xlim_slider,)


@app.cell(hide_code=True)
def _(mo, xlim_slider):
    kde_integral_slider = mo.ui.range_slider(
        start=0,
        stop=xlim_slider.value,
        value=[0, 20],
        full_width=True,
        label="Integration slider:",
        show_value=True,
    )
    kde_integral_slider
    return (kde_integral_slider,)


@app.cell
def _(kde, kde_integral_slider, mo):
    [_x_l_integral, _x_r_integral] = kde_integral_slider.value
    mo.md(rf"""
    The area between {_x_l_integral} and {_x_r_integral} is equal to: {(kde.integrate_box_1d(_x_l_integral, _x_r_integral) * 100):.3f}%
    """)
    return


@app.cell
def _(kde, kde_integral_slider, keywords_per_movie, np, so, xlim_slider):
    _RESOLUTION = 100

    [_x_l_integral, _x_r_integral] = kde_integral_slider.value

    _x = np.linspace(
        keywords_per_movie["keywords_count"].min(),
        keywords_per_movie["keywords_count"].max(),
        _RESOLUTION,
    )
    _y = kde(_x)

    mask = (_x >= _x_l_integral) & (_x <= _x_r_integral)

    (
        so.Plot(x=_x, y=_y)
        .add(so.Area(), label="KDE")
        .add(
            so.Area(color="orange"),
            x=_x[mask],
            y=_y[mask],
            label="Integration Region",
        )
        .limit(x=(0, xlim_slider.value))
        .show()
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    All the plots tell the same story: 97.212% of the movies use 20 keywords or less. That leads to a very sparse correlation, which in turn results so much blackness in the heat-map.
    """)
    return


if __name__ == "__main__":
    app.run()
