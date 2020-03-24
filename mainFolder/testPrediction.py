import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
#from dash.exceptions import PreventUpdate

import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
from mainFolder import app, dash_testPrediction_graph

# 2010 - 2020 (10 years for actual)
# 2020 - 2025 (5 years for predicted)

hdb_data = pd.read_csv('./mainFolder/final_df.csv')
lrf_data = pd.read_csv('./mainFolder/linear_regression_formula.csv')

#Select only data from year 2010 onwards 
hdb_data_2010_onwards = hdb_data[hdb_data['listing_year'] > 2009]

# Unique town, address, floor area, remaning lease years, listing year, flat type, storey range and flat model
unique_town = hdb_data_2010_onwards['town'].unique()
unique_address = hdb_data_2010_onwards['Full_Address'].unique()
unique_floorarea = hdb_data_2010_onwards['floor_area_sqm'].unique()
unique_remaininglease = hdb_data_2010_onwards['remaining_lease'].unique()
unique_listingyear = hdb_data_2010_onwards['listing_year'].unique()
unique_flattype = hdb_data_2010_onwards['flat_type'].unique()
unique_storeyrange = hdb_data_2010_onwards['storey_range'].unique()
unique_flatmodel = hdb_data_2010_onwards['flat_model'].unique()

# Create an empty list for actual year, predict year, actual resale price and new resale price to plot the x and y axis
actual_year=[]
predict_year=[]
actual_resale_price_per_sqm=[]
predict_resale_price_per_sqm=[]

# Initialize Boolean Default Value for hardcoding the graph
isDefault_predict_resale_price = True
isDefault_actual_resale_price = True
isDefault_cat_to_num = True

dash_testPrediction_graph.layout = html.Div([

    html.Div([
        html.Div([
            html.P("Select Town"),
            dcc.Dropdown(
                id='dropdown_town',
                options=[{'label': i, 'value': i} for i in unique_town],
                value='PASIR RIS'
            ),
            html.P("Select Floor Area in square meters"),
            dcc.Dropdown(
                id='dropdown_floorarea',
                options=[{'label': i, 'value': i} for i in unique_floorarea],
                value='67'
            ),
            html.P("Select Listing Year"),
            dcc.Dropdown(
                id='dropdown_listyear',
                options=[{'label': i, 'value': i} for i in unique_listingyear],
                value='2010'
            ),
            html.P("Select Storey Range"),
            dcc.Dropdown(
                id='dropdown_storeyrange',
                options=[{'label': i, 'value': i} for i in unique_storeyrange],
                value='04 TO 06'
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            html.P("Select Address"),
            dcc.Dropdown(
                id='dropdown_address',
                options=[{'label': i, 'value': i} for i in unique_address],
                value='Block 142 PASIR RIS ST 11'
            ),
            html.P("Select Remaining Lease Years"),
            dcc.Dropdown(
                id='dropdown_remaininglease',
                options=[{'label': i, 'value': i} for i in unique_remaininglease],
                value='86'
            ),
            html.P("Select Flat Type"),
            dcc.Dropdown(
                id='dropdown_flattype',
                options=[{'label': i, 'value': i} for i in unique_flattype],
                value='4 ROOM'
            ),
            html.P("Select Flat Model"),
            dcc.Dropdown(
                id='dropdown_flatmodel',
                options=[{'label': i, 'value': i} for i in unique_flatmodel],
                value='model a'
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
        ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    # Bar Graph
    dcc.Graph(id='bar-graph'),

    html.Hr()
])

@dash_testPrediction_graph.callback(
    dash.dependencies.Output('bar-graph', 'figure'),
    [dash.dependencies.Input('dropdown_town', 'value'),
     dash.dependencies.Input('dropdown_address', 'value'),
     dash.dependencies.Input('dropdown_floorarea', 'value'),
     dash.dependencies.Input('dropdown_remaininglease', 'value'),
     dash.dependencies.Input('dropdown_listyear', 'value'),
     dash.dependencies.Input('dropdown_flattype', 'value'),
     dash.dependencies.Input('dropdown_storeyrange', 'value'),
     dash.dependencies.Input('dropdown_flatmodel', 'value')])
def update_bar_graph(dropdown_town, dropdown_address, dropdown_floorarea, dropdown_remaininglease, dropdown_listyear, dropdown_flattype, dropdown_storeyrange, dropdown_flatmodel):

    actual_result = find_actual_resale_price_per_sqm(dropdown_town, dropdown_address, int(dropdown_listyear))
    cat_to_num_result = convertCatToNum(dropdown_flattype, dropdown_storeyrange, dropdown_flatmodel)

    #actual_result[0] - town_result, actual_result[1] - min_dist_mrt, actual_result[2] - min_dist_mall, actual_result[3] - cbd_dist, 
    #cat_to_num_result[0] - flat_type_num, cat_to_num_result[1] - storey_range_num, cat_to_num_result[2] - flat_model_num
    calculate_resale_price_per_sqm(int(dropdown_floorarea), int(dropdown_remaininglease), actual_result[0], actual_result[1], actual_result[2], actual_result[3], actual_result[4], int(dropdown_listyear), cat_to_num_result[0], cat_to_num_result[1], cat_to_num_result[2])
    print("actual_year",actual_year)
    print("actual_resale_price_per_sqm",actual_resale_price_per_sqm)
    print("predict_year",predict_year)
    print("predict_resale_price_per_sqm",predict_resale_price_per_sqm)

    total_year = actual_year + predict_year
    total_resale_price_per_sqm = actual_resale_price_per_sqm + predict_resale_price_per_sqm
    column_color = [0]*len(total_year)
    df = pd.DataFrame(
    {'totalyear': total_year,
     'totalresale_price_per_sqm': total_resale_price_per_sqm,
     'predicted_column_color': column_color
    })
    df.iloc[len(column_color)-6:].predicted_column_color = 1
    print("Dataframe",df)

    fig = px.bar(df,  x = 'totalyear', y ='totalresale_price_per_sqm', color='predicted_column_color',
                 labels={'totalyear':'Year ', 'totalresale_price_per_sqm':'Resale Price per sqm'}, height=400)
    
    fig.update_layout(title_text=actual_result[0])

    return fig
 
def find_actual_resale_price_per_sqm(town, address, listingyear):
    global isDefault_actual_resale_price

    town_result = "PASIR RIS"
    min_dist_mrt = 876.562453385642
    min_dist_mall = 749.497865968619
    cbd_dist = 9028.44930163097
    price_per_sqm = 290.322580645161
    resale_price = 500000

    # Clear the lists
    actual_year.clear()
    actual_resale_price_per_sqm.clear()
    
    if isDefault_actual_resale_price:
        # Hardcoded for the first time
        listingyear = 2020
        filtered_town = hdb_data_2010_onwards[hdb_data_2010_onwards['town'] == "PASIR RIS"]
        filtered_town_and_address = filtered_town[filtered_town['Full_Address'] == "Block 142 PASIR RIS ST 11"]
        filtered_listingyear_and_resaleprice = filtered_town_and_address.groupby(['listing_year'],as_index=True).mean()[['resale_price']]
        filtered_listingyear_and_resaleprice.reset_index(inplace=True)
        complete_hdb_data = pd.merge(filtered_town_and_address, filtered_listingyear_and_resaleprice[['listing_year','resale_price']],on='listing_year')
        # Drop resale_price_x column
        complete_hdb_data.drop(['resale_price_x'], axis=1, inplace=True)
        # Rename "resale_price_y" to "resale_price"
        complete_hdb_data.rename(columns = {'resale_price_y': 'resale_price'}, inplace = True)

        for eachYear in range(2010, listingyear+1):
            for row in range(len(complete_hdb_data)):
                if complete_hdb_data.iloc[row]['listing_year'] == eachYear:
                    actual_year.append(eachYear)
                    actual_resale_price_per_sqm.append(complete_hdb_data.iloc[row]['price_per_sqm'])
                    break
        isDefault_actual_resale_price = False
    else: 

        filtered_town = hdb_data_2010_onwards[hdb_data_2010_onwards['town'] == town]
        filtered_town_and_address = filtered_town[filtered_town['Full_Address'] == address]
        filtered_listingyear_and_resaleprice = filtered_town_and_address.groupby(['listing_year'],as_index=True).mean()[['resale_price']]
        filtered_listingyear_and_resaleprice.reset_index(inplace=True)
        complete_hdb_data = pd.merge(filtered_town_and_address, filtered_listingyear_and_resaleprice[['listing_year','resale_price']],on='listing_year')
        # Drop resale_price_x column
        complete_hdb_data.drop(['resale_price_x'], axis=1, inplace=True)
        # Rename "resale_price_y" to "resale_price"
        complete_hdb_data.rename(columns = {'resale_price_y': 'resale_price'}, inplace = True)

        for eachYear in range(2010, listingyear+1):
            for row in range(len(complete_hdb_data)):
                if complete_hdb_data.iloc[row]['listing_year'] == eachYear:
                    actual_year.append(eachYear)
                    actual_resale_price_per_sqm.append(complete_hdb_data.iloc[row]['price_per_sqm'])
                    min_dist_mrt = complete_hdb_data.iloc[row]['min_dist_mrt']
                    min_dist_mall = complete_hdb_data.iloc[row]['min_dist_mall']
                    cbd_dist = complete_hdb_data.iloc[row]['cbd_dist']
                    resale_price = complete_hdb_data.iloc[row]['resale_price']
                    break
        town_result = town
        
    return town_result, min_dist_mrt, min_dist_mall, cbd_dist, resale_price

def convertCatToNum(flat_type_cat, storey_range_cat, flat_model_cat):
    global isDefault_cat_to_num

    myDict = {'5 ROOM': 1,
             'MULTI GENERATION': 2,
             'MULTI-GENERATION': 3,
             '1 ROOM': 4,
             '4 ROOM': 5,
             '3 ROOM': 6,
             '2 ROOM': 7,
             'EXECUTIVE': 8,
             '37 TO 39': 1,
             '10 TO 12': 2,
             '40 TO 42': 3,
             '46 TO 48': 4,
             '13 TO 15': 5,
             '11 TO 15': 6,
             '16 TO 20': 7,
             '01 TO 03': 8,
             '49 TO 51': 9,
             '01 TO 05': 10,
             '22 TO 24': 11,
             '31 TO 35': 12,
             '43 TO 45': 13,
             '28 TO 30': 14,
             '25 TO 27': 15,
             '21 TO 25': 16,
             '19 TO 21': 17,
             '07 TO 09': 18,
             '16 TO 18': 19,
             '31 TO 33': 20,
             '06 TO 10': 21,
             '36 TO 40': 22,
             '34 TO 36': 23,
             '26 TO 30': 24,
             '04 TO 06': 25,
             'new generation': 1,
             'multi generation': 2,
             'standard': 3,
             'improved-maisonette': 4,
             'type s2': 5,
             'improved': 6,
             'premium apartment': 7,
             'simplified': 8,
             'apartment': 9,
             'adjoined flat': 10,
             '2-room': 11,
             'premium maisonette': 12,
             'model a': 13,
             'model a-maisonette': 14,
             'type s1': 15,
             'model a2': 16,
             'premium apartment loft': 17,
             'terrace': 18,
             'dbss': 19,
             'maisonette': 20}

    if isDefault_cat_to_num:
        # Hardcoded for the first time
        for key in myDict : 
            if key == "4 ROOM":
                flat_type_num = myDict[key]
            if key == "04 TO 06":
                storey_range_num = myDict[key] 
            if key == "model a":
                flat_model_num = myDict[key]
        isDefault_cat_to_num = False
    else:
        for key in myDict :
            if key == flat_type_cat:
                flat_type_num = myDict[key]
            if key == storey_range_cat:
                storey_range_num = myDict[key]
            if key == flat_model_cat:
                flat_model_num = myDict[key]
    return flat_type_num, storey_range_num, flat_model_num

# Linear Regression Formula - Calculate the number of years the user wants to predict to
def calculate_resale_price_per_sqm(floorarea, remaininglease, town, min_dist_mrt, min_dist_mall, cbd_dist, resale_price, listingyear, flat_type_num, storey_range_num, flat_model_num):
    global isDefault_predict_resale_price
    futureyear = 2020

    # Clear the lists
    predict_year.clear()
    predict_resale_price_per_sqm.clear()

    if isDefault_predict_resale_price: 
        # Hardcoded for the first time
        floorarea = 67
        remaininglease = 86
        listingyear = 2020

        # Extract the first row (Pasir Ris)
        town_data = lrf_data.iloc[0]

        for predictedYear in range(futureyear, futureyear+6):
            new_resale_price_per_sqm = town_data.a1*floorarea + town_data.a2*remaininglease + town_data.a3*min_dist_mrt + town_data.a4*min_dist_mall + town_data.a5*cbd_dist + town_data.a6*predictedYear + town_data.a7*resale_price + town_data.a8*flat_type_num + town_data.a9*storey_range_num + town_data.a10*flat_model_num + town_data.Intercept
            print("year:" + str(predictedYear) + "price_per_sqm" + str(new_resale_price_per_sqm))
            predict_year.append(predictedYear)
            predict_resale_price_per_sqm.append(new_resale_price_per_sqm)
            remaininglease -= 1

        isDefault_predict_resale_price = False       
    else:
        # Find the matching town based on the selected town in dropdown 
        for row in range(len(lrf_data)):
            if lrf_data.iloc[row]['town'] == town:
                town_data = lrf_data.iloc[row]
                #print("Corresponding Town: ", town_data)

        for predictedYear in range(futureyear, futureyear+6):
            new_resale_price_per_sqm = town_data.a1*floorarea + town_data.a2*remaininglease + town_data.a3*min_dist_mrt + town_data.a4*min_dist_mall + town_data.a5*cbd_dist + town_data.a6*predictedYear + town_data.a7*resale_price + town_data.a8*flat_type_num + town_data.a9*storey_range_num + town_data.a10*flat_model_num + town_data.Intercept
            predict_year.append(predictedYear)
            predict_resale_price_per_sqm.append(new_resale_price_per_sqm)
            remaininglease -= 1