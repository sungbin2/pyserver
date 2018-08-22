from server.main_ import app, c


@app.route('/mobile', methods=['GET', 'POST'])
def _mobile():
    if c.is_GET():
        pass
    elif c.is_POST():
        pass

    return c.display()
