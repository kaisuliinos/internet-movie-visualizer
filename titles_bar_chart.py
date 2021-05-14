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
  years = bar_source.data['years']
  year_min = np.min(years)
  year_max = np.max(years)

  p = figure(
    name='titles_bar_chart',
    title='Number of releases per year',
    x_range=(year_min+1, year_max+1),
    plot_width=1000,
    plot_height=600,
    x_axis_label='Year',
    tooltips=[("Year", "@startYear"), ("Total releases", "@primaryTitle")],
  )

  p.toolbar_location = None

  p.xgrid.visible = False

  p.vbar(x='years', top='primaryTitle', source=bar_source, width=0.7)
  p.y_range.start = 0

  return p
