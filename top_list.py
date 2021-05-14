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
  top_list: pd.DataFrame = titles[titles.numVotes > 1000].nlargest(10, 'averageRating', keep='first')
  top_list.reset_index(inplace=True)
  top_list['order'] = top_list.index + 1
  top_list['text'] = top_list.apply(format_text, axis=1)
  top_list['x'] = 0
  top_list['y'] = top_list.index[::-1] # Reverse index

  return top_list[['order', 'x', 'y', 'text']]


def top_list(top_list: ColumnDataSource):
  p = figure(
    name='top_list',
    title='Top 10 best rated films',
    plot_width=600,
    plot_height=400,
    x_range=[0, 1000],
    y_range=[0, 10],
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
    text_font={'value': 'Courier New'}
  )
  p.add_glyph(top_list, glyph)

  return p
