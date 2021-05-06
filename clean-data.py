import pandas as pd

def line():
  print('\n')

def formPaths(file):
  data_path = 'data/'
  extension = '.tsv'
  test_suffix = '.prod'

  input = '{}{}{}'.format(data_path, file, extension)
  output = '{}{}{}{}'.format(data_path, file, test_suffix, extension)
  return (input, output)

titles_file = 'title.basics'
principals_file = 'title.principals'
names_file = 'name.basics'

titles_input, titles_output = formPaths(titles_file)
principals_input, principals_output = formPaths(principals_file)
names_input, names_output = formPaths(names_file)

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

categories = ['movie', 'tvMovie', 'tvSeries', 'tvMiniSeries']
titles = titles[titles['titleType'].isin(categories)]

titles.reset_index(drop=True, inplace=True)

print(titles.head(5))
line()

titles.to_csv(titles_output, sep='\t', na_rep='\\N', index=False)

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

principals.to_csv(principals_output, sep='\t', na_rep='\\N', index=False)

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

names.to_csv(names_output, sep='\t', na_rep='\\N', index=False)
