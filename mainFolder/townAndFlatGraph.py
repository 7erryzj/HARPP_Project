import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
from mainFolder import dash_townAndFlatGraph_graph, app
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px

hdb = pd.read_csv('./mainFolder/final_df.csv')
df4 = hdb.groupby(['listing_year','town','flat_type'],as_index=True).mean()[['resale_price']]
df4.reset_index(inplace=True)
available_town = hdb['town'].unique()
available_flat = hdb['flat_type'].unique()
#options in the filter are : all the unique towns in town column, all the unique flat types in flat_type column

dash_townAndFlatGraph_graph.layout = html.Div([
    html.Div([
        html.Div([
                dcc.Dropdown(
                    id='town-ddl',
                    options=[{'label': i, 'value': i} for i in available_town],
                    value='ANG MO KIO'
                )
            ],
            style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='flat-ddl',
                    options=[{'label': i, 'value': i} for i in available_flat],
                    value='1 ROOM'
                )
            ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
        ]),

        dcc.Graph(
                id='bar-graph'
        ),
    ])

@dash_townAndFlatGraph_graph.callback(
    Output('bar-graph', 'figure'),
    [Input('town-ddl', 'value'),
     Input('flat-ddl', 'value')])

def showNumberTransactionsForTownAndFlatModel(town, flatType):
    df = df4[ (df4['town'] == town) & (df4['flat_type'] == flatType) ]
    fig = px.bar(df, x='listing_year', y='resale_price',
             labels={'resale_price':'Average Resale Price for ' + town + ' ' +flatType , 'listing_year':'Year'}, height=400)
    fig.update_layout(
         title={
        'text': "Transactions For Town And Flat Model",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}
    )
    return fig