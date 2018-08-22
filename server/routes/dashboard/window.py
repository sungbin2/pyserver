from server.main_ import app, c


@app.route('/window', methods=['GET', 'POST'])
def _window():
    if c.is_GET():
        pass
    elif c.is_POST():
        pass

    return c.display()
