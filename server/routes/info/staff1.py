from server.main_ import app, orm, c
from dateutil import parser
from datetime import datetime, date


@app.route('/info/staff1', methods=['GET'])
def _info_staff1():
    store_id = c.session['store']
    if c.is_GET():

        return c.display(store_id=store_id)
    else:
        return c.display(store_id=store_id)





@app.route('/info/staff1/<int:_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def _info_staff1_(_id):
    store_id = c.session['store']
    if c.is_GET():
        if True:  # c.is_json()
            l = []
            with orm.session_scope() as ss:  # type:c.typeof_Session
                q1 = ss.query(orm.정보_직원) \
                    .filter_by(s=store_id) \
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

    elif c.is_POST():
        with orm.session_scope() as ss:  # type:c.typeof_Session
            print(c.data_POST())
            if c.data_POST()['i'] == '신규':

                only = c.newitem_web(orm.정보_직원, c.session)
                for k, v in c.data_POST().items():
                    if hasattr(only, k) and k != 'i':
                        if getattr(only, k) != v:
                            setattr(only, k, v)

                ss.add(only)
                return 'modified'

            elif c.data_POST()['i'] != '신규':
                only = c.simple_query(ss, orm.정보_직원, s=c.session['store'])

                for x in only:

                    if int(x.i) == int(c.data_POST()['i']):
                        for k, v in c.data_POST().items():
                            if hasattr(x, k) and k != 'i':
                                if getattr(x, k) != v:
                                    print(k, 'is changed')
                                    setattr(x, k, v)
                        x.issync = None
                        return 'modified'

            return 'modified'