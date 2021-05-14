import pandas as pd
import numpy as np

from bokeh.models import ColumnDataSource, Grid, LinearAxis, Plot, Text
from bokeh.models import Div
from bokeh.plotting import figure

def format_text(data):
  order = data[0]
  title = data[1]
  start = data[2]
  end = data[3]
  rating = data[4]
  print(end)
  if pd.isna(end):
    return '{}: {} ({}): {}'.format(order, title, start, rating)
  else:
    return '{}: {} ({}-{}): {}'.format(order, title, start, end, rating)

def top_list_data(titles: pd.DataFrame) -> pd.DataFrame:
  top_list: pd.DataFrame = titles[titles.numVotes > 1000].nlargest(10, 'averageRating', keep='first')
  top_list.reset_index(inplace=True)
  top_list['order'] = top_list.index
  top_list['text'] = top_list[['order', 'primaryTitle','startYear', 'endYear', 'averageRating']].apply(format_text, axis=1)
  top_list.drop(columns=['isAdult', 'endYear', 'runtimeMinutes', 'originalTitle', 'genres', 'titleType'], inplace=True)
  top_list['x'] = 0
  top_list['y'] = top_list.index[::-1] # Reverse index

  print(top_list.head(10))

  return top_list


def top_list(top_list: ColumnDataSource):
  p = figure(
    title='Top 10 best rated films',
    plot_width=600,
    plot_height=400,
    x_range=[0, 1000],
    y_range=[0, 9],
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
