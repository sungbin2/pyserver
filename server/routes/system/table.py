import json

from server.main_ import app, orm, c

form_types = [
    {'tag': '테이블명', 'name': 'name', 'type': 'input', 'valid': None, },
]


def tablegroup_query(ss, sid):
    return ss.query(orm.설정_테이블그룹) \
        .filter_by(sid=sid) \
        .order_by(ss.asc(orm.설정_테이블그룹.번호)) \
        .filter_by(isdel=c.X)


def table_query(ss, sid, group_id):
    return ss.query(orm.설정_테이블) \
        .filter_by(sid=sid) \
        .filter_by(group_id=group_id) \
        .order_by(ss.asc(orm.설정_테이블.번호)) \
        .filter_by(isdel=c.X)


@app.route('/system/table', methods=['GET', ])
def _system_table_():
    sid = c.session['store']

    with orm.session_scope() as ss:  # type:c.typeof_Session
        if c.is_GET():
            gl = tablegroup_query(ss, sid).first()
            return c.redirect(c.url_for('_system_table', group_id=gl.id))


@app.route('/system/table/<int:group_id>', methods=['GET', 'PUT', ])
def _system_table(group_id):
    sid = c.session['store']

    if c.is_json():
        if c.is_GET():
            with orm.session_scope() as ss:  # type:c.typeof_Session
                l = c.for_json_l(table_query(ss, sid, group_id).all())
                return c.jsonify(l)
        elif c.is_PUT():
            with orm.session_scope() as ss:  # type:c.typeof_Session
                for k, v in c.data_POST().items():
                    ol = json.loads(k)
                    for o in ol:
                        r = c.newitem_web(orm.설정_테이블, c.session)
                        c.merge_(o, r)
                        r.group_id = group_id
                        r.issync = None
                        ss.merge(r)
                return 'modified'

    else:
        with orm.session_scope() as ss:  # type:c.typeof_Session
            if c.is_GET():
                gl = c.for_json_l(tablegroup_query(ss, sid).all())
                return c.display(item=c.newitem_web(orm.설정_테이블그룹, c.session),
                                 form_types=form_types, gl=gl, selected=group_id,
                                 TABLEBORDER_WIDTH=c.TABLEBORDER_WIDTH, TABLEBORDER_HEIGHT=c.TABLEBORDER_HEIGHT, )

    c.abort(404)


@app.route('/system/table2', methods=['GET', 'POST'])
def _system_table2():
    shop_id = c.session['store']
    only = c.get_settings(orm, shop_id)

    if c.is_GET():
        if c.is_json():
            return c.jsonify(only.j['테이블'])
        else:
            return c.render_template('system/table2.html',
                                     item=None, form_types=form_types,
                                     TABLEBORDER_WIDTH=c.TABLEBORDER_WIDTH, TABLEBORDER_HEIGHT=c.TABLEBORDER_HEIGHT, )
    elif c.is_POST():
        with orm.session_scope() as ss:  # type:c.typeof_Session
            next_one = c.newitem_web(orm.setting, c.session)
            next_one.j = only.j.copy()
            for each in c.data_POST():
                next_one.j['테이블'] = c.json.loads(each)
            ss.add(next_one)
            return 'modified'
