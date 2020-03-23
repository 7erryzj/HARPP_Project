import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
from mainFolder import dash_mapGraph_graph, app
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px

HDB = pd.read_csv('mainFolder/final_df.csv',low_memory=False)
available_year = HDB['listing_year'].unique()
available_year.sort()

dash_mapGraph_graph.layout = html.Div([

    html.Div([
            dcc.Dropdown(
                id='year-ddl',
                options=[{'label': i, 'value': i} for i in available_year],
                value=1990
            )
        ]),
    dcc.Graph(
            id='map-graph'
    )
])

@dash_mapGraph_graph.callback(
    Output('map-graph', 'figure'),
    [Input('year-ddl', 'value')])

def showNumberTransactionsForFlatType(year_ddl):
    dataset = HDB.loc[(HDB.listing_year == year_ddl)].drop(
    columns=['block', 'region','flat_model_cat','storey_range_cat',
            'flat_type_cat','in_2017','cbd_dist','min_dist_mall','min_dist_mrt',
            'remaining_lease','lease_commence_date','flat_model','floor_area_sqm',
            'town', 'month', 'street_name','flat_type','storey_range','DF','Full_Address'])

    # Create a df with unique lat,long coordinates
    non_duplicate_df = dataset.drop_duplicates(subset=['lat','long'], keep=False)
    non_duplicate_df['Sales for the year'] = 1
    non_duplicate_df = non_duplicate_df.reindex(columns=['long','lat','Sales for the year','price_per_sqm','resale_price'])
    non_duplicate_df = non_duplicate_df.rename(columns={'price_per_sqm':'Average Price Per Sqm',
                                                        'resale_price':'avg_resale_price'})

    # Create a df with non-unique lat,long coordinates
    duplicate_df = dataset.loc[dataset.duplicated(subset=['lat','long'], keep=False)]
    # Group the duplicate_df
    gb = duplicate_df.groupby(['long', 'lat'], as_index=True)
    # Create a df with the coutns for each pair of lat,long coordinates
    counts = gb.size().to_frame(name='counts')
    # Perform mean operation and rename columns as such
    duplicate_df = (counts
                    .join(gb.agg({'price_per_sqm': 'mean'}).rename(columns={'price_per_sqm': 'Average Price Per Sqm'}))
                    .join(gb.agg({'resale_price': 'mean'}).rename(columns={'resale_price': 'avg_resale_price'}))
                    .reset_index()
                )
    # Final renaming of columns, for the map display
    duplicate_df = duplicate_df.rename(columns={'counts':'Sales for the year'})

    # Finally, we concat both df together to form the final df to plot
    plotting_df = pd.concat([duplicate_df, non_duplicate_df])
    ############################################################
    ##################### PLOTLY PLOTTING ######################
    ############################################################
    # Plotting the Map
    px.set_mapbox_access_token('pk.eyJ1IjoidG9ja2V0IiwiYSI6ImNrN3p5dHAxczAxejgzbnA1Z2V1c2Y3eHIifQ.7-31EkU6G7Vsie54KNriBQ')
    fig = px.scatter_mapbox(plotting_df, lat="lat", lon="long",     
                            color="Average Price Per Sqm", size="Sales for the year",
                    color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)

    fig.update_layout(
         title={
        'text': "Map Graph",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}
    )
    return fig
    #######################################################

