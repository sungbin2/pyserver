from flask import Flask
from server import shared_lib

c = shared_lib

# create our little application :)
app = Flask(__name__)
app.secret_key = 'KBIZPOS'
app.debug = True

orm = c.ORM('postgresql',
            {
                'user': 'postgres',
                'password': '13a0a8e64e00c2cdd96ee6181b7bbd8627e97b50519320bb7b8ac81ed15957',
                'host': '175.194.100.73',
                'port': '55432',
                'db': 'modernpos',
            })

import server.routes.login.login
import server.routes.dashboard.dashboard
import server.routes.info.store
import server.routes.info.storepwd
import server.routes.dashboard.window
import server.routes.dashboard.weather
import server.routes.dashboard.mobile

import server.routes.info.staff
import server.routes.info.staff1
import server.routes.system.network
import server.routes.system.printer
import server.routes.system.config
import server.routes.system.config1
import server.routes.system.receiptform


import server.routes.board.board

free_for_all = [
    '_login',
    '_getsession',
	'_autosession',
]


@app.before_request
def before_request():
    c.session['current_menu'] = c.request.path.replace('/', '_')
    print('c.current_menu is updated: ', c.session['current_menu'])

    FREE_FOR_ALL = []
    for x in free_for_all:
        FREE_FOR_ALL.append(c.url_for(x))

    if 'logged_in' in c.session and c.session['logged_in'] is True:
        pass
    elif '_static' in c.session['current_menu']:
        pass
    elif c.request.path not in FREE_FOR_ALL:
        return c.redirect(c.url_for('_login'))


@app.route('/getsession', methods=['POST'])
def _getsession():
    if c.is_POST():
        with orm.session_scope() as ss:  # type:c.typeof_Session
            rtn = 'SUCCESS'
            id = c.data_POST('id')
            pw = c.data_POST('pw')

            account = ss.query(orm.계정) \
                .filter_by(아이디=id) \
                .filter_by(패스워드=pw) \
                .first()
            if account is None:
                rtn = 'FAILED'
            else:
                c.account_session(orm, account, c.session)
            return rtn

@app.route('/autosession', methods=['GET'])
def _autosession():
    if c.is_GET():
        with orm.session_scope() as ss:  # type:c.typeof_Session
            rtn = 'SUCCESS'
            d = c.data_GET()
            ip = c.request.remote_addr
            print(ip)
            print(d)
            id = d['id']
            pw = d['pw']

            account = ss.query(orm.account) \
                .filter_by(아이디=id) \
                .first()
            if account is None:
                rtn = 'FAILED'
            elif account is None:
                rtn = 'FAILED'
            else:
                c.account_session(orm, account, c.session)
                return c.redirect(c.url_for('_dashboard'))
            return rtn

def make_line(tbl, entire):
    with orm.session_scope() as ss:  # type:c.typeof_Session
        l = ss.query(tbl)
        if tbl == orm.정보_가게:
            l = l.filter_by(no=c.session['store'])
        else:
            l = l.filter_by(s=c.session['store'])
        l = l.all() if entire else l.filter_by(issync=None).all()
        return c.for_json_l(l)


@app.route('/downloaddb', methods=['GET', 'POST'])
def _downloaddb():
    if c.is_GET():
        with orm.session_scope() as ss:  # type:c.typeof_Session
            opt = True if 'entire' in c.data_GET() else False
            d = {}
            for tn in orm.tbln_list_:
                _l = tn.split('_')
                if _l[0] in ['settings', '정보', '상품']:
                    d[tn] = make_line(getattr(orm, tn), opt)
            cnt = 0
            for val in d.values():
                cnt += len(val)
            d['cnt'] = cnt
            history = c.newitem_web(orm.히스토리_동기화_설정, c.session)
            history.발생시점 = c.now_()
            history.항목수 = cnt
            ss.add(history)
            return c.jsonify(d)
    elif c.is_POST():
        with orm.session_scope() as ss:  # type:c.typeof_Session
            rtn = 'SUCCESS'
            cnt_ = int(c.data_POST('cnt_'))

            q1 = ss.query(orm.히스토리_동기화_설정) \
                .filter_by(s=c.session['store']) \
                .order_by(ss.desc(orm.히스토리_동기화_설정.발생시점)) \
                .first()
            if q1.항목수 != cnt_:
                rtn = 'FAILED'
            else:
                d = {}
                for tn in orm.tbln_list_:
                    _l = tn.split('_')
                    if _l[0] in ['settings', '정보', '상품']:
                        d[tn] = make_line(getattr(orm, tn), False)
                cnt = 0
                now_ = c.now_()
                for k, v in d.items():
                    for item in v:
                        _o = getattr(orm, k)(**item)
                        _o.issync = now_
                        ss.merge(_o)
                        cnt += 1
                if cnt != cnt_:
                    rtn = 'DIFFERENT'

            return rtn


@app.route('/uploaddb', methods=['GET', 'POST'])
def _uploaddb():
    if c.is_GET():
        pass
    elif c.is_POST():
        with orm.session_scope() as ss:  # type:c.typeof_Session
            rtn = 'SUCCESS'
            jo = c.data_json()

            cnt = jo['cnt']
            cnt_ = 0
            del jo['cnt']

            for jk in jo:
                for jl in jo[jk]:
                    # try:
                    #     _o = getattr(c.orm, jk)(**jl)
                    #     ss.merge(_o)
                    #     cnt_ += 1
                    # except Exception as err:
                    #     pass
                    _o = getattr(orm, jk)(**jl)
                    ss.merge(_o)
                    cnt_ += 1

            print('SYNC_ITEM: received', cnt)
            print('SYNC_ITEM: saved', cnt_)

            if cnt != cnt_:
                rtn = 'DIFFERENT'

            return rtn


