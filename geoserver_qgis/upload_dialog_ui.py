# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'upload_dialog_ui.ui'
#
# Created: Thu Jan 31 13:54:26 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_UploadDialog(object):
    def setupUi(self, UploadDialog):
        UploadDialog.setObjectName(_fromUtf8("UploadDialog"))
        UploadDialog.resize(318, 68)
        self.pbnUpload = QtGui.QPushButton(UploadDialog)
        self.pbnUpload.setGeometry(QtCore.QRect(20, 20, 281, 26))
        self.pbnUpload.setObjectName(_fromUtf8("pbnUpload"))

        self.retranslateUi(UploadDialog)
        QtCore.QMetaObject.connectSlotsByName(UploadDialog)

    def retranslateUi(self, UploadDialog):
        UploadDialog.setWindowTitle(QtGui.QApplication.translate("UploadDialog", "GeoServer Bridge - Upload layers", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnUpload.setText(QtGui.QApplication.translate("UploadDialog", "Upload the active layer to GeoServer", None, QtGui.QApplication.UnicodeUTF8))

