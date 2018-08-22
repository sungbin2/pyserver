# try:
#     from PySide2.QtCore import *
#     from PySide2.QtGui import *
#     from PySide2.QtWidgets import *
#
#     QTLIBRARY = 'PySide2'
#
# except:
if True:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *

    QTLIBRARY = 'PyQt5'

    Signal = pyqtSignal
    Slot = pyqtSlot
