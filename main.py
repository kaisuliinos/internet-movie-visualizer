from bokeh.core.property.container import ColumnData
from bokeh.models import ColumnDataSource
from bokeh.models.layouts import Column
import numpy as np
import pandas as pd

from bokeh.plotting import show
from bokeh.layouts import layout, column, row
from bokeh.models import RangeSlider, AutocompleteInput, RadioButtonGroup
from bokeh.io import curdoc
from bokeh.themes import Theme

from read_data import read_names, read_principals, read_titles, read_ratings
from titles_bar_chart import titles_bar_chart, titles_bar_chart_data
from genre_bubble_chart import genre_bubble_chart_data, genre_bubble_chart
from top_list import top_list, top_list_data

from utils import create_name_strings

# -----------------------------------------------------------------------------

titles: pd.DataFrame = read_titles()
ratings: pd.DataFrame = read_ratings()
principals: pd.DataFrame = read_principals()
names: pd.DataFrame = read_names()

autocomplete_names = names[['primaryName', 'primaryProfession']].apply(create_name_strings, axis=1).to_list()

titles = titles.join(other=ratings, on='tconst', rsuffix='_ratings')

# -----------------------------------------------------------------------------

genres_df: pd.DataFrame = genre_bubble_chart_data(titles.copy())
genres_source = ColumnDataSource(genres_df)

toplist_df = top_list_data(titles.copy())
toplist_source = ColumnDataSource(toplist_df)

title_count_df: pd.DataFrame = titles_bar_chart_data(titles.copy())
title_count_source = ColumnDataSource(title_count_df)

# -----------------------------------------------------------------------------

year_slider = RangeSlider(
  name='filter_year',
  start=1910,
  end=2021,
  step=1,
  value=(1910, 2021)
)

def update_year(attr, old, new):
  start, end = new
  global genres_source, toplist_source

  new_titles = titles[(titles.startYear >= start) & (titles.startYear <= end)]

  genres_new_df = genre_bubble_chart_data(new_titles.copy())
  genres_source.data = genres_new_df

  toplist_new_df = top_list_data(new_titles.copy())
  toplist_source.data = toplist_new_df

year_slider.on_change('value', update_year)

# -----------------------------------------------------------------------------

search_bar = AutocompleteInput(
  name='filter_name',
  value='',
  case_sensitive=False,
  completions=autocomplete_names,
  css_classes=['autocomplete']
)

def update_name(attr, old, new):
  print(new)

search_bar.on_change('value', update_name)

# -----------------------------------------------------------------------------

tab_labels = ['Movies', 'Tv-series']
tabs = RadioButtonGroup(
  name='filter_tab',
  labels=tab_labels,
  active=0
)

# -----------------------------------------------------------------------------

genre_bubble_chart = genre_bubble_chart(genres_source)
toplist = top_list(toplist_source)
bar_chart = titles_bar_chart(title_count_source)

curdoc().theme = Theme(filename="static/theme.json")

curdoc().add_root(genre_bubble_chart)
curdoc().add_root(toplist)
curdoc().add_root(bar_chart)

curdoc().add_root(year_slider)
curdoc().add_root(search_bar)
curdoc().add_root(tabs)