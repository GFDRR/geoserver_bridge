# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'upload_dialog_ui.ui'
#
# Created: Sun Feb  3 13:58:59 2013
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
        UploadDialog.resize(708, 338)
        self.gridLayout = QtGui.QGridLayout(UploadDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pbnUpload = QtGui.QPushButton(UploadDialog)
        self.pbnUpload.setObjectName(_fromUtf8("pbnUpload"))
        self.gridLayout.addWidget(self.pbnUpload, 1, 0, 1, 1)
        self.layerTableView = QtGui.QTableView(UploadDialog)
        self.layerTableView.setObjectName(_fromUtf8("layerTableView"))
        self.gridLayout.addWidget(self.layerTableView, 0, 0, 1, 1)

        self.retranslateUi(UploadDialog)
        QtCore.QMetaObject.connectSlotsByName(UploadDialog)

    def retranslateUi(self, UploadDialog):
        UploadDialog.setWindowTitle(QtGui.QApplication.translate("UploadDialog", "GeoServer Bridge - Upload layers", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnUpload.setText(QtGui.QApplication.translate("UploadDialog", "Upload the selected layers to GeoServer", None, QtGui.QApplication.UnicodeUTF8))

