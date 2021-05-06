import numpy as np
import pandas as pd

env = 'test' # 'test' or 'prod'

def line():
  print('\n')

def form_path(file):
  data_path = 'data/'
  extension = '.tsv'
  suffix = '.{}'.format(env)

  return '{}{}{}{}'.format(data_path, file, suffix, extension)

def read_csv(file, file_spec, index_col=None):
  res: pd.DataFrame = pd.read_csv(
    file,
    sep='\t',
    dtype=file_spec,
    index_col=index_col,
    na_values='\\N',
  )
  return res

titles_file = 'title.basics'
principals_file = 'title.principals'
names_file = 'name.basics'
ratings_file = 'title.ratings'

titles_input = form_path(titles_file)
principals_input = form_path(principals_file)
names_input = form_path(names_file)
ratings_input = form_path(ratings_file)

# -------------------------------------------------------------------------------------------------
# Titles

def read_titles():
  titles: pd.DataFrame = read_csv(
    titles_input,
    {
      'tconst': str,
      'titleType': str,
      'primaryTitle': str,
      'originalTitle': str,
      'isAdult': str,
      'startYear': str,
      'endYear': str,
      'runtimeMinutes': str,
      'genres': str
    },
    'tconst'
  )
  return titles

# -------------------------------------------------------------------------------------------------
# Ratings

def read_ratings():
  ratings: pd.DataFrame = read_csv(
    ratings_input,
    {
      'tconst': str,
      'averageRating': str,
      'numVotes': str
    },
    'tconst'
  )
  return ratings

# -------------------------------------------------------------------------------------------------
# Principals

def read_principals():
  principals: pd.DataFrame = read_csv(
    principals_input,
    {
      'tconst': str,
      'ordering': int,
      'nconst': str,
      'category': str,
      'job': str,
      'characters': str
    },
    'tconst'
  )
  return principals

# -------------------------------------------------------------------------------------------------
# Names

def read_names():
  names: pd.DataFrame = read_csv(
    names_input,
    {
      'nconst': str,
      'primaryName': str,
      'birthYear': str,
      'deathYear': str,
      'primaryProfession': str,
      'knownForTitles': str
    },
    'nconst'
  )
  return names
