import numpy as np
import pandas as pd

from bokeh.plotting import show
from bokeh.layouts import layout, column, row
from bokeh.models import RangeSlider, TextInput, RadioButtonGroup

from read_data import read_names, read_principals, read_titles, read_ratings
from genre_bubble_chart import genre_bubble_chart
from top_list import top_list
from titles_bar_chart import titles_bar_chart

def line():
  print('\n')

titles: pd.DataFrame = read_titles()
ratings: pd.DataFrame = read_ratings()
principals: pd.DataFrame = read_principals()
names: pd.DataFrame = read_names()

titles = titles.join(other=ratings, on='tconst', rsuffix='_ratings')

bubble_chart = genre_bubble_chart(titles.copy()) # Pass a copy instead of reference
toplist = top_list(titles.copy())
bar_chart = titles_bar_chart(titles.copy())

year_slider = RangeSlider(
  title='Select the release year range',
  start=1910,
  end=2021,
  step=1,
  value=(1910, 2021)
)

search_bar = TextInput(value='', title="Search by director or author's name:")

tab_labels = ['Movies', 'Tv-series']
tabs = RadioButtonGroup(labels=tab_labels, active=0)

r = row(tabs, year_slider, search_bar)
c = column(r, toplist, bar_chart)

lo = layout([
  [c, bubble_chart]
])

show(lo)
