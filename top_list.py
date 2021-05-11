import pandas as pd
from bokeh.models import Div


def top_list(titles: pd.DataFrame):

    top_ten = titles[(titles.numVotes > 1000) & (titles.titleType == 'movie')].nlargest(10, 'averageRating', keep='first')

    list_items = []
    for index, row in top_ten.iterrows():
        list_items.append('<li>{} - {}</li>'.format(row['primaryTitle'], row['averageRating']))

    div = Div(text="""
        <ol type='1'>
            {}
        </ol>""".format(''.join(list_items))
    )

    return div
