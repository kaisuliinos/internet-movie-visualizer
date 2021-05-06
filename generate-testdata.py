import pandas as pd

# Import data
titles: pd.DataFrame = pd.read_csv(
  'title.basics.tsv',
  sep='\t',
  dtype={
    'tconst': str,
    'titleType': str,
    'primaryTitle': str,
    'originalTitle': str,
    'isAdult': str,
    'startYear': str,
    'endYear': str,
    'runtimeMinutes': str,
    'genres': str
  }
)

titles = titles.sample(10000)
titles.reset_index(drop=True, inplace=True)

titles.to_csv('title.basics.test.tsv', sep='\t', na_rep='\\N', index=False)