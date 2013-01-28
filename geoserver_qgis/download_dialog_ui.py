# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'download_dialog_ui.ui'
#
# Created: Mon Jan 28 12:25:43 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DownloadDialog(object):
    def setupUi(self, DownloadDialog):
        DownloadDialog.setObjectName(_fromUtf8("DownloadDialog"))
        DownloadDialog.resize(487, 99)
        self.pbnDownload = QtGui.QPushButton(DownloadDialog)
        self.pbnDownload.setGeometry(QtCore.QRect(20, 40, 161, 26))
        self.pbnDownload.setObjectName(_fromUtf8("pbnDownload"))
        self.pbnDownloadAdd = QtGui.QPushButton(DownloadDialog)
        self.pbnDownloadAdd.setGeometry(QtCore.QRect(220, 40, 251, 26))
        self.pbnDownloadAdd.setObjectName(_fromUtf8("pbnDownloadAdd"))

        self.retranslateUi(DownloadDialog)
        QtCore.QMetaObject.connectSlotsByName(DownloadDialog)

    def retranslateUi(self, DownloadDialog):
        DownloadDialog.setWindowTitle(QtGui.QApplication.translate("DownloadDialog", "GeoserverQGIS", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnDownload.setText(QtGui.QApplication.translate("DownloadDialog", "Download the layers", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnDownloadAdd.setText(QtGui.QApplication.translate("DownloadDialog", "Download and add to QGIS the layers", None, QtGui.QApplication.UnicodeUTF8))

