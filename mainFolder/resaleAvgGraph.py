import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
from mainFolder import dash_resaleAvgGraph_graph, app
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px

hdb = pd.read_csv('mainFolder/final_df.csv',low_memory=False)
df7 = hdb[['region', 'town', 'listing_year', 'resale_price']]
available_filter = ['region', 'town']

#show how hdb prices changes over time in different towns/regions
dash_resaleAvgGraph_graph.layout = html.Div([

    html.Div([
            dcc.Dropdown(
                id='selection-ddl',
                options=[{'label': i, 'value': i} for i in available_filter],
                value='region'
            )
        ]),
    dcc.Graph(
            id='line-graph'
    )
])

@dash_resaleAvgGraph_graph.callback(
    Output('line-graph', 'figure'),
    [Input('selection-ddl', 'value')])

def AverageResalePriceWithTime(factor):
    df = df7.groupby([factor,'listing_year'],as_index=True).mean()[['resale_price']]
    df.reset_index(inplace=True)
    fig = px.line(df, x="listing_year", y="resale_price", color=factor)
    fig.update_layout(
         title={
        'text': "Average Resale Price With Time",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}
    )
    return fig