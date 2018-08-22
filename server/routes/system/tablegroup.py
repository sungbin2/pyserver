from server.main_ import app, orm, c

thead = [
    {'tag': '#', 'name': 'id', 'width': 100, },
    {'tag': None, 'name': '번호', 'width': None, },
    {'tag': '테이블그룹명', 'name': '그룹명', 'width': None, },
]

form_types = [
    {'tag': '테이블그룹명', 'name': '그룹명', 'type': 'input', 'valid': None, },
]


def tablegroup_query(ss, sid):
    return ss.query(orm.설정_테이블그룹) \
        .filter_by(sid=sid) \
        .order_by(ss.asc(orm.설정_테이블그룹.번호)) \
        .filter_by(isdel=c.X)


@app.route('/system/tablegroup', methods=['GET', ])
def _system_tablegroup():
    sid = c.session['store']

    if c.is_GET():
        if c.is_json():
            with orm.session_scope() as ss:  # type:c.typeof_Session
                l = c.for_json_l(tablegroup_query(ss, sid).all())
                return c.jsonify(l)
        return c.display(item=c.newitem_web(orm.설정_테이블그룹, c.session),
                         thead=thead, form_types=form_types, id=sid)


@app.route('/system/tablegroup/<int:_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def _system_tablegroup_(_id):
    sid = c.session['store']

    if c.is_json():
        if c.is_GET():
            with orm.session_scope() as ss:  # type:c.typeof_Session
                r = c.simple_query(ss, orm.설정_테이블그룹, id=_id)
                return c.jsonify(c.for_json(r))
        elif c.is_POST():
            with orm.session_scope() as ss:  # type:c.typeof_Session
                r = c.newitem_web(orm.설정_테이블그룹, c.session)
                cnt = tablegroup_query(ss, sid).count()
                r.번호 = cnt + 1
                for k, v in c.data_POST().items():
                    if hasattr(r, k) and k != 'id':
                        if getattr(r, k) != v:
                            setattr(r, k, v)
                ss.add(r)
                return 'added'
        elif c.is_PUT():
            with orm.session_scope() as ss:  # type:c.typeof_Session
                r = c.simple_query(ss, orm.설정_테이블그룹, id=_id)
                if r.sid == c.session['store']:
                    for k, v in c.data_POST().items():
                        if hasattr(r, k) and k != 'id':
                            if getattr(r, k) != v:
                                print(k, 'is changed')
                                setattr(r, k, v)
                    r.issync = None
                    return 'modified'
                else:
                    c.abort(403)
        elif c.is_DELETE():
            with orm.session_scope() as ss:  # type:c.typeof_Session
                r = c.simple_query(ss, orm.설정_테이블그룹, id=_id)
                if r.sid == c.session['store']:
                    r.isdel = c.O
                    l = tablegroup_query(ss, sid).all()
                    for i in range(len(l)):
                        l[i].번호 = i + 1
                    r.issync = None
                    return 'deleted'
                else:
                    c.abort(403)
    c.abort(404)


@app.route('/system/tablegroup/<int:_id>/moveup', methods=['PUT', ])
def _system_tablegroup_moveup(_id):
    sid = c.session['store']

    if c.is_json():
        if c.is_PUT():
            with orm.session_scope() as ss:  # type:c.typeof_Session
                r = c.simple_query(ss, orm.설정_테이블그룹, id=_id).번호
                l = tablegroup_query(ss, sid).all()
                if sid == c.session['store']:
                    if r <= 1:
                        return 'modified'
                    else:
                        for i in l:
                            if i.번호 == r - 1:
                                i.번호 += 1
                            elif i.번호 == r:
                                i.번호 -= 1
                    return 'modified'
                else:
                    c.abort(403)

    c.abort(404)


@app.route('/system/tablegroup/<int:_id>/movedown', methods=['PUT', ])
def _system_tablegroup_movedown(_id):
    sid = c.session['store']

    if c.is_json():
        if c.is_PUT():
            with orm.session_scope() as ss:  # type:c.typeof_Session
                r = c.simple_query(ss, orm.설정_테이블그룹, id=_id).번호
                l = tablegroup_query(ss, sid).all()
                if sid == c.session['store']:
                    if r >= len(l):
                        return 'modified'
                    else:
                        for i in l:
                            if i.번호 == r:
                                i.번호 += 1
                            elif i.번호 == r + 1:
                                i.번호 -= 1
                    return 'modified'
                else:
                    c.abort(403)

    c.abort(404)
