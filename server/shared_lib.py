from shared.commons import *
from shared.bundle_str import *
from shared.bundle_sqlalchemy import *
from shared.bundle_flask import *


def account_session(orm, account, session):
    with orm.session_scope() as ss:  # type:c.typeof_Session
        session['logged_in'] = True
        session['아이디'] = account.아이디
        session['store'] = account.s
        session['가게명'] = ss.query(orm.정보_가게.가게명).filter_by(i=account.s).first()


def dict_itemgroup(orm, store_id):
    with orm.session_scope() as ss:  # type:c.typeof_Session
        l = ss.query(orm.상품_분류) \
            .filter_by(s=store_id) \
            .order_by(ss.asc(orm.상품_분류.분류명)) \
            .filter_by(isdel=X) \
            .all()

        d = {i.i: '{0}|{1}'.format(i.i, i.분류명) for i in l}
        return d


def dict_item(orm, store_id):
    with orm.session_scope() as ss:  # type:c.typeof_Session
        l = ss.query(orm.상품_품목) \
            .filter_by(s=store_id) \
            .order_by(ss.asc(orm.상품_품목.품목명)) \
            .filter_by(isdel=X) \
            .all()

        d = {i.i: '{0}|{1}'.format(i.i, i.품목명) for i in l}
        return d
