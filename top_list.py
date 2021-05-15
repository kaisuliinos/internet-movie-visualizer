import pandas as pd
import numpy as np

from bokeh.models import ColumnDataSource, Grid, LinearAxis, Plot, Text
from bokeh.models import Div
from bokeh.plotting import figure

def format_text(row):
  order = row.order
  title = row.primaryTitle
  start = row.startYear
  end = row.endYear
  rating = row.averageRating

  if pd.isna(end):
    return '{}: {} ({}): {}'.format(order, title, start, rating)
  else:
    return '{}: {} ({}-{}): {}'.format(order, title, start, end, rating)

def top_list_data(titles: pd.DataFrame) -> pd.DataFrame:
  titles.dropna(subset=['primaryTitle', 'startYear', 'averageRating'], inplace=True)
  if titles.empty: return pd.DataFrame()

  top_list: pd.DataFrame = titles[titles.numVotes > 1000].nlargest(10, 'averageRating', keep='first')

  # In case other filters have resulted in empty top list, remove vote restriction
  if top_list.empty:
    top_list = titles.nlargest(10, 'averageRating', keep='first')

  top_list.reset_index(inplace=True)

  top_list['order'] = top_list.index + 1
  top_list['text'] = top_list.apply(format_text, axis=1)
  top_list['x'] = 0
  top_list['y'] = -top_list.index # Reverse index

  return top_list[['order', 'x', 'y', 'text']]


def top_list(top_list: ColumnDataSource):
  p = figure(
    name='top_list',
    plot_width=600,
    plot_height=300,
    x_range=[0, 1000],
    y_range=[-10, 1],
    min_border=0,
    toolbar_location=None
  )

  p.xgrid.visible = False
  p.ygrid.visible = False

  p.xaxis.visible = False
  p.yaxis.visible = False

  glyph = Text(
    x='x',
    y='y',
    text='text',
  )
  p.add_glyph(top_list, glyph)

  return p
