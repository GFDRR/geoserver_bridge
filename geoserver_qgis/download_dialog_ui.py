# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'download_dialog_ui.ui'
#
# Created: Thu Jan 31 14:01:08 2013
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
        DownloadDialog.resize(591, 273)
        self.gridLayout = QtGui.QGridLayout(DownloadDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pbnDownload = QtGui.QPushButton(DownloadDialog)
        self.pbnDownload.setObjectName(_fromUtf8("pbnDownload"))
        self.gridLayout.addWidget(self.pbnDownload, 2, 0, 1, 1)
        self.pbnDownloadAdd = QtGui.QPushButton(DownloadDialog)
        self.pbnDownloadAdd.setObjectName(_fromUtf8("pbnDownloadAdd"))
        self.gridLayout.addWidget(self.pbnDownloadAdd, 2, 1, 1, 1)
        self.layerTreeView = QtGui.QTableView(DownloadDialog)
        self.layerTreeView.setObjectName(_fromUtf8("layerTreeView"))
        self.gridLayout.addWidget(self.layerTreeView, 0, 0, 1, 2)

        self.retranslateUi(DownloadDialog)
        QtCore.QMetaObject.connectSlotsByName(DownloadDialog)

    def retranslateUi(self, DownloadDialog):
        DownloadDialog.setWindowTitle(QtGui.QApplication.translate("DownloadDialog", "GeoServer Bridge - Download layers", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnDownload.setText(QtGui.QApplication.translate("DownloadDialog", "Download the layers", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnDownloadAdd.setText(QtGui.QApplication.translate("DownloadDialog", "Download and add to QGIS the layers", None, QtGui.QApplication.UnicodeUTF8))

