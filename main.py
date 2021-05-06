import numpy as np
import pandas as pd

from read_data import read_names, read_principals, read_titles, read_ratings

def line():
  print('\n')

titles: pd.DataFrame = read_titles()
ratings: pd.DataFrame = read_ratings()
principals: pd.DataFrame = read_principals()
names: pd.DataFrame = read_names()

titles = titles.join(other=ratings, on='tconst', rsuffix='_ratings')

print('Titles and ratings')
print(titles.head(5))
line()

print('Principals')
print(principals.head(5))
line()

print('Names')
print(names.head(5))
line()