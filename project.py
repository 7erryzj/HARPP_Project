from mainFolder import app, testGraph
#, dash_line_graph, dash_live_graph

if __name__ == '__main__':
    #debug mode, you can  make changes and go to the cmd press enter to refresh
    #works for all except css. css u need to restart server
    app.run(debug=True)

    #production running.
    #app.run(host='0.0.0.0', port='8050')
