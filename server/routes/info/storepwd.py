from server.main_ import app, orm, c
from dateutil import parser


def _get_store(store_id):
    with orm.session_scope() as ss:  # type:c.typeof_Session
        only = ss.query(orm.정보_가게) \
            .filter_by(no=store_id) \
            .one()

        return c.OBJ_cp(only)


@app.route('/info/storepwd')
def _info_storepwd_():
    return c.redirect(c.url_for('_info_storepwd', store_id=c.session['store']))


@app.route('/info/storepwd/<int:store_id>', methods=['GET', 'POST', 'PUT'])
def _info_storepwd(store_id):
    if c.is_GET():
        if c.is_json():
            return c.jsonify(_get_store(store_id).for_json())
        else:
            return c.display()
    elif c.is_POST() or c.is_PUT():
        with orm.session_scope() as ss:  # type:c.typeof_Session
            only = ss.query(orm.정보_가게) \
                .filter_by(no=store_id) \
                .one()
            for k, v in c.data_POST().items():
                if getattr(only, k) != v:
                    print(k, 'is changed')
                    if k in ['개점일', '폐점일']:
                        try:
                            setattr(only, k, parser.parse(v))
                        except:
                            setattr(only, k, None)
                    else:
                        setattr(only, k, v)
            only.issync = None
        return c.display()