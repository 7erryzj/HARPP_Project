from flask import Flask
#from flask_mysqldb import MySQL
#from flask_bcrypt import Bcrypt
#from flask_login import LoginManager
import dash
#import os


app = Flask(__name__)

dash_testPrediction_graph= dash.Dash(__name__, server=app,url_base_pathname='/testPrediction/')
dash_transactionCountForXYear_graph= dash.Dash(__name__, server=app,url_base_pathname='/transactionCountForXYearGraph/')
dash_mapGraph_graph= dash.Dash(__name__, server=app,url_base_pathname='/mapGraph/')
dash_gapminderGraph_graph= dash.Dash(__name__, server=app,url_base_pathname='/gapminderGraph/')
dash_resaleBarGraph_graph= dash.Dash(__name__, server=app,url_base_pathname='/resaleBarGraph/')
dash_resaleAvgGraph_graph= dash.Dash(__name__, server=app,url_base_pathname='/resaleAvgGraph/')
dash_townAndFlatGraph_graph= dash.Dash(__name__, server=app,url_base_pathname='/townAndFlatGraph/')

from mainFolder import routes, transactionCountForXYearGraph, testPrediction, mapGraph, gapminderGraph, resaleBarGraph, resaleAvgGraph, townAndFlatGraph
#import graph
#, line, live