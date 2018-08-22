from server.main_ import app, orm, c

thead = [
    {'tag': '#', 'name': 'idx', 'width': 40, },
    {'tag': None, 'name': '프린터명', 'width': 90, },
    {'tag': None, 'name': '모델명', 'width': 70, },
    {'tag': None, 'name': '연결기기명', 'width': 110, },
    {'tag': None, 'name': '통신포트', 'width': 80, },
    {'tag': None, 'name': '통신속도', 'width': 80, },
    {'tag': None, 'name': '영수증', 'width': 80, },
    {'tag': None, 'name': '고객주문서', 'width': 110, },
    {'tag': None, 'name': '주방주문서', 'width': 110, },
]
form_types = [
    {'tag': None, 'name': '프린터명', 'type': 'input', 'valid': None, },
    {'tag': None, 'name': '모델명', 'type': 'select', 'l': c.PRINTER_MODEL, 'valid': None, },
    {'tag': None, 'name': '연결기기명', 'type': 'select', 'l': [], 'valid': None, },
    {'tag': None, 'name': '통신포트', 'type': 'select', 'l': c.COM_PORT, 'valid': None, },
    {'tag': None, 'name': '통신속도', 'type': 'select', 'l': c.COM_BAUDRATE, 'valid': None, },
    {'tag': None, 'name': '영수증', 'type': 'checkbox', 'valid': None, },
    {'tag': None, 'name': '고객주문서', 'type': 'checkbox', 'valid': None, },
    {'tag': None, 'name': '주방주문서', 'type': 'checkbox', 'valid': None, },
]

@app.route('/system/printer', methods=['GET'])
def _system_printer():

    return '0'

@app.route('/system/printer/<int:sid>', methods=['GET', 'POST'])
def _system_printer_(sid):
    store_id = sid
    only = c.get_settings(orm, store_id)
    available_networks = []
    networks = only.j['네트워크']
    adjusted = only.j['프린터']
    for each in networks:
        if each['enabled']:
            available_networks.append(each['기기명'])
    for each in adjusted:
        each['연결기기명'] = networks[each['network_id']]['기기명']
    for each in form_types:
        if each['name'] == '연결기기명':
            each['l'] = available_networks

    if c.is_GET():
        if c.is_json():
            return c.jsonify(adjusted)
        else:
            return c.display(thead=thead, form_types=form_types,store_id=sid,
                             defnet=available_networks[0]
                             if len(available_networks) > 0
                             else '')
    elif c.is_POST():
        with orm.session_scope() as ss:  # type:c.typeof_Session
            next_one = c.newitem_web2(orm.setting, sid)
            next_one.j = only.j.copy()
            for each in c.data_POST():
                next_one.j['프린터'] = c.json.loads(each)
            for each in next_one.j['프린터']:
                for i in range(len(networks)):
                    if each['연결기기명'] == networks[i]['기기명']:
                        each['network_id'] = i
            ss.add(next_one)
            return 'modified'
