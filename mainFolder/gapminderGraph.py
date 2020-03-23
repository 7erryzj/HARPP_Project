import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
from mainFolder import dash_gapminderGraph_graph, app
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px

#df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')
#df = pd.read_csv('mainFolder\example1.csv')
#available_indicators = df['Indicator Name'].unique()
#available_indicators = df['town'].unique()
dataset = pd.read_csv('./mainFolder/gapminder_df.csv').drop(columns=['Unnamed: 0'])

# Make list of years in our dataset
years = []
for year in dataset['listing_year'].unique():
    years.append(str(year))
year = years.sort()

# Make list of Towns
towns = []
for town in dataset['town'].unique():
    towns.append(str(town))
    

# make figure
figure = {
    'data': [],
    'layout': {},
    'frames': []
}

# fill in most of layout
figure['layout']['xaxis'] = {'title': 'Price Per Square Meter'}
figure['layout']['yaxis'] = {'title': 'Resale Price'}
figure['layout']['hovermode'] = 'closest'
figure['layout']['sliders'] = {
    'args': [
        'transition', {
            'duration': 400,
            'easing': 'cubic-in-out'
        }
    ],
    'initialValue': '1990',
    'plotlycommand': 'animate',
    'values': years,
    'visible': True
}
figure['layout']['updatemenus'] = [
    {
        'buttons': [
            {
                'args': [None, {'frame': {'duration': 500, 'redraw': False},
                         'fromcurrent': True, 'transition': {'duration': 300, 'easing': 'quadratic-in-out'}}],
                'label': 'Play',
                'method': 'animate'
            },
            {
                'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate',
                'transition': {'duration': 0}}],
                'label': 'Pause',
                'method': 'animate'
            }
        ],
        'direction': 'left',
        'pad': {'r': 10, 't': 87},
        'showactive': False,
        'type': 'buttons',
        'x': 0.1,
        'xanchor': 'right',
        'y': 0,
        'yanchor': 'top'
    }
]

sliders_dict = {
    'active': 0,
    'yanchor': 'top',
    'xanchor': 'left',
    'currentvalue': {
        'font': {'size': 20},
        'prefix': 'Year:',
        'visible': True,
        'xanchor': 'right'
    },
    'transition': {'duration': 300, 'easing': 'cubic-in-out'},
    'pad': {'b': 10, 't': 50},
    'len': 0.9,
    'x': 0.1,
    'y': 0,
    'steps': []
}

# make data
year = 1990
for town in towns:
    dataset_by_year_and_town = dataset[(dataset['town'] == town) & (dataset['listing_year'] == int(year))]

    data_dict = {
        'x': list(dataset_by_year_and_town['price_per_sqm']),
        'y': list(dataset_by_year_and_town['resale_price']),
        'mode': 'markers',
        'text': list(dataset_by_year_and_town['flat_type']),
        'marker': {
            'sizemode': 'area',
            'sizeref': 0.9,
            'size': list(dataset_by_year_and_town['count'])
        },
        'name': town
    }
    figure['data'].append(data_dict)
    
# make frames
for year in years:
    frame = {'data': [], 'name': str(year)}
    for town in towns:
        dataset_by_year_and_town = dataset[(dataset['town'] == town) & (dataset['listing_year'] == int(year))]

        data_dict = {
            'x': list(dataset_by_year_and_town['price_per_sqm']),
            'y': list(dataset_by_year_and_town['resale_price']),
            'mode': 'markers',
            'text': list(dataset_by_year_and_town['flat_type']),
            'marker': {
                'sizemode': 'area',
                'sizeref': 0.9,
                'size': list(dataset_by_year_and_town['count'])
            },
            'name': town
        }
        frame['data'].append(data_dict)

    figure['frames'].append(frame)
    slider_step = {'args': [
        [year],
        {'frame': {'duration': 700, 'redraw': False},
         'mode': 'immediate',
       'transition': {'duration': 300}}
     ],
     'label': year,
     'method': 'animate'}
    sliders_dict['steps'].append(slider_step)

    
figure['layout']['sliders'] = [sliders_dict]

dash_gapminderGraph_graph.layout = dcc.Graph(
    id='exmaple-graph',
    figure=figure
)


