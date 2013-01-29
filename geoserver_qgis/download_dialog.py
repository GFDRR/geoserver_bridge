"""
Geoserver Geonode QGIS Bridge
A QGS plugin to download and upload data, styles metadata to and from GeoServer

Contact: vivien.deparday@gmail.com

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

from PyQt4 import QtCore, QtGui
from download_dialog_ui import Ui_DownloadDialog

from storage.qgscatalog import QGSCatalog


class DownloadDialog(QtGui.QDialog):
    def __init__(self, iface):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_DownloadDialog()
        self.ui.setupUi(self)

        self.iface = iface

        myButton = self.ui.pbnDownload
        QtCore.QObject.connect(myButton, QtCore.SIGNAL('clicked()'),
                               self.downloadLayers)

        myButton = self.ui.pbnDownloadAdd
        QtCore.QObject.connect(myButton, QtCore.SIGNAL('clicked()'),
                               self.downloadAddLayers)

    def downloadLayers():
        qgs_cat = QGSCatalog("http://localhost:8080/geoserver/rest", username="admin", password="geoserver")
        all_layers = qgs_cat.get_layers()
        all_layers['poi'].download()

    def downloadAddLayers(self):
        qgs_cat = QGSCatalog("http://localhost:8080/geoserver/rest", username="admin", password="geoserver")
        all_layers = qgs_cat.get_layers()

        selected_layer = all_layers['sfdem']
        file_paths = selected_layer.download()
        layer_type = selected_layer.resource.resource_type

        if layer_type == "featureType":
            self.iface.addVectorLayer(file_paths['data'], selected_layer.name, "ogr")
        elif layer_type == "coverage":
            self.iface.addRasterLayer(file_paths['data'], "raster")
