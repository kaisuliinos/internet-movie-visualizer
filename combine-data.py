import numpy as np
import pandas as pd

env = 'test' # 'test' or 'prod'

def line():
  print('\n')

def formPath(file):
  data_path = 'data/'
  extension = '.tsv'
  suffix = '.{}'.format(env)

  return '{}{}{}{}'.format(data_path, file, suffix, extension)

titles_file = 'title.basics'
principals_file = 'title.principals'
names_file = 'name.basics'
ratings_file = 'title.ratings'

titles_input = formPath(titles_file)
principals_input = formPath(principals_file)
names_input = formPath(names_file)
ratings_input = formPath(ratings_file)

# -------------------------------------------------------------------------------------------------
# Titles

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

print('TITLES')
print('Title types:')
print(titles.titleType.unique())
line()

print(titles.head(5))
line()

# -------------------------------------------------------------------------------------------------
# Principals

title_ids = titles['tconst']

principals: pd.DataFrame = pd.read_csv(
  principals_input,
  sep='\t',
  dtype={
    'tconst': str,
    'ordering': int,
    'nconst': str,
    'category': str,
    'job': str,
    'characters': str
  }
)

print('PRINCIPALS')
print('Principal categories:')
print(principals.category.unique())
line()

print(principals.head(5))
line()

# -------------------------------------------------------------------------------------------------
# Names

name_ids = principals['nconst']

names: pd.DataFrame = pd.read_csv(
  names_input,
  sep='\t',
  dtype={
    'nconst': str,
    'primaryName': str,
    'birthYear': str,
    'deathYear': str,
    'primaryProfession': str,
    'knownForTitles': str
  }
)

names.reset_index(drop=True, inplace=True)

print('NAMES')
print(names.head(5))
line()

# -------------------------------------------------------------------------------------------------
# Ratings

ratings: pd.DataFrame = pd.read_csv(
  ratings_input,
  sep='\t',
  dtype={
    'tconst': str,
    'averageRating': str,
    'numVotes': str
  }
)

ratings.reset_index(drop=True, inplace=True)

print('RATINGS')
print(ratings.head(5))
line()
