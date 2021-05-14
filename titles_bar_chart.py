import pandas as pd
import numpy as np

from bokeh.models import ColumnDataSource
from bokeh.plotting import figure

def titles_bar_chart(titles: pd.DataFrame):
    # Drop unnecessary data
    titles.drop(columns=['isAdult', 'endYear', 'runtimeMinutes', 'originalTitle'], inplace=True)

    titles = titles[(titles.genres != 'short') & (
                titles.genres != '')]  # Remove 'short' from genres (not useful) and empty strings (NA)
    titles.reset_index(drop=True, inplace=True)

    # Replace \N values with pandas NA
    titles.startYear.replace('\\N', pd.NA, inplace=True)
    titles.genres.replace('\\N', pd.NA, inplace=True)

    # Convert types
    titles.startYear = pd.to_numeric(titles.startYear, downcast='integer')

    titles_by_year = pd.pivot_table(titles, index=['startYear'], values=['primaryTitle'],
                                    aggfunc=lambda x: len(x.unique()), fill_value=0)
    # Discard future releases
    titles_by_year = titles_by_year[titles_by_year.index <= 2021]

    bar_source = ColumnDataSource(titles_by_year)

    years = titles_by_year.index
    year_min = np.min(years)
    year_max = np.max(years)

    p = figure(title='Number of releases per year',
               x_range=(year_min+1, year_max+1),
               plot_width=1000,
               plot_height=600,
               x_axis_label='Year',
               tooltips=[("Year", "@startYear"), ("Total releases", "@primaryTitle")])

    p.vbar(x='startYear', top='primaryTitle', source=bar_source, width=0.7)
    p.y_range.start = 0

    return p
