import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
from mainFolder import dash_testGraph_graph, app
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px

#df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')
df = pd.read_csv('mainFolder\example1.csv')
#available_indicators = df['Indicator Name'].unique()
available_indicators = df['town'].unique()

url = 'https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv'
dataset = pd.read_csv(url)

px.set_mapbox_access_token('pk.eyJ1IjoidG9ja2V0IiwiYSI6ImNrN3p5dHAxczAxejgzbnA1Z2V1c2Y3eHIifQ.7-31EkU6G7Vsie54KNriBQ')
df = px.data.carshare()
fig = px.scatter_mapbox(df, lat="centroid_lat", lon="centroid_lon",     color="peak_hour", size="car_hours",
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)

dash_testGraph_graph.layout = dcc.Graph(
    id='exmaple-graph',
    figure=fig
)


