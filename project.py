from mainFolder import app
#, dash_line_graph, dash_live_graph

if __name__ == '__main__':
    #debug mode, you can  make changes and go to the cmd press enter to refresh
    #works for all except css. css u need to restart server
    #app.run(debug=True)

    #production running.
    #when u want to connect other device to this platform, u use this.
    app.run(host='0.0.0.0', port='8050')

