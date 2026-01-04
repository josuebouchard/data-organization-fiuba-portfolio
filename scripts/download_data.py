# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "kagglehub==0.3.13",
#     "numpy==2.4.0",
#     "polars==1.36.1",
#     "rich",
# ]
# ///

import kagglehub
import polars as pl
import ast
import zipfile
from pathlib import Path
from rich.console import Console
from rich.progress import Progress
from rich.markdown import Markdown

"""
# Download and pre-process the dataset

This repository requires the use of different CSVs, most of which are preprocessed versions of "The Movies Dataset" by Rounak Banik from Kaggle.
https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset
"""

# Constants
KAGGLE_DATASET = "rounakbanik/the-movies-dataset"

# File paths
repo_root_path = Path(__file__).parent.parent
dataset_path = repo_root_path / "data"


def _get_kaggle_unzipped_file(dataset: str, file: str) -> zipfile.Path:
    return zipfile.Path(
        root=kagglehub.dataset_download(dataset, path=file),
        at=file,
    )


def _preprocess_keywords(csv):
    OUTPUT_NAME = "keywords.csv"
    (
        pl.scan_csv(csv)
        .select(
            pl.col("id"),
            pl.col("keywords").map_elements(
                lambda elem: ",".join(i.get("name") for i in ast.literal_eval(elem)),
                return_dtype=pl.String,
            ),
        )
        .sink_csv(dataset_path / OUTPUT_NAME)
    )


def _preprocess_movies(csv):
    OUTPUT_NAME = "movies.csv"
    (
        pl.scan_csv(
            csv,
            infer_schema_length=100_000,
        )
        .with_columns(
            pl.col("genres").map_elements(
                lambda elem: ",".join(i.get("name") for i in ast.literal_eval(elem)),
                return_dtype=pl.String,
            ),
            pl.col("belongs_to_collection").map_elements(
                lambda elem: (
                    d.get("name")
                    if isinstance(d := ast.literal_eval(elem), dict)
                    else None
                ),
                return_dtype=pl.String,
            ),
            pl.col("production_companies").map_elements(
                lambda elem: (
                    ",".join(str(i.get("id")) for i in parsed)
                    if isinstance(parsed := ast.literal_eval(elem), list)
                    else None
                ),
                return_dtype=pl.String,
            ),
        )
        .sink_csv(dataset_path / OUTPUT_NAME)
    )


def main():
    console = Console()

    console.print(Markdown("# Dataset Downloader"))

    console.print(":wave: Hello! I'll download the datasets in no time!\n")

    # Create dataset folder if it doesn't exist
    dataset_path.mkdir(exist_ok=True)

    with Progress() as progress:
        task1 = progress.add_task("Downloading keywords.csv", total=100)
        task2 = progress.add_task("Downloading movies.csv", total=100)

        # === Download and pre-process `keywords.csv` ===
        keywords_zip_path = _get_kaggle_unzipped_file(
            KAGGLE_DATASET,
            "keywords.csv",
        )
        progress.update(task1, advance=50)

        _preprocess_keywords(keywords_zip_path.open(encoding="utf8"))
        progress.update(task1, advance=50)

        # === Download and pre-process `movies.csv` ===

        movies_zip_path = _get_kaggle_unzipped_file(
            KAGGLE_DATASET,
            "movies_metadata.csv",
        )
        progress.update(task2, advance=50)

        _preprocess_movies(movies_zip_path.open(encoding="utf8"))
        progress.update(task2, advance=100)

    console.print()
    console.print(":white_check_mark: All datasets were generated and can be found in:")
    console.print(Markdown(f"`{dataset_path.absolute()}`"))

    console.bell()


if __name__ == "__main__":
    main()
