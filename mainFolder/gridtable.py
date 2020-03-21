import json
from json2html import *
from datetime import datetime

def loadJson():
    now = datetime.now().time()
    print("JSONLOAD")
    print(now)
    json_d = 'data/final_df.json'
    with open(json_d, encoding='utf-8', errors='ignore') as json_data:
        data = json.load(json_data, strict=False)

    # print(data)
    formatted_table = json2html.convert(json=data,table_attributes="id=\"hdb_tableid\"")
    now2 = datetime.now().time()
    print("JSONFIN")
    print(now2)
    #print(formatted_table)
    return formatted_table

    