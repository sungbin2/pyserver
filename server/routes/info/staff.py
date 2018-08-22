from server.main_ import app, orm, c
from dateutil import parser
from datetime import datetime, date

def _get_staff():
    with orm.session_scope() as ss:  # type:c.typeof_Session
        q1 = ss.query(orm.정보_가게) \
            .filter_by(id=c.session['store']) \
            .one()
        return c.OBJ_cp(q1)


@app.route('/info/staff', methods=['GET', 'POST'])
def _info_staff():
    if c.is_GET():
        pass
    elif c.is_POST():
        pass
    return c.display()


@app.route('/info/staff/list', methods=['GET'])
def _info_staff_list():
    if c.is_GET():
        if True:  # c.is_json()
            l = []
            with orm.session_scope() as ss:  # type:c.typeof_Session
                q1 = ss.query(orm.정보_직원) \
                    .filter_by(s=c.session['store']) \
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
