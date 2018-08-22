from server.main_ import app, c


@app.route('/weather', methods=['GET', 'POST'])
def _weather():
    if c.is_GET():
        pass
    elif c.is_POST():
        pass

    return c.display()
