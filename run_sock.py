from MyProj.app import app,socketio



# load_dotenv('.env')

if __name__ == '__main__':
    # app.run(debug = True)
    # 
    socketio.run(app,debug=True,port = 5000)
    # app.run(port=5005)
    # socketio.run(,debug=True)
    # app.run(debug = True)