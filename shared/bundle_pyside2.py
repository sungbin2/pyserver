from shared.pyside_pyqt import *

from shared.qtw.label import Label
from shared.qtw.button import Button
from shared.qtw.textbox import TextBox
from shared.qtw.intbox import IntBox
from shared.qtw.genderbox import GenderBox
from shared.qtw.birthdaybox import BirthdayBox
from shared.qtw.datepicker import DatePicker
from shared.qtw.daterangepicker import DateRangePicker
from shared.qtw.embedframe import EmbedFrame
from shared.qtw.frame import Frame
from shared.qtw.border import Border
from shared.qtw.gloweddialog import GlowedDialog

from shared.qtw.closebtn import CloseBtn


def setup_layout(l, p, *args, **kwargs) -> QLayout:
    rtn = l()
    p.addLayout(rtn, *args, **kwargs)
    return rtn


def clear_layout(l: QLayout):
    while l.count():
        try:
            l.takeAt(0).widget().deleteLater()
        except:
            pass


def sizer(widget: QWidget, _w=None, _h=None):
    if _w is not None:
        widget.setFixedWidth(_w)
    if _h is not None:
        widget.setFixedHeight(_h)
    sp = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    sp.setHorizontalStretch(0)
    sp.setVerticalStretch(0)
    # sp.setHeightForWidth(w.SizePolicy().hasHeightForWidth())
    widget.setSizePolicy(sp)


def autocreate_form(parent, items, layout_form, lw=None, fw=None, h=None, prefix='w'):
    d = {}
    cnt = 0
    for i in items:
        if type(i) == str:
            _lbl = i
            _name = i.replace(' ', '')
            _type = TextBox()
        elif type(i) == dict:
            _lbl = i['name']
            _name = i['name'].replace(' ', '')
            _type = i['type']()
        else:
            print('autocreate_form: 올바른 값을 입력하십시오,', i)
        _lbl_obj = Label(_s=_lbl, _h_align='r')

        if lw is not None:
            _lbl_obj.setFixedWidth(lw)
        if fw is not None:
            _type.setFixedWidth(fw)
        if h is not None:
            _lbl_obj.setFixedHeight(h)
            _type.setFixedHeight(h)

        layout_form.setWidget(cnt + 1, QFormLayout.LabelRole, _lbl_obj)
        layout_form.setWidget(cnt + 1, QFormLayout.FieldRole, _type)
        setattr(parent, prefix + 'lbl' + _name, _lbl_obj)
        setattr(parent, prefix + _name, _type)
        cnt += 1


def HLine_():
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setFrameShadow(QFrame.Sunken)
    return line
