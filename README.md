# HealthSenti

HealthSenti is an easy to use interactive application that is designed to visually compare the public sentiment of a certain health topic and the incidence of that health topic based on official datasets, thus allowing for a clearer understanding of the state of health in the respective country or location. This application is primarily intended for use in developing countries, where there is a lack of health data due to various obstacles, who can use this new dataset based on public sentiment to either supplement their health dataset or serve to see how representative the official health datasets are of the public's opinion.

## Installation

You can clone the repository by running the following command:

```bash
git clone git@github.com/kahesayn/healthSenti.git
```

`cd` into the project root folder:

```bash
cd healthSenti
```

This program uses [Pipenv](https://github.com/pypa/pipenv) for dependency management.

- If needed, install and upgrade the `pipenv` with `pip`:

  ```bash
  pip install pipenv -U
  ```

- To create a default virtual environment and use the program:

  ```bash
  pipenv install
  ```

HealthSenti relies on `en_core_web_sm` English models for one of the sentiment analyzers
trained on written web text (blogs, news, comments) that includes vocabulary,
vectors, syntax and entities.

To install the pre-trained model, you can run the following command:

```bash
pipenv run python -m spacy download en_core_web_sm
```

## Web Interface

HealthSenti is mainly developed on its web interface with [Streamlit](https://www.streamlit.io)
in order to provide fast text analysis and visualizations.

In order to run the `Streamlit` interface, type and execute the following command
in your terminal:

```bash
pipenv run streamlit run healthSenti.py
```
