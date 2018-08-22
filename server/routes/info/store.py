from server.main_ import app, orm, c
from dateutil import parser
from datetime import datetime, date


def _get_store(store_id):
    with orm.session_scope() as ss:  # type:c.typeof_Session
        only = ss.query(orm.정보_가게) \
            .filter_by(s=store_id) \
            .one()

        return c.OBJ_cp(only)


@app.route('/info/store')
def _info_store():
    return c.display()


@app.route('/info/store1')
def _info_store1():
    return c.display()

@app.route('/info/store2')
def _info_store2():
    return c.display()

@app.route('/info/store3')
def _info_store3():
    return c.display()

@app.route('/info/store4')
def _info_store4():
    return c.display()

@app.route('/info/storelogin')
def _info_storelogin():
    return c.display()

@app.route('/info/store/<int:store_id>', methods=['GET', 'POST', 'PUT'])
def _info_store_(store_id):
    if c.is_GET():
        if c.is_json():
            return c.jsonify(_get_store(store_id).for_json())
        else:
            return c.display()
    # elif c.is_POST() or c.is_PUT():
    #     with orm.session_scope() as ss:  # type:c.typeof_Session
    #         only = ss.query(orm.정보_가게) \
    #             .filter_by(s=store_id) \
    #             .one()
    #         for k, v in c.data_POST().items():
    #             if getattr(only, k) != v:
    #                 print(k, 'is changed')
    #                 if k in ['개점일', '폐점일']:
    #                     try:
    #                         setattr(only, k, parser.parse(v))
    #                     except:
    #                         setattr(only, k, None)
    #                 else:
    #                     setattr(only, k, v)
    #         only.issync = None
    #     return c.display()
    elif c.is_POST():
        with orm.session_scope() as ss:  # type:c.typeof_Session
            print(c.data_POST())
            if c.data_POST()['i'] == '신규':

                only = c.newitem_web3(orm.정보_가게)

                for k, v in c.data_POST().items():
                    if hasattr(only, k)  and k != 'i':
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
                ss.add(only)
                q1 = ss.query(orm.정보_가게) \
                    .order_by(ss.desc(orm.정보_가게.i)) \
                    .first()
                q1.s = q1.i

                only = c.newitem_web2(orm.account , q1.i)
                only.아이디 = q1.i
                only.패스워드 = '15a66be023f335531096a3bb13e2e9a6372656c2caa85b309b4aa8413dbc7'
                ss.add(only)

                only = c.newitem_web2(orm.setting, q1.i)
                q2 = ss.query(orm.setting) \
                        .filter_by(i=0) \
                        .one()
                only.j = q2.j
                ss.add(only)

                only = c.newitem_web2(orm.정보_직원, q1.i)
                only.직원번호 = 1
                only.직원암호 = 1
                only.직원명 = "관리자"
                only.직무 = "대표"
                only.재직상태 = "재직"
                ss.add(only)

                only = c.newitem_web2(orm.setting_기능설정, q1.i)
                q3 = ss.query(orm.setting_기능설정) \
                    .filter_by(i=0) \
                    .one()
                only.j = q3.j
                ss.add(only)

                only = c.newitem_web2(orm.setting_영수증서식, q1.i)
                q4 = ss.query(orm.setting_영수증서식) \
                    .filter_by(i=0) \
                    .one()
                only.j = q4.j
                ss.add(only)

                return 'modified'

            elif c.data_POST()['i'] != '신규':
                only = c.simple_query(ss, orm.정보_가게, s=store_id)

                for x in only:

                    if int(x.i) == int(c.data_POST()['i']):
                        for k, v in c.data_POST().items():
                            if hasattr(x, k) and k != 'i':
                                if getattr(x, k) != v:
                                    print(k, 'is changed')
                                    if k in ['개점일', '폐점일']:
                                        try:
                                            setattr(x, k, parser.parse(v))
                                        except:
                                            setattr(x, k, None)
                                    else:
                                        setattr(x, k, v)
                        x.issync = None
                        return 'modified'

            return 'modified'

@app.route('/info/store/all', methods=['GET', 'POST', 'PUT'])
def _info_store_all():
    if c.is_GET():
        if True:  # c.is_json()
            l = []
            with orm.session_scope() as ss:  # type:c.typeof_Session
                q1 = ss.query(orm.정보_가게) \
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