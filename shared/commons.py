import datetime
import os
import socket
import sys
from pyblake2 import blake2b


TABLEBORDER_WIDTH = 800
TABLEBORDER_HEIGHT = 580
MENUBORDER_WIDTH = 480
MENUBORDER_HEIGHT = 470

# DEFPORT_DB = 8520
DEFPORT_DB = 55432
DEFPORT_HTTPD = 8521

# EOL = '\r\n'
EOL = '\n'


VAT = 0.1
O = 'O'
X = 'X'
SEP = ' | '
COM_PORT = ['COM01', 'COM02', 'COM03', 'COM04', 'COM05', 'COM06', 'COM07', 'COM08', 'COM09', 'COM10',
            'COM11', 'COM12', 'COM13', 'COM14', 'COM15', 'COM16', 'COM17', 'COM18', 'COM19', 'COM20', ]
COM_BAUDRATE = ['4800', '9600', '19200', '38400', '57600', '115200', '230400', ]
PRINTER_MODEL = ['기본', 'IBM 4610-1NR']



class OBJ(object):
    def __init__(self, d={}):
        if d != {}:
            self.__dict__ = d


class OBJ_cp(object):
    def __init__(self, o):
        temp = o.__dict__.copy()
        if '_sa_instance_state' in temp:
            del temp['_sa_instance_state']
        self.__dict__ = temp
        self.o_type = type(o)

    def for_json(self):
        temp = self.__dict__.copy()
        if '_sa_instance_state' in temp:
            del temp['_sa_instance_state']
        if 'o_type' in temp:
            del temp['o_type']
        return temp


def pw_hash(pw: str) -> str:
    h = blake2b(digest_size=30)
    h.update(pw.encode())
    return str(len(pw)) + h.hexdigest()


def here(var):
    return var is not None


def nohere(var):
    return var is None



def app_exit():
    sys.exit()


def app_rerun():
    os.execl(sys.executable, sys.executable, *sys.argv)


def now_():
    return datetime.datetime.now()


def today_():
    return datetime.datetime.today()


def merge_(src, dst):
    if type(src) is dict:
        temp = src.copy()
    else:
        temp = src.__dict__.copy()

    if '_sa_instance_state' in temp:
        del temp['_sa_instance_state']
    for k, v in temp.items():
        setattr(dst, k, v)


def get_localip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    return s.getsockname()[0]


def get_fullpath(f, s):
    return os.path.join(os.path.dirname(f), s)


def vat_calc(amt, 부가세과세, 부가세포함):
    rtn = {'합계': 0, '공급가': 0, '세금': 0, '과세금액': 0, '면세금액': 0, }
    if 부가세과세 == O:
        if 부가세포함 == O:
            rtn['공급가'] = round(amt / (1 + VAT))
            rtn['세금'] = amt - round(amt / (1 + VAT))
            rtn['과세금액'] = amt
        elif 부가세포함 == X:
            rtn['공급가'] = amt
            rtn['세금'] = amt * VAT
            rtn['과세금액'] = amt + (amt * VAT)
    elif 부가세과세 == X:
        rtn['면세금액'] = amt

    rtn['공급가'] = int(rtn['공급가'])
    rtn['세금'] = int(rtn['세금'])
    rtn['과세금액'] = int(rtn['과세금액'])

    rtn['합계'] = rtn['과세금액'] + rtn['면세금액']
    return rtn


def get_settings(orm, store_id):
    with orm.session_scope() as ss:  # type:c.typeof_Session
        only = ss.query(orm.setting) \
            .filter_by(s=store_id) \
            .filter_by(isdel=X) \
            .order_by(ss.desc(orm.setting.i)) \
            .first()

        return OBJ_cp(only)
    
def get_settings1(orm, store_id):
    with orm.session_scope() as ss:  # type:c.typeof_Session
        only = ss.query(orm.기능설정) \
            .filter_by(s=store_id) \
            .order_by(ss.desc(orm.기능설정.no)) \
            .first()
        return OBJ_cp(only)



def get_setting_영수증서식(orm, shop_id):
    with orm.session_scope() as ss:  # type:c.typeof_Session
        only = ss.query(orm.setting_영수증서식) \
            .filter_by(s=shop_id) \
            .filter_by(isdel=X) \
            .order_by(ss.desc(orm.setting_영수증서식.i)) \
            .first()
        return OBJ_cp(only)
