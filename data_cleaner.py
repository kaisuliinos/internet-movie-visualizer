import pandas as pd

env = 'prod' # 'test' or 'prod'

def line():
  print('\n')

def formPaths(file):
  data_path = 'data/'
  extension = '.tsv'
  suffix = '.{}'.format(env)

  input = '{}{}{}'.format(data_path, file, extension)
  output = '{}{}{}{}'.format(data_path, file, suffix, extension)
  return (input, output)

titles_file = 'title.basics'
principals_file = 'title.principals'
names_file = 'name.basics'
ratings_file = 'title.ratings'

titles_input, titles_output = formPaths(titles_file)
principals_input, principals_output = formPaths(principals_file)
names_input, names_output = formPaths(names_file)
ratings_input, ratings_output = formPaths(ratings_file)

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

categories = ['movie', 'tvMovie', 'tvSeries', 'tvMiniSeries']
titles = titles[titles['titleType'].isin(categories)]

if (env == 'test'):
  titles = titles.sample(n=10000, random_state=0)

titles.reset_index(drop=True, inplace=True)

print(titles.head(5))
line()

titles.to_csv(titles_output, sep='\t', na_rep='\\N', index=False, line_terminator='\n')

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

job_titles = ['self', 'director', 'cinematographer', 'composer', 'producer', 'actor', 'actress', 'writer']

principals = principals[principals['category'].isin(job_titles)]
principals = principals[principals['tconst'].isin(title_ids)]

principals.reset_index(drop=True, inplace=True)

print(principals.head(5))
line()

principals.to_csv(principals_output, sep='\t', na_rep='\\N', index=False, line_terminator='\n')

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

names = names[names['nconst'].isin(name_ids)]

names.reset_index(drop=True, inplace=True)

print('NAMES')
print(names.head(5))
line()

names.to_csv(names_output, sep='\t', na_rep='\\N', index=False, line_terminator='\n')

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

ratings = ratings[ratings['tconst'].isin(title_ids)]

ratings.reset_index(drop=True, inplace=True)

print('RATINGS')
print(ratings.head(5))
line()

ratings.to_csv(ratings_output, sep='\t', na_rep='\\N', index=False, line_terminator='\n')