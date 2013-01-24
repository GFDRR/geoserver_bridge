# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_geoserver_qgis.ui'
#
# Created: Wed Jan 23 20:13:55 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_GeoserverQGIS(object):
    def setupUi(self, GeoserverQGIS):
        GeoserverQGIS.setObjectName(_fromUtf8("GeoserverQGIS"))
        GeoserverQGIS.resize(484, 107)
        self.pbnDownload = QtGui.QPushButton(GeoserverQGIS)
        self.pbnDownload.setGeometry(QtCore.QRect(20, 60, 161, 26))
        self.pbnDownload.setObjectName(_fromUtf8("pbnDownload"))
        self.pbnDownloadAdd = QtGui.QPushButton(GeoserverQGIS)
        self.pbnDownloadAdd.setGeometry(QtCore.QRect(220, 60, 251, 26))
        self.pbnDownloadAdd.setObjectName(_fromUtf8("pbnDownloadAdd"))

        self.retranslateUi(GeoserverQGIS)
        QtCore.QMetaObject.connectSlotsByName(GeoserverQGIS)

    def retranslateUi(self, GeoserverQGIS):
        GeoserverQGIS.setWindowTitle(QtGui.QApplication.translate("GeoserverQGIS", "GeoserverQGIS", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnDownload.setText(QtGui.QApplication.translate("GeoserverQGIS", "Download the layers", None, QtGui.QApplication.UnicodeUTF8))
        self.pbnDownloadAdd.setText(QtGui.QApplication.translate("GeoserverQGIS", "Download and add to QGIS the layers", None, QtGui.QApplication.UnicodeUTF8))

