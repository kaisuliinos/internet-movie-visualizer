import numpy as np
import pandas as pd

from bokeh.plotting import show
from bokeh.layouts import layout, column
from bokeh.models import RangeSlider

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

bubble_chart = genre_bubble_chart(titles.copy()) # Pass a copy instead of reference
toplist = top_list(titles.copy())

year_slider = RangeSlider(
  title="Select the release year range",
  start=1910,
  end=2021,
  step=1,
  value=(1910, 2021)
)

c = column(year_slider, toplist)
lo = layout([
  [bubble_chart, c]
])

show(lo)
