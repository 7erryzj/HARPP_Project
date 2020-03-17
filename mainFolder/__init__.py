from flask import Flask
#from flask_mysqldb import MySQL
#from flask_bcrypt import Bcrypt
#from flask_login import LoginManager
import dash
import dash_html_components as html
#import os


app = Flask(__name__)

#random key generated. can be useful for example session cookie, authentication etc.
#app.config['SECRET_KEY'] = os.urandom(24) 

#for graph
#dash_line_graph = dash.Dash(__name__, sharing=True, server = app, static_folder='static', url_base_pathname='/line/')
#dash_live_graph = dash.Dash(__name__, sharing=True, server = app, static_folder='static', url_base_pathname='/live/')
#dash_graph_test = dash.Dash(__name__, server=app, url_base_pathname='/dash_graph_test/')
dash_testGraph_graph= dash.Dash(__name__, server=app,url_base_pathname='/testGraph/')

from mainFolder import routes, testGraph
#import graph
#, line, live