from shared.commons import *
from contextlib import contextmanager

from sqlalchemy import create_engine, func, asc, desc
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session as _typeof_Session_
from sqlalchemy.orm.attributes import flag_modified

typeof_Session = _typeof_Session_


class ORM(object):
    def __init__(self, dialect, con_dict, tbln_list=None):

        if dialect == 'sqlite':
            self.connectionstring = 'sqlite+pysqlite:///{0}'.format(con_dict['file'], )
            tblnq = """SELECT name FROM sqlite_master WHERE type='table'"""

        elif dialect == 'fdb':
            self.connectionstring = 'firebird+fdb://{0}:{1}@{2}:{3}/{4}'.format(
                con_dict['user'],
                con_dict['password'],
                con_dict['host'],
                con_dict['port'],
                con_dict['file'],
            )
            tblnq = """select rdb$relation_name from rdb$relations where rdb$view_blr is null and (rdb$system_flag is null or rdb$system_flag = 0);"""

        elif dialect == 'postgresql':
            self.connectionstring = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(
                con_dict['user'],
                con_dict['password'],
                con_dict['host'],
                con_dict['port'],
                con_dict['db'],
            )
            tblnq = """SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"""

        self.engine = create_engine(self.connectionstring, echo=False)

        self.Base = declarative_base(cls=DeferredReflection)

        if tbln_list is None:
            tblnq_r = self.engine.execute(tblnq)
            tblnq_r_l = tblnq_r.fetchall()
            tbln_list = []

            for n in tblnq_r_l:
                tbln_list.append(n[0].strip())

        for tbln in tbln_list:
            setattr(self, tbln, type(tbln, (self.Base,), {'__tablename__': tbln}))

        self.Base.prepare(self.engine)

        self.Session = sessionmaker(bind=self.engine)

        self.tbln_list_ = tbln_list

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.Session()
        session.func = func
        session.asc = asc
        session.desc = desc
        session.flag_modified = flag_modified

        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()


# def run_my_program():
#     with session_scope() as session:
#         ThingOne().go(session)
#         ThingTwo().go(session)

#
# def newitem_web(obj_type, sess):
#     o = obj_type()
#     o.s = sess['store']
#     o.isdel = X
#     o.issync = None
#     return o

def newitem_web(obj_type, sess):
    _now = now_()
    o = obj_type()
    o.s = sess['store']
    o.ct = _now
    o.et = _now
    o.j = {}
    o.isdel = X
    o.issync = None
    return o

def newitem_web2(obj_type, sess):
    _now = now_()
    o = obj_type()
    o.s = sess
    o.ct = _now
    o.et = _now
    o.j = {}
    o.isdel = X
    o.issync = None
    return o

def newitem_web3(obj_type):
    _now = now_()
    o = obj_type()
    o.ct = _now
    o.et = _now
    o.j = {}
    o.isdel = X
    o.issync = None
    return o

def newitem_web1(obj_type, sess):
    _now = now_()
    o = obj_type()
    o.s = sess['store']
    o.isdel = X
    o.issync = _now
    o.func = {}
    return o

# def newitem_pos(obj_type, sess):
#     o = newitem_web(obj_type, sess)
#     o.eid = sess['eid']
#     return o


def simple_query(ss, obj_type, no=None, s=None, order_by_asc=None, order_by_desc=None, ):
    o = ss.query(obj_type)
    if no:
        o = o.filter_by(no=no).filter_by(isdel=X).one()
    else:
        if s:
            o = o.filter_by(s=s)
        if order_by_asc == 'no':
            o = o.order_by(ss.asc(obj_type.no))
        o = o.filter_by(isdel=X).all()

    return o





def for_json(query_one):
    temp = query_one.__dict__.copy()
    if '_sa_instance_state' in temp:
        del temp['_sa_instance_state']
    return temp


def for_json_l(query_all):
    temp = []
    for each in query_all:
        temp.append(for_json(each))
    return temp


def for_json2(query_one):
    temp = query_one.__dict__.copy()
    if '_sa_instance_state' in temp:
        del temp['_sa_instance_state']
    for k in temp:
        if isinstance(temp[k], datetime.datetime):
            temp[k] = str(temp[k])
        elif isinstance(temp[k], datetime.date):
            temp[k] = str(temp[k])
    return temp


def for_json_l2(query_all):
    temp = []
    for each in query_all:
        temp.append(for_json2(each))
    return temp
