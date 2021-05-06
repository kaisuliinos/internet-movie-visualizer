import pandas as pd
import numpy as np
import circlify

from bokeh.models import ColumnDataSource, HoverTool, LabelSet
from bokeh.palettes import brewer
from bokeh.plotting import figure, output_file, show

# Import data
titles: pd.DataFrame = pd.read_csv(
  'data/title.basics.test.tsv',
  sep='\t',
  dtype={
    'tconst': str,
    'titleType': pd.CategoricalDtype(categories=['short', 'movie', 'tvShort', 'tvMovie', 'tvSeries', 'tvEpisode', 'tvMiniSeries', 'tvSpecial', 'video', 'videoGame']),
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
# titles.genres = titles.genres.str.cat(np.repeat('total', titles.shape[0]), sep=',', na_rep='') # Evil hackery to get total count into pivot table
titles.genres = titles.genres.str.lower().str.split(',')
titles = titles.explode('genres')
titles = titles[(titles.genres != 'short') & (titles.genres != '')] # Remove 'short' from genres (not useful) and empty strings (NA)
titles.reset_index(drop=True, inplace=True)
# Here ends Mika's previous code ----


counts_by_genre = pd.pivot_table(titles, index=['genres'], values=['primaryTitle'], aggfunc=lambda x: len(x.unique()), fill_value=0)

# Convert the index to column and rename primaryTitle to datum so that to_dict returns the data in a format circlify understands
counts_by_genre.reset_index(inplace=True)
counts_by_genre = counts_by_genre.rename(columns={'primaryTitle': 'datum'})

# Create circles to plot
data = counts_by_genre.to_dict(orient='records')
circles = circlify.circlify(data, show_enclosure=False)

# Change circle objects to dicts for pandas
circle_dicts = []
circle_plot_width = 800
for c in circles:
  circle_dicts.append({'x': c.x, 'y': c.y, 'r': c.r * circle_plot_width*0.9, 'genre': c.ex['genres']})

# Plot the circles
circles_df = pd.DataFrame(data=circle_dicts)
circles_df.set_index(['genre'], inplace=True)
circles_source = ColumnDataSource(circles_df)
p = figure(x_range=[-1, 1], y_range=[-1, 1], plot_width=circle_plot_width, plot_height=circle_plot_width)
p.scatter(x='x', y='y', size='r', source=circles_source)

# To show the labels for each bubble
labels = LabelSet(x='x', y='y', text='genre', source=circles_source)
p.add_layout(labels)

show(p)
