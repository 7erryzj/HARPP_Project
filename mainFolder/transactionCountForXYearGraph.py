import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
from mainFolder import dash_transactionCountForXYear_graph, app
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px

df3 = pd.read_csv('./mainFolder/final_df.csv')
df3 = df3.groupby(['listing_year', 'flat_type'],as_index=True).count()[['resale_price']]
df3.reset_index(inplace=True)
df3 = df3.rename(columns={'resale_price': 'transaction_count'})

available_year = df3['listing_year'].unique()

indexNames = df3[ (df3['flat_type'] == 'EXECUTIVE') | (df3['flat_type'] == '2 ROOM') | (df3['flat_type'] == '1 ROOM') 
                | (df3['flat_type'] == 'MULTI GENERATION')  | (df3['flat_type'] == 'MULTI-GENERATION') ].index
df3.drop(indexNames , inplace=True)

dash_transactionCountForXYear_graph.layout = html.Div([

    html.Div([
            dcc.Dropdown(
                id='year-ddl',
                options=[{'label': i, 'value': i} for i in available_year],
                value=1990
            )
        ]),
    dcc.Graph(
            id='bar-graph'
    )
])

@dash_transactionCountForXYear_graph.callback(
    Output('bar-graph', 'figure'),
    [Input('year-ddl', 'value')])

def showNumberTransactionsForFlatType(year_ddl):
    df = df3[df3['listing_year'] == year_ddl]
    fig = px.bar(df, x='flat_type', y='transaction_count', height=400)
    return fig