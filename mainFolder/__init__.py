from flask import Flask
#from flask_mysqldb import MySQL
#from flask_bcrypt import Bcrypt
#from flask_login import LoginManager
import dash
#import os


app = Flask(__name__)

dash_testGraph_graph= dash.Dash(__name__, server=app,url_base_pathname='/testGraph/')
dash_testGraph2_graph= dash.Dash(__name__, server=app,url_base_pathname='/testGraph2/')
dash_testPrediction_graph= dash.Dash(__name__, server=app,url_base_pathname='/testPrediction/')
dash_transactionCountForXYear_graph= dash.Dash(__name__, server=app,url_base_pathname='/transactionCountForXYearGraph/')
dash_mapGraph_graph= dash.Dash(__name__, server=app,url_base_pathname='/mapGraph/')
dash_gapminderGraph_graph= dash.Dash(__name__, server=app,url_base_pathname='/gapminderGraph/')

from mainFolder import routes, testGraph, testGraph2, transactionCountForXYearGraph, testPrediction, mapGraph, gapminderGraph
#import graph
#, line, live