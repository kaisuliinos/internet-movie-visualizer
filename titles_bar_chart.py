import pandas as pd
import numpy as np

from bokeh.models import ColumnDataSource
from bokeh.plotting import figure

def create_years(row):
  if pd.isna(row.endYear):
    return row.startYear
  else:
    return list(range(row.startYear, row.endYear + 1))


def titles_bar_chart_data(titles: pd.DataFrame) -> pd.DataFrame:
  titles.dropna(subset=['startYear'], inplace=True)
  if titles.empty: return pd.DataFrame()

  titles['years'] = titles.apply(create_years, axis=1)
  titles = titles.explode('years')
  titles.reset_index(drop=True, inplace=True)

  titles_by_year = pd.pivot_table(
    titles, index=['years'],
    values=['primaryTitle'],
    aggfunc=lambda x: len(x.unique()), fill_value=0
  )

  # Discard future releases
  titles_by_year = titles_by_year[titles_by_year.index <= 2021]

  return titles_by_year

def titles_bar_chart(bar_source: ColumnDataSource):
  p = figure(
    name='titles_bar_chart',
    plot_width=600,
    plot_height=300,
    x_axis_label='Year',
    tooltips=[("Year", "@years"), ("Total releases", "@primaryTitle")],
    outline_line_alpha=0.5
  )

  p.toolbar_location = None

  p.xgrid.visible = False

  p.vbar(x='years', top='primaryTitle', source=bar_source, width=0.7)
  p.y_range.start = 0

  return p
