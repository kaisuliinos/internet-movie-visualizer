import numpy as np
import pandas as pd

from bokeh.plotting import show
from bokeh.layouts import layout

from read_data import read_names, read_principals, read_titles, read_ratings
from genre_bubble_chart import genre_bubble_chart
from top_list import top_list

def line():
  print('\n')

titles: pd.DataFrame = read_titles()
ratings: pd.DataFrame = read_ratings()
principals: pd.DataFrame = read_principals()
names: pd.DataFrame = read_names()

titles = titles.join(other=ratings, on='tconst', rsuffix='_ratings')

p = genre_bubble_chart(titles.copy()) # Pass a copy instead of reference
tl = top_list(titles.copy())

lo = layout([
  [p, tl]
])
show(lo)