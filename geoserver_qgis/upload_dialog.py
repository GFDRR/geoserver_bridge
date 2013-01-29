"""
Geoserver Geonode QGIS Bridge
A QGS plugin to download and upload data, styles metadata to and from GeoServer

Contact: vivien.deparday@gmail.com

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

from PyQt4 import (QtCore,
                   QtGui)
from upload_dialog_ui import Ui_UploadDialog

from storage.qgscatalog import QGSCatalog
from storage.utilities import upload_layer_to_gs


class UploadDialog(QtGui.QDialog):
    def __init__(self, iface):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_UploadDialog()
        self.ui.setupUi(self)

        self.iface = iface

        myButton = self.ui.pbnUpload
        QtCore.QObject.connect(myButton, QtCore.SIGNAL('clicked()'),
                               self.uploadActiveLayer)

    def uploadActiveLayer(self):
        qgs_cat = QGSCatalog("http://localhost:8080/geoserver/rest", username="admin", password="geoserver")

        canvas = self.iface.mapCanvas()
        cLayer = canvas.currentLayer()
        file_path = QtCore.QFileInfo(cLayer.dataProvider().dataSourceUri().section('|', 0, 0))
        layer_name = str(file_path.baseName())

        upload_layer_to_gs(qgs_cat, layer_name, str(file_path.absoluteFilePath()))

    def listWorkspaceLayers(self):
        canvas = self.iface.mapCanvas()
        allLayers = canvas.layers()
        return allLayers
