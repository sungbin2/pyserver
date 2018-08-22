import pprint
from flask import Response
from flask import json

from server.main_ import app, orm, c

pp = pprint.PrettyPrinter(indent=4)

@app.route('/system/receiptform', methods=['GET','POST'])
def _system_receiptform():
    store_id = c.session['store']
    if c.is_GET():

        return c.display(store_id=store_id)
    else:
        return c.display(store_id=store_id)


@app.route('/system/receiptform/<int:store_id>', methods=['GET', 'POST'])
def _system_receiptform_(store_id):
    only = c.get_setting_영수증서식(orm, store_id)

    if c.is_GET():
        if c.is_json():
            response = Response(
                response=json.dumps(only.j),
                status=200,
                mimetype='text/plain')

            return response

        else:
            return c.display()
    elif c.is_POST():
        if c.is_json():
            with orm.session_scope() as ss:  # type:c.typeof_Session
                next_one = c.newitem_web(orm.setting_영수증서식, c.session)
                _j = c.data_json()
                for k in _j:
                    _j[k] = [x for x in _j[k].split(c.EOL) if len(x.strip()) > 0]
                    # pp.pprint(_j)
                next_one.j = only.j.copy()
                k=0

                for i in next_one.j:
                    for j in _j.keys():
                        if i == j:
                            next_one.j[j] = _j[j]
                        k = k + 1
                ss.add(next_one)
                return 'modified'
