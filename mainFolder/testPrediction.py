
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
#from dash.exceptions import PreventUpdate

import pandas as pd
from mainFolder import app, dash_testPrediction_graph

# 2010 - 2020 (10 years for actual)
# 2020 - 2030 (10 years for predicted)

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

# Extract the first row
#town_data = lrf_data.iloc[0]
#print(town_data)
#print(town_data.a1)

# Create an empty list for actual year, predict year, actual resale price and new resale price to plot the x and y axis
actual_year=[]
predict_year=[]
actual_resale_price=[]
predict_resale_price=[]

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
            #dcc.Dropdown(
            #    id='dropdown_address',
            #    value='Block 142 PASIR RIS ST 11'
            #),
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

    html.Hr(),

    # Actual Line Graph
    dcc.Graph(id='actual-line-graph'),

    html.Hr(),

    # Predicted Line Graph
    dcc.Graph(id='predicted-line-graph')

])

#def setAddressMethod(town):
#    filtered_dropdown_town = hdb_data_2010_onwards[hdb_data_2010_onwards['town'] == town]
#    filtered_dropdown_address = filtered_dropdown_town['Full_Address'].unique()
#    print("Town",town, "Unique Address", filtered_dropdown_address)
#    return filtered_dropdown_address

#@dash_testPrediction_graph.callback(
#    Output('dropdown_address', 'options'),
#    [Input('dropdown_town', 'value')])
#def set_address_options(selected_town):
    
#    filtered_dropdown_address = setAddressMethod(selected_town)
#    return dcc.Dropdown(
#                options=[{'label': i, 'value': i} for i in filtered_dropdown_address]
#                #value=filtered_dropdown_address.iloc[0]['Full_Address']
#            )

#@dash_testPrediction_graph.callback(
#    Output('dropdown_address', 'value'),
#    [Input('dropdown_address', 'options')])
#def set_address_values(availabe_options):
#    return availabe_options[0]['value']

def create_actual_line_graph(title):
    return {
        'data': [dict(
            x=actual_year,
            y=actual_resale_price,
            mode='lines+markers',
            name=title
        )],
        'layout': {
            'height': 300,
            'margin': {'l': 100, 'b': 50, 'r': 0, 't': 40},
            'annotations': [{
                'x': 1, 'y': 1, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'valign' : 'top',
                'text': "Town"
            }],
             'title':'Actual Resale Price of Each Town',
             'showlegend':True,
              'legend':dict(
                x=1.0,
                y=1.0
              ),
              'xaxis':{
                'title': "Years"
                },
               'yaxis':{
                'title': "Actual Price"
                },
        }
    }

@dash_testPrediction_graph.callback(
    dash.dependencies.Output('actual-line-graph', 'figure'),
    [dash.dependencies.Input('dropdown_town', 'value'),
     dash.dependencies.Input('dropdown_address', 'value'),
     dash.dependencies.Input('dropdown_floorarea', 'value'),
     dash.dependencies.Input('dropdown_remaininglease', 'value'),
     dash.dependencies.Input('dropdown_listyear', 'value'),
     dash.dependencies.Input('dropdown_flattype', 'value'),
     dash.dependencies.Input('dropdown_storeyrange', 'value'),
     dash.dependencies.Input('dropdown_flatmodel', 'value')])
def update_actual_line_graph(dropdown_town, dropdown_address, dropdown_floorarea, dropdown_remaininglease, dropdown_listyear, dropdown_flattype, dropdown_storeyrange, dropdown_flatmodel):
    print("Town: ",dropdown_town)
    print("Address: ",dropdown_address)
    print("Floor Area: ",dropdown_floorarea)
    print("Remaining Lease Years: ",dropdown_remaininglease)
    print("Listing Year: ",dropdown_listyear)
    print("Listing Year Type: ",type(dropdown_listyear))
    print("Flat Type: ",dropdown_flattype)
    print("Storey Range: ",dropdown_storeyrange)
    print("Flat Model: ",dropdown_flatmodel)

    actual_result = find_actual_resale_price(dropdown_town, dropdown_address, int(dropdown_listyear))
    cat_to_num_result = convertCatToNum(dropdown_flattype, dropdown_storeyrange, dropdown_flatmodel)

    #actual_result[0] - town_result, actual_result[1] - min_dist_mrt, actual_result[2] - min_dist_mall, actual_result[3] - cbd_dist, 
    #cat_to_num_result[0] - flat_type_num, cat_to_num_result[1] - storey_range_num, cat_to_num_result[2] - flat_model_num
    calculate_resale_price(int(dropdown_floorarea), int(dropdown_remaininglease), actual_result[0], actual_result[1], actual_result[2], actual_result[3], int(dropdown_listyear), cat_to_num_result[0], cat_to_num_result[1], cat_to_num_result[2])

    return create_actual_line_graph(actual_result[0])

def create_predicted_line_graph(title):
    return {
        'data': [dict(
            x=predict_year,
            y=predict_resale_price,
            mode='lines+markers',
            name=title
        )],
        'layout': {
            'height': 300,
            'margin': {'l': 100, 'b': 50, 'r': 0, 't': 40},
            'annotations': [{
                'x': 1, 'y': 1, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'valign' : 'top',
                'text': "Town"
            }],
             'title':'Predicted Resale Price of Each Town',
             'showlegend':True,
              'legend':dict(
                x=1.0,
                y=1.0
              ),
              'xaxis':{
                'title': "Years"
                },
               'yaxis':{
                'title': "Predicted Price"
                },
        }
    }

@dash_testPrediction_graph.callback(
    dash.dependencies.Output('predicted-line-graph', 'figure'),
    [dash.dependencies.Input('dropdown_town', 'value'),
     dash.dependencies.Input('dropdown_address', 'value'),
     dash.dependencies.Input('dropdown_floorarea', 'value'),
     dash.dependencies.Input('dropdown_remaininglease', 'value'),
     dash.dependencies.Input('dropdown_listyear', 'value'),
     dash.dependencies.Input('dropdown_flattype', 'value'),
     dash.dependencies.Input('dropdown_storeyrange', 'value'),
     dash.dependencies.Input('dropdown_flatmodel', 'value')])
def update_predicted_line_graph(dropdown_town, dropdown_address, dropdown_floorarea, dropdown_remaininglease, dropdown_listyear, dropdown_flattype, dropdown_storeyrange, dropdown_flatmodel):
    print("Town: ",dropdown_town)
    print("Address: ",dropdown_address)
    print("Floor Area: ",dropdown_floorarea)
    print("Remaining Lease Years: ",dropdown_remaininglease)
    print("Listing Year: ",dropdown_listyear)
    print("Listing Year Type: ",type(dropdown_listyear))
    print("Flat Type: ",dropdown_flattype)
    print("Storey Range: ",dropdown_storeyrange)
    print("Flat Model: ",dropdown_flatmodel)

    actual_result = find_actual_resale_price(dropdown_town, dropdown_address, int(dropdown_listyear))
    cat_to_num_result = convertCatToNum(dropdown_flattype, dropdown_storeyrange, dropdown_flatmodel)

    #actual_result[0] - town_result, actual_result[1] - min_dist_mrt, actual_result[2] - min_dist_mall, actual_result[3] - cbd_dist, 
    #cat_to_num_result[0] - flat_type_num, cat_to_num_result[1] - storey_range_num, cat_to_num_result[2] - flat_model_num
    calculate_resale_price(int(dropdown_floorarea), int(dropdown_remaininglease), actual_result[0], actual_result[1], actual_result[2], actual_result[3], int(dropdown_listyear), cat_to_num_result[0], cat_to_num_result[1], cat_to_num_result[2])

    return create_predicted_line_graph(actual_result[0])

def create_bar_graph(title):
    return {
        'data': [
                {'x': actual_year, 'y': actual_resale_price, 'type': 'bar', 'name': 'Actual Price'},
                {'x': predict_year, 'y': predict_resale_price, 'type': 'bar', 'name': u'Predicted Price'},
            ],
            'layout': {
                'title': title,
                'xaxis':{
                'title': "Years"
                },
               'yaxis':{
                'title': "Resale Price"
                },
            }
    }

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

    actual_result = find_actual_resale_price(dropdown_town, dropdown_address, int(dropdown_listyear))
    cat_to_num_result = convertCatToNum(dropdown_flattype, dropdown_storeyrange, dropdown_flatmodel)

    #actual_result[0] - town_result, actual_result[1] - min_dist_mrt, actual_result[2] - min_dist_mall, actual_result[3] - cbd_dist, 
    #cat_to_num_result[0] - flat_type_num, cat_to_num_result[1] - storey_range_num, cat_to_num_result[2] - flat_model_num
    calculate_resale_price(int(dropdown_floorarea), int(dropdown_remaininglease), actual_result[0], actual_result[1], actual_result[2], actual_result[3], int(dropdown_listyear), cat_to_num_result[0], cat_to_num_result[1], cat_to_num_result[2])

    return create_bar_graph(actual_result[0])

def find_actual_resale_price(town, address, listingyear):
    global isDefault_actual_resale_price

    town_result = "PASIR RIS"
    min_dist_mrt = 876.562453385642
    min_dist_mall = 749.497865968619
    cbd_dist = 9028.44930163097

    # Clear the lists
    actual_year.clear()
    actual_resale_price.clear()
    
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
                    actual_resale_price.append(complete_hdb_data.iloc[row]['resale_price'])
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
                    actual_resale_price.append(complete_hdb_data.iloc[row]['resale_price'])
                    min_dist_mrt = complete_hdb_data.iloc[row]['min_dist_mrt']
                    min_dist_mall = complete_hdb_data.iloc[row]['min_dist_mall']
                    cbd_dist = complete_hdb_data.iloc[row]['cbd_dist']
                    break
        town_result = town
        
    return town_result, min_dist_mrt, min_dist_mall, cbd_dist

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
def calculate_resale_price(floorarea, remaininglease, town, min_dist_mrt, min_dist_mall, cbd_dist, listingyear, flat_type_num, storey_range_num, flat_model_num):
    global isDefault_predict_resale_price
    predictyear = 2020

    # Clear the lists
    predict_year.clear()
    predict_resale_price.clear()

    if isDefault_predict_resale_price: 
        # Hardcoded for the first time
        floorarea = 67
        remaininglease = 86
        listingyear = 2020

        # Extract the first row (Pasir Ris)
        town_data = lrf_data.iloc[0]

        for eachYear in range(2010, listingyear+1):
            new_resale_price = town_data.a1*floorarea + town_data.a2*remaininglease + town_data.a3*min_dist_mrt + town_data.a4*min_dist_mall + town_data.a5*cbd_dist + town_data.a6*eachYear + town_data.a7*flat_type_num + town_data.a8*storey_range_num + town_data.a9*flat_model_num + town_data.Intercept
            predict_year.append(predictyear)
            predict_resale_price.append(new_resale_price)
            predictyear += 1
            
        isDefault_predict_resale_price = False       
    else:
        # Find the matching town based on the selected dropdown town
        for row in range(len(lrf_data)):
            if lrf_data.iloc[row]['town'] == town:
                town_data = lrf_data.iloc[row]
                #print("Corresponding Town: ", town_data)

        for eachYear in range(2010, listingyear+1):
            new_resale_price = town_data.a1*floorarea + town_data.a2*remaininglease + town_data.a3*min_dist_mrt + town_data.a4*min_dist_mall + town_data.a5*cbd_dist + town_data.a6*eachYear + town_data.a7*flat_type_num + town_data.a8*storey_range_num + town_data.a9*flat_model_num + town_data.Intercept
            predict_year.append(predictyear)
            predict_resale_price.append(new_resale_price)
            predictyear += 1