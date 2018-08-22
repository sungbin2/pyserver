from lxml import etree
from server.main_ import app, orm, c
from flask import json
from flask import Response

def get_config1(store_id):
    only = c.get_settings(orm, store_id)
    return only.j['설정']

def get_config2(orm, store_id):
    with orm.session_scope() as ss:  # type:c.typeof_Session
        only = ss.query(orm.setting) \
            .filter_by(s=store_id) \
            .order_by(ss.desc(orm.setting.i)) \
            .first()
        return c.OBJ_cp(only)

@app.route('/system/conf/<int:sid>', methods=['GET'])
def _system_conf_(sid):
    store_id = sid
    if c.is_GET():
        xml_path = c.os.path.join(c.os.path.dirname(__file__), '../../static/KBIZ_preferences.xml')
        f = open(xml_path, encoding='utf-8')
        tree = etree.parse(f)
        xml_root = tree.getroot()

        form_types = []

        for a in xml_root:
            form_types.append({'name': a.get('name'), 'type': 'divider'})
            for b in a:
                _c = {'tag': None,
                      'name': b.get('key') + c.SEP + b.get('name'),
                      'type': b.get('value'),
                      'valid': None}
                if b.get('value') == 'select':
                    _c['l'] = []
                    for d in b:
                        _c['l'].append(d.get('name'))
                form_types.append(_c)

        return c.display(xml=xml_root, form_types=form_types, item={"no": store_id}, store_id=store_id)



@app.route('/system/data', methods=['GET','POST'])
def _system_data():
    if c.is_GET():
        return c.display()
    else:
        return c.display()


@app.route('/system/data/<int:sid>', methods=['GET'])
def _system_data_(sid):
    store_id = sid
    only1 = get_config2(orm, store_id)

    if c.is_GET():
        if c.is_json():
            response = Response(
                response=json.dumps(only1.j),
                status=200,
                mimetype='text/plain')

            return response
        else:
            return c.display()



@app.route('/system/conf1')
def _system_conf1():
    return c.display()


@app.route('/system/conf1/<int:sid>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def _system_conf1_(sid):
    store_id = sid
    if c.is_GET():
        if c.is_json():
            return c.display(store_id = sid)
        else:
            return c.display(store_id = sid)

    elif c.is_POST():
        print(c.data_POST())
        with orm.session_scope() as ss:  # type:c.typeof_Session
            only = c.get_settings(orm, store_id)
            next_one = c.newitem_web2(orm.setting, store_id)
            next_one.j = only.j.copy()
            for k, v in c.data_POST().items():
                for i in next_one.j['설정']:
                    if k.split(c.SEP, 1)[0] == i:
                        if next_one.j['설정'][i]['v'] != v:
                            next_one.j['설정'][i]['v'] = v
                            print(i,next_one.j['설정'][i])


            ss.add(next_one)

            return 'modified'

    # return 'modified'



@app.route('/system/conf2/<int:sid>', methods=['GET'])
def _system_conf2_(sid):
    store_id = sid

    return c.display(store_id = sid)

@app.route('/system/conf3/<int:sid>', methods=['GET'])
def _system_conf3_(sid):
    store_id = sid

    return c.display(store_id = sid)

@app.route('/system/conf4/<int:sid>', methods=['GET'])
def _system_conf4_(sid):
    store_id = sid

    return c.display(store_id=sid)

@app.route('/system/conf5/<int:sid>', methods=['GET'])
def _system_conf5_(sid):
    store_id = sid

    return c.display(store_id = sid)

@app.route('/system/config1', methods=['GET'])
def _system_config1():
    store_id = 0
    if c.is_GET():
        xml_path = c.os.path.join(c.os.path.dirname(__file__), '../../static/KBIZ_preferences.xml')
        f = open(xml_path, encoding='utf-8')
        tree = etree.parse(f)
        xml_root = tree.getroot()

        form_types = []

        for a in xml_root:
            form_types.append({'name': a.get('name'), 'type': 'divider'})
            for b in a:
                _c = {'tag': None,
                      'name': b.get('key') + c.SEP + b.get('name'),
                      'type': b.get('value'),
                      'valid': None}
                if b.get('value') == 'select':
                    _c['l'] = []
                    for d in b:
                        _c['l'].append(d.get('name'))
                form_types.append(_c)

        return c.display(xml=xml_root, form_types=form_types, item={"no": store_id}, store_id=store_id)


@app.route('/system/config1/<int:store_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def _system_config1_(store_id):
    if c.is_json():
        if c.is_GET():
            d = {k + c.SEP + v['k']: v['v'] for k, v in get_config1(store_id).items()}
            return c.jsonify(d)
        elif c.is_PUT():
            with orm.session_scope() as ss:  # type:c.typeof_Session
                only = c.get_settings(orm, store_id)
                next_one = c.newitem_web2(orm.setting, store_id)
                next_one.j = only.j.copy()

                for k, v in c.data_POST().items():

                    if c.SEP in k and 'checkbox' not in k:
                        _n = k.split(c.SEP, 1)[0]
                        _k = k.split(c.SEP, 1)[1]
                        _v = v
                        next_one.j['설정'][_n] = {'k': _k, 'v': _v}

                ss.add(next_one)
            return 'modified'

    c.abort(404)

@app.route('/system/config2', methods=['GET'])
def _system_config2():
    return c.display()

@app.route('/system/config2/<int:store_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def _system_config2_(store_id):

    if c.is_GET():
        if c.is_json():
            return c.display()
        else:
            return c.display()
    elif c.is_POST():
        if c.is_json():
            with orm.session_scope() as ss:  # type:c.typeof_Session
                only = c.get_settings(orm, store_id)
                next_one = c.newitem_web2(orm.setting, store_id)
                next_one.j = only.j.copy()
                for k, v in c.data_POST().items():
                    print(k,v)
                print(next_one.j['설정'])
                # ss.add(next_one)

                return 'modified'
