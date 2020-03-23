import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
from mainFolder import dash_resaleBarGraph_graph, app
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px

hdb = pd.read_csv('mainFolder/final_df.csv',low_memory=False)
df5 = hdb[['town', 'region', 'flat_type', 'flat_model', 'storey_range', 'remaining_lease', 'listing_year', 'resale_price']]

available_filter = ['town','region','flat_type','flat_model', 'storey_range', 'remaining_lease', 'listing_year']
#options in the filter are : town, region, flat type, flat mode, storey range, remaining lease, listing year

#to see relationship/trend between various factors with resale price

dash_resaleBarGraph_graph.layout = html.Div([

    html.Div([
            dcc.Dropdown(
                id='selection-ddl',
                options=[{'label': i, 'value': i} for i in available_filter],
                value='town'
            )
        ]),
    dcc.Graph(
            id='bar-graph'
    )
])

@dash_resaleBarGraph_graph.callback(
    Output('bar-graph', 'figure'),
    [Input('selection-ddl', 'value')])

def BarPlotForResalePrice(x_colName):
    df = df5.groupby([x_colName],as_index=True).mean()[['resale_price']]
    df.reset_index(inplace=True)
    fig = px.bar(df, x=x_colName, y='resale_price',
             labels={'resale_price':'Average Resale Price'}, height=400)
    
    fig.update_layout(
         title={
        'text': "Bar Plot For Resale Price",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}
    )
    return fig



