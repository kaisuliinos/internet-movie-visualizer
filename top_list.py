import pandas as pd
import numpy as np

from bokeh.models import ColumnDataSource, Grid, LinearAxis, Plot, Text
from bokeh.models import Div
from bokeh.plotting import figure

def top_list_data(titles: pd.DataFrame) -> pd.DataFrame:
    top_list: pd.DataFrame = titles[titles.numVotes > 1000].nlargest(10, 'averageRating', keep='first')
    top_list.drop(columns=['isAdult', 'endYear', 'runtimeMinutes', 'originalTitle', 'genres', 'titleType'], inplace=True)
    top_list.reset_index(inplace=True)
    top_list['x'] = 0
    top_list['y'] = top_list.index # TODO: fix this shit

    return top_list


def top_list(top_list: ColumnDataSource):
    plot = Plot(
        title=None, plot_width=300, plot_height=300,
        min_border=0, toolbar_location=None)

    glyph = Text(x="x", y="y", text="primaryTitle", text_color="#96deb3")
    plot.add_glyph(top_list, glyph)

    return plot
