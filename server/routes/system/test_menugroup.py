from server.main_ import app, orm, c


@app.route('/system/menugroup', methods=['GET', ])
def _system_menugroup():
    store_id = c.session['store']

    if c.is_GET():

        return c.display(store_id=store_id)
    else:
        return c.display(store_id=store_id)


@app.route('/system/menugroup/<int:_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def _system_menugroup_(_id):
    store_id = c.session['store']

    if c.is_json():
        if c.is_GET():
            with orm.session_scope() as ss:  # type:c.typeof_Session
                q1 = ss.query(orm.상품_분류) \
                    .filter_by(s=store_id) \
                    .filter_by(isdel='X') \
                    .all()
                for x in q1:
                    dummy = x.__dict__.copy()
                    del dummy['_sa_instance_state']
                    for k, v in dummy.items():
                        if v is None:
                            dummy[k] = ''
                        elif isinstance(v, date):
                            dummy[k] = v.isoformat()
                        elif isinstance(v, datetime):
                            dummy[k] = v.isoformat(' ')
                    l.append(dummy)
            return c.jsonify(l)

    c.abort(404)

