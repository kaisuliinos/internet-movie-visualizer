import pandas as pd

import pandas as pd

def line():
  print('\n')

def formPaths(file):
  data_path = 'data/'
  extension = '.tsv'
  test_suffix = '.test'

  input = '{}{}{}'.format(data_path, file, extension)
  output = '{}{}{}{}'.format(data_path, file, test_suffix, extension)
  return (input, output)

titles_file = 'title.basics'
crew_file = 'title.crew'

titles_input, titles_output = formPaths(titles_file)
crew_input, crew_output = formPaths(crew_file)

# Import titles
titles: pd.DataFrame = pd.read_csv(
  titles_input,
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

print(titles.titleType.unique())

categories = ['short', 'movie', 'tvShort', 'tvMovie', 'tvSeries', 'tvMiniSeries']
titles = titles[titles['titleType'].isin(categories)]

titles = titles.sample(10000)
titles.reset_index(drop=True, inplace=True)

titles.to_csv(titles_output, sep='\t', na_rep='\\N', index=False)

title_ids = titles['tconst']

# Crew
crew: pd.DataFrame = pd.read_csv(
  crew_input,
  sep='\t',
  dtype={
    'tconst': str,
    'directors': str,
    'writers': str
  }
)

crew = crew[crew['tconst'].isin(title_ids)]
crew.reset_index(drop=True, inplace=True)

print(crew.head(5))
line()

crew.to_csv(crew_output, sep='\t', na_rep='\\N', index=False)