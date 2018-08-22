import json

from server.main_ import app, orm, c

form_types = [
    {'tag': None, 'name': '메뉴명', 'type': 'select', 'valid': None, },
]


def menugroup_query(ss, sid):
    return ss.query(orm.설정_메뉴그룹) \
        .filter_by(sid=sid) \
        .order_by(ss.asc(orm.설정_메뉴그룹.번호)) \
        .filter_by(isdel=c.X)


def menu_query(ss, sid, group_id):
    return ss.query(orm.설정_메뉴) \
        .filter_by(sid=sid) \
        .filter_by(group_id=group_id) \
        .order_by(ss.asc(orm.설정_메뉴.번호)) \
        .filter_by(isdel=c.X)


@app.route('/system/menu', methods=['GET', ])
def _system_menu_():
    sid = c.session['store']

    with orm.session_scope() as ss:  # type:c.typeof_Session
        if c.is_GET():
            gl = menugroup_query(ss, sid).first()
            return c.redirect(c.url_for('_system_menu', group_id=gl.id))


@app.route('/system/menu/<int:group_id>', methods=['GET', 'PUT', ])
def _system_menu(group_id):
    sid = c.session['store']
    id = c.dict_item(orm, sid)
    il = list(id.values())
    # print(id, il)
    form_types[0]['l'] = il

    if c.is_json():
        if c.is_GET():
            with orm.session_scope() as ss:  # type:c.typeof_Session
                l = c.for_json_l(menu_query(ss, sid, group_id).all())
                for i in l:
                    try:
                        i['메뉴명'] = id[i['품목코드']]
                    except:
                        i['메뉴명'] = '미지정'
                return c.jsonify(l)
        elif c.is_PUT():
            with orm.session_scope() as ss:  # type:c.typeof_Session
                for k, v in c.data_POST().items():
                    ol = json.loads(k)
                    for o in ol:
                        r = c.newitem_web(orm.설정_메뉴, c.session)
                        c.merge_(o, r)
                        r.group_id = group_id
                        try:
                            r.품목코드 = c.fs2i(o['메뉴명'].split('|', 1)[0].strip())
                        except:
                            r.품목코드 = 0
                        r.issync = None
                        ss.merge(r)
                return 'modified'

    else:
        with orm.session_scope() as ss:  # type:c.typeof_Session
            if c.is_GET():
                gl = c.for_json_l(menugroup_query(ss, sid).all())
                _g = [i for i in gl if i['id'] == group_id][0]
                return c.display(item=c.newitem_web(orm.설정_메뉴그룹, c.session),
                                 form_types=form_types, gl=gl, selected=group_id,
                                 상하칸=_g['상하칸'], 좌우칸=_g['좌우칸'],
                                 MENUBORDER_WIDTH=c.MENUBORDER_WIDTH, MENUBORDER_HEIGHT=c.MENUBORDER_HEIGHT, )

    c.abort(404)


@app.route('/system/menu2', methods=['GET', 'POST'])
def _system_menu2():
    shop_id = c.session['store']
    only = c.get_settings(orm, shop_id)

    id = c.dict_item(orm, shop_id)
    il = list(id.values())
    # print(id, il)
    form_types[0]['l'] = il

    if c.is_GET():
        if c.is_json():
            with orm.session_scope() as ss:  # type:c.typeof_Session
                menu2 = ss.query(orm.상품_품목) \
                    .filter_by(s=shop_id) \
                    .filter_by(isdel=c.X) \
                    .all()
                menu2 = c.for_json_l(menu2)
                menu2 = {i['i']: i for i in menu2}
                menu2[0] = {'품목명': '미지정', '단가': 0}
                # print (only.j['메뉴'])
                return c.jsonify(d=only.j['메뉴'], l=menu2)
        else:
            return c.render_template('system/menu2.html',
                                     item=None, form_types=form_types,
                                     MENUBORDER_WIDTH=c.MENUBORDER_WIDTH, MENUBORDER_HEIGHT=c.MENUBORDER_HEIGHT, )
    elif c.is_POST():
        with orm.session_scope() as ss:  # type:c.typeof_Session
            next_one = c.newitem_web(orm.setting, c.session)
            next_one.j = only.j.copy()
            for each in c.data_POST():
                next_one.j['메뉴'] = c.json.loads(each)
            ss.add(next_one)
            return 'modified'
