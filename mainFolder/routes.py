from mainFolder import app
# , mysql, bcrypt, phone
from flask import render_template, flash, redirect, url_for, request
from mainFolder import gridtable, dao
from flask import Flask, render_template
from datetime import datetime

# , session, logging, request, g, make_response
# from flask_mysqldb import MySQL
# from passlib.hash import sha256_crypt
# import json
# import pandas as pd
# from datetime import datetime, timedelta,timezone
# from time import strftime
# from pytz import timezone
# import tzlocal
# import uuid
# import os
# import xlsxwriter
# from openpyxl import load_workbook
# import subprocess
# import cookies
# from bs4 import BeautifulSoup
# import requests
# import urllib.request
# import mechanize
# import http.cookiejar as cookielib

# app = Flask(__name__)


@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login.html', title='Login')

@app.route("/mainPage", methods=['GET', 'POST'])
def mainPage():
    # for all the template pages, render this.
    # requestedID = dao.daoTest()
    return render_template('mainpage.html', title='Home')

@app.route("/viewListing", methods=['GET', 'POST'])
def viewListing():
    #dao.jsonConvert()
    table = gridtable.loadJson()
    return render_template('viewListing.html', tables=table)

@app.route("/predictionTool", methods=['GET', 'POST'])
def predictionTool():
    return render_template('predictiontool.html', title='Prediction Tool')


@app.route("/viewAnalytics", methods=['GET', 'POST'])
def viewAnalytics():
    return render_template('viewanalytics.html', title='View Analytics')


# then when u need to have dynamic functions on page i.e clicking a button, saving some data
# use ajax instead. then call the function itself

@app.route("/function", methods=['GET', 'POST'])
def function():
    # get your data from your html
    return render_template('test.html', title='Home')
