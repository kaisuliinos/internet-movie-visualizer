from bokeh.core.property.container import ColumnData
from bokeh.models.layouts import Column
import pandas as pd
import numpy as np
import circlify

from bokeh.models import ColumnDataSource, LabelSet
from bokeh.plotting import figure

from utils import string_to_rgb

circle_plot_width = 650

def genre_bubble_chart_data(titles: pd.DataFrame) -> pd.DataFrame:
  titles.dropna(subset=['genres'], inplace=True)
  if titles.empty: return pd.DataFrame()

  # Split genres column and explode to multiple rows
  titles.genres = titles.genres.str.lower().str.split(',')

  titles = titles.explode('genres')
  titles = titles[(titles.genres != 'short') & (titles.genres != '')] # Remove 'short' from genres (not useful) and empty strings (NA)
  titles.reset_index(drop=True, inplace=True)

  counts_by_genre = pd.pivot_table(
    titles, index=['genres'],
    values=['primaryTitle'],
    aggfunc=lambda x: len(x.unique()),
    fill_value=0
  )

  # Convert the index to column and rename primaryTitle to datum so that to_dict returns the data in a format circlify understands
  counts_by_genre.reset_index(inplace=True)
  counts_by_genre = counts_by_genre.rename(columns={'primaryTitle': 'datum'})

  # Create circles to plot
  data = counts_by_genre.to_dict(orient='records')
  circles = circlify.circlify(data, show_enclosure=False)

  # Change circle objects to dicts for pandas
  circle_dicts = []
  for _, c in enumerate(circles):
    circle_dicts.append({
      'x': c.x,
      'y': c.y,
      'r': c.r * circle_plot_width*0.9,
      'genre': c.ex['genres'],
      'color': string_to_rgb(c.ex['genres'])
    })

  # Plot the circles
  circles_df = pd.DataFrame(data=circle_dicts)
  circles_df.set_index(['genre'], inplace=True)

  return circles_df


def genre_bubble_chart(circles_source: ColumnDataSource):
  p = figure(
    name='genre_bubble_chart',
    x_range=[-1, 1],
    y_range=[-1, 1],
    plot_width=circle_plot_width,
    plot_height=circle_plot_width,
    tools='tap'
  )

  p.toolbar_location = None

  p.scatter(x='x', y='y', size='r', fill_color='color', line_color='color', source=circles_source)

  # To show the labels for each bubble
  labels = LabelSet(
    x='x',
    y='y',
    text='genre',
    source=circles_source,
    text_align='center',
    text_baseline='middle',
  )
  p.add_layout(labels)

  p.xgrid.visible = False
  p.ygrid.visible = False

  p.xaxis.visible = False
  p.yaxis.visible = False

  return p
