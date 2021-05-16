# Internet Movie Visualizer

Movie data visualizer based on the IMDb dataset.

## Requirements

- Python 3.9 and the packages listed in the Pipfile (we recommend pipenv for installation)
- For production data, datasets downloaded from https://www.imdb.com/interfaces/ into the `data` folder:
  - title.basics.tsv
  - title.principals.tsv
  - title.ratings.tsv
  - name.basics.tsv
  - Run these through `data-cleaner.py` and set the env in the script file to `prod`
  - When running the main script, change the env in `read-data.py` to `prod`

## Running locally

```
bokeh serve .
```
