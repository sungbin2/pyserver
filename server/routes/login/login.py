from server.main_ import app, orm, c


@app.route('/')
def hello_world():
    return c.redirect(c.url_for('_window'))


@app.route('/login', methods=['GET', 'POST'])
def _login():
    error = ''
    if c.is_GET():
        pass
    elif c.is_POST():
        with orm.session_scope() as ss:  # type:c.typeof_Session

            id = c.data_POST('user')
            pw = c.data_POST('password')

            account = ss.query(orm.account) \
                .filter_by(s='0') \
                .filter_by(아이디=id) \
                .first()

            if account is None:
                error = '아이디 또는 패스워드를 잘못 입력하셨습니다.'
            elif c.pw_hash(pw) != account.패스워드:
                error = '아이디 / 패스워드를 잘못 입력하셨습니다.'
            else:
                c.account_session(orm, account, c.session)
                return c.redirect(c.url_for('hello_world'))

    return c.display(error=error)


@app.route('/logout', methods=['GET', 'POST'])
def _logout():
    c.session['logged_in'] = False
    return c.redirect('http://asp.van.or.kr:8081/login')
