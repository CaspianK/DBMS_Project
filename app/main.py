from website import create_app, start_pool
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)