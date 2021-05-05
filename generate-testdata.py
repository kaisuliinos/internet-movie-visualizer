import pandas as pd
import numpy as np

# Import data
titles: pd.DataFrame = pd.read_csv(
  'title.basics.tsv',
  sep='\t',
  dtype={
    'tconst': str,
    'titleType': pd.CategoricalDtype(categories=['short', 'movie', 'tvEpisode' 'tvMovie', 'tvSeries', 'video']),
    'primaryTitle': str,
    'originalTitle': str,
    'isAdult': str,
    'startYear': str,
    'endYear': str,
    'runtimeMinutes': str,
    'genres': str
  }
)

titles = titles.sample(1000)

titles.to_csv('name.basics.test.tsv', sep='\t', na_rep='NA')