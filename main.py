from bokeh.core.property.container import ColumnData
from bokeh.models import ColumnDataSource
from bokeh.models.layouts import Column
import numpy as np
import pandas as pd

from bokeh.plotting import show
from bokeh.layouts import layout, column, row
from bokeh.models import RangeSlider, AutocompleteInput, RadioButtonGroup, Button, TapTool
from bokeh.io import curdoc
from bokeh.themes import Theme
from bokeh.events import Tap

from read_data import read_names, read_principals, read_titles, read_ratings
from titles_bar_chart import titles_bar_chart, titles_bar_chart_data
from genre_bubble_chart import genre_bubble_chart_data, genre_bubble_chart
from top_list import top_list, top_list_data

from utils import create_name_strings

# -----------------------------------------------------------------------------

titles_raw: pd.DataFrame = read_titles()
ratings_raw: pd.DataFrame = read_ratings()
principals_raw: pd.DataFrame = read_principals()
names_raw: pd.DataFrame = read_names()

autocomplete_names = names_raw[['primaryName', 'primaryProfession']].apply(create_name_strings, axis=1).to_list()

titles_raw = titles_raw.join(other=ratings_raw, on='tconst', rsuffix='_ratings')

titles = titles_raw.copy()

# -----------------------------------------------------------------------------
# GLOBALS

year_min = 1910
year_max = 2021

# 0 - Movies
# 1 - Tv-Series
tab = 0

start = year_min
end = year_max

name = ''

genres = []

# -----------------------------------------------------------------------------

genres_source = ColumnDataSource()
toplist_source = ColumnDataSource()
title_count_source = ColumnDataSource()

def update_data():
  global tab, start, end, name, genre, titles, genres_source, toplist_source, title_count_source

  if tab == 0:
    titles = titles_raw[titles_raw.titleType.isin(['movie', 'tvMovie'])]
  else:
    titles = titles_raw[titles_raw.titleType.isin(['tvSeries', 'tvMiniSeries'])]
  
  titles = titles[
    ((titles.startYear >= start) & (titles.startYear <= end)) |
    (titles.endYear.notna() & (
      ((titles.endYear >= start) & (titles.endYear <= end)) |
      ((titles.startYear < start) & (titles.endYear > end))
    ))
  ]

  if (name != ''):
    try:
      row = names_raw[names_raw.primaryName == name].iloc[0] # Throws IndexError if empty dataframe
      nconst = row.name
      principals = principals_raw[principals_raw.nconst == nconst]['tconst'].to_list()
      titles = titles[titles.index.isin(principals)]
    except IndexError:
      pass

  toplist_df = top_list_data(titles.copy())
  toplist_source.data = toplist_df

  title_count_df: pd.DataFrame = titles_bar_chart_data(titles.copy())
  title_count_source.data = title_count_df

  genres_df: pd.DataFrame = genre_bubble_chart_data(titles.copy())
  genres_source.data = genres_df

def update_genres():
  global genres

  toplist_df = pd.DataFrame()
  title_count_df = pd.DataFrame()

  if not genres:
    toplist_df = top_list_data(titles.copy())
    title_count_df = titles_bar_chart_data(titles.copy())
  else:
    new_titles = titles.copy()
    new_titles = new_titles[new_titles.genres.str.lower().str.contains('|'.join(genres), regex=True, na=False)]

    toplist_df = top_list_data(new_titles)
    title_count_df = titles_bar_chart_data(new_titles)

  toplist_source.data = toplist_df
  title_count_source.data = title_count_df


# Initial run on new session
update_data()

# -----------------------------------------------------------------------------

tab_labels = ['Movies', 'Tv-series']
tabs = RadioButtonGroup(
  name='filter_tab',
  labels=tab_labels,
  active=tab
)

def update_tab(attr, old, new):
  global tab

  if (new != old):
    tab = new
    update_data()

tabs.on_change('active', update_tab)

# -----------------------------------------------------------------------------

year_slider = RangeSlider(
  name='filter_year',
  start=year_min,
  end=year_max,
  step=1,
  value=(year_min, year_max),
  title='Selected years'
)

def update_year(attr, old, new):
  global start, end

  if (new != old):
    start, end = new
    update_data()

year_slider.on_change('value_throttled', update_year)

# -----------------------------------------------------------------------------

search_bar = AutocompleteInput(
  name='filter_name',
  value='',
  case_sensitive=False,
  completions=autocomplete_names,
  css_classes=['autocomplete'],
  placeholder='Search for director, author, actor'
)

def update_name(attr, old, new):
  global name

  if (new != old):
    name = new.split(' (')[0]
    update_data()

search_bar.on_change('value', update_name)

search_bar_button = Button(
  name='filter_name_button',
  label='Clear',
  width=80
)

def clear_name():
  global name
  
  if (name != ''):
    name = ''
    search_bar.value = ''
    update_data()

search_bar_button.on_click(clear_name)

# -----------------------------------------------------------------------------

def select_genre(attr, old, new):
  global genres

  genre_indices = new

  if not genre_indices:
    genres = []
  else:
    all_genres = genres_source.data['genre']
    genres = [all_genres[i] for i in genre_indices]
  
  update_genres()

genres_source.selected.on_change('indices', select_genre)

# -----------------------------------------------------------------------------

toplist = top_list(toplist_source)
bar_chart = titles_bar_chart(title_count_source)
genre_bubble_chart = genre_bubble_chart(genres_source)

curdoc().theme = Theme(filename="static/theme.json")

curdoc().add_root(genre_bubble_chart)
curdoc().add_root(toplist)
curdoc().add_root(bar_chart)

curdoc().add_root(tabs)
curdoc().add_root(year_slider)
curdoc().add_root(search_bar)
curdoc().add_root(search_bar_button)
