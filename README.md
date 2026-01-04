# Data Organization Portfolio (FIUBA)

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![marimo](https://img.shields.io/badge/Notebooks-marimo-teal.svg)](https://marimo.io/)
[![uv](https://img.shields.io/badge/Package%20Manager-uv-purple.svg)](https://docs.astral.sh/uv/)

A curated collection of data science exercises from the **Data Organization (75.06), Argerich chair** curriculum at the [engineering college of the University of Buenos Aires (FIUBA)](https://fi.uba.ar/), a top-tier engineering program in Argentina. The original implementations were completed during the 2nd Semester of 2022 at FIUBA.

This repository documents my transition from foundational data engineering concepts at FIUBA to modern, reproducible workflows.

## 🛠️ Tech Stack & Skills

### **Core Competencies**
* **Data Processing:**
    * **Pandas:** Extensive use for memory-efficient data manipulation and cleaning.
    * **PySpark (RDD):** Implementation of distributed computing concepts and resilient distributed datasets.
    * **Polars (Current/Upcoming):** Utilizing Polars for high-performance I/O and data acquisition scripts.
* **Machine Learning:** Practical application of feature engineering and predictive modeling using **Scikit-Learn**.
* **Visualization:** Creating insightful, interactive plots using **Plotly** and **Matplotlib** within reactive environments.

### **Modern Workflow**
* **Marimo:** I use reactive Python notebooks to ensure code reproducibility and eliminate "hidden state" bugs.
* **uv:** Fast, disk-space efficient dependency management and project isolation. It also provides fast install of packages.

---

## 📂 Project Structure

* `/scripts`: Infrastructure scripts, including `download_data.py` (powered by Polars).
* `/exercises`: Individual modules covering different phases of the data lifecycle.
* `/data`: (Ignored by Git) Local storage for datasets.

---

## 🚀 Getting Started

> [!NOTE]
> This project uses `uv` for easy setup. You do not need to manage virtual environments manually.

1.  **Clone the repo:**
    ```bash
    git clone git@github.com:josuebouchard/data-organization-fiuba-portfolio.git
    cd data-organization-fiuba-portfolio
    ```

2.  **Download the datasets:**
    ```bash
    uv run scripts/download_data.py
    ```

3.  **Run the notebooks:**
    ```bash
    # To just run the notebook
    uvx marimo run exercises/exercise_1.py

    # To edit the notebook
    uvx marimo edit exercises/exercise_1.py
    ```

---

## 🎓 Academic Context
The 75.06 curriculum at FIUBA is a high-intensity program focused on the **efficiency, storage, and processing of large-scale datasets**. Unlike a standard "Intro to Data Science" course, this program emphasizes the architectural and algorithmic challenges of data. 

Through this coursework, I learned about:
* **Distributed Computing:** Managing large-scale data processing using the **PySpark RDD** (Resilient Distributed Datasets) API and MapReduce paradigms.
* **Performance Engineering:** Optimizing data workflows for CPU and memory efficiency.
* **Statistical Modeling:** Building end-to-end Machine Learning pipelines, from raw data ingestion to model evaluation and feature engineering.