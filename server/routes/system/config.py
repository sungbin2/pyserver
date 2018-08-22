from lxml import etree
from server.main_ import app, orm, c
from flask import json
from flask import Response

def get_config(orm, store_id):
    with orm.session_scope() as ss:  # type:c.typeof_Session
        only = ss.query(orm.setting_기능설정) \
            .filter_by(s=store_id) \
            .order_by(ss.desc(orm.setting_기능설정.i)) \
            .first()
        return c.OBJ_cp(only)

@app.route('/system/config', methods=['GET','POST'])
def _system_config():
    store_id = c.session['store']
    if c.is_GET():

        return c.display(store_id=store_id)
    else:
        return c.display(store_id=store_id)

    # return c.redirect(c.url_for('_system_config', store_id=c.session['store']))

@app.route('/system/config/<int:store_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def _system_config_(store_id):
    only1 = get_config(orm, store_id)

    if c.is_GET():
        if c.is_json():
            response = Response(
                response= json.dumps(only1.j),
                status=200,
                mimetype='text/plain')

            return response
        else:
            return c.display()
    elif c.is_POST():
        if c.is_json():
            with orm.session_scope() as ss:  # type:c.typeof_Session
                next_one = c.newitem_web2(orm.setting_기능설정, store_id)
                next_one.j = only1.j.copy()
                for each in c.data_POST():
                    next_one.j = c.json.loads(each)

                ss.add(next_one)
                return 'modified'


@app.route('/system/configfunc/<int:sid>', methods=['GET','POST'])
def _system_configfunc_(sid):
    store_id = sid
    if c.is_GET():

        return c.display(store_id=sid)
    else:
        return c.display(store_id=sid)


@app.route('/system/configcert/<int:sid>', methods=['GET','POST'])
def _system_configcert_(sid):
    store_id = sid
    if c.is_GET():

        return c.display(store_id=sid)
    else:
        return c.display(store_id=sid)