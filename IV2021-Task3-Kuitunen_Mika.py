import pandas as pd
import numpy as np

from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import brewer
from bokeh.plotting import figure, output_file, show

# Import data
titles: pd.DataFrame = pd.read_csv(
  'data/title.basics.test.tsv',
  sep='\t',
  dtype={
    'tconst': str,
    'titleType': pd.CategoricalDtype(categories=['short', 'movie', 'tvEpisode' 'tvMovie', 'tvSeries', 'tvMiniSeries', 'tvEpisode', 'video']),
    'primaryTitle': str,
    'originalTitle': str,
    'isAdult': str,
    'startYear': str,
    'endYear': str,
    'runtimeMinutes': str,
    'genres': str
  }
)

# Drop unnecessary data
titles.drop(columns=['tconst', 'isAdult', 'endYear', 'runtimeMinutes', 'originalTitle'], inplace=True)

# Filter out everything that is not short or a movie
#titles = titles[(titles['titleType'] == 'movie') | (titles['titleType'] == 'short')]
titles = titles[titles['titleType'] == 'movie']

# Replace \N values with pandas NA
titles.startYear.replace('\\N', pd.NA, inplace=True)
titles.genres.replace('\\N', pd.NA, inplace=True)

# Convert types
titles.startYear = pd.to_numeric(titles.startYear, downcast='integer')

# Split genres column and explode to multiple rows
titles.genres = titles.genres.str.cat(np.repeat('total', titles.shape[0]), sep=',', na_rep='') # Evil hackery to get total count into pivot table
titles.genres = titles.genres.str.lower().str.split(',')
titles = titles.explode('genres')
titles = titles[(titles.genres != 'short') & (titles.genres != '')] # Remove 'short' from genres (not useful) and empty strings (NA)
titles.reset_index(drop=True, inplace=True)

# Create a pivot table where the index is year of release and columns are number of films released that year for a given genre, plus total of films released that year
genres_by_year = pd.pivot_table(titles, index='startYear', columns=['genres'], values=['primaryTitle'], aggfunc=lambda x: len(x.unique()), fill_value=0)
genres_by_year.columns = genres_by_year.columns.droplevel() # Drop hierarchy level

# Divide film release numbers by the total films released to get percentage
columns_not_total = genres_by_year.columns.drop(['total'])
genres_by_year[columns_not_total] = (genres_by_year[columns_not_total].div(genres_by_year.total, axis=0)*100).round(2)

# Pick the 10 most popular genres overall (exclude 'total')
print(genres_by_year.drop(columns=['total']).sum().sort_values(ascending=False).head(10))
top_10_genres = genres_by_year.drop(columns=['total']).sum().sort_values(ascending=False).head(10).index.values

# Filter out columns of genres outside the top 10
genres_by_year = genres_by_year[genres_by_year.columns.intersection(top_10_genres)]

# Discard future releases
genres_by_year = genres_by_year[genres_by_year.index <= 2021]

### Set up for Bokeh

years = genres_by_year.index

year_min = np.min(years)
year_max = np.max(years)
print('From year {} to {}'.format(str(year_min.astype(int)), str(year_max.astype(int))))

films_max = genres_by_year.sum(axis=1).max() + 10.0

names = top_10_genres

source = ColumnDataSource(genres_by_year)

# Bokeh

output_file('Task3-Mika.html')

p = figure(
  title='Occurrence of genres in films by year of release, top 10 most frequent genres',
  x_range=(year_min, year_max),
  y_range=(0, films_max),
  plot_width=900,
  plot_height=600,
  x_axis_label='Year',
  y_axis_label='Percentage of films tagged (note: one film can have multiple genres)'
)
p.grid.minor_grid_line_color = '#eeeeee'

colors=brewer['Spectral'][len(names)]
p.varea_stack(stackers=names, x='startYear', color=colors, legend_label=names.tolist(), source=source)

# reverse the legend entries to match the stacked order
p.legend.items.reverse()
p.legend.location = 'top_left'

show(p)
