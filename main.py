from api.server import create_app

def main():
    app, socketio = create_app()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()