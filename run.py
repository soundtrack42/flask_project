from app import create_app, setup_app

if __name__ == '__main__':

    app = create_app()
    setup_app(app)
    app.run(debug=True)
