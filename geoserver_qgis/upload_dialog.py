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

from projectlayermodel import ProjectLayerModel

import pdb


class UploadDialog(QtGui.QDialog):
    def __init__(self, iface):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_UploadDialog()
        self.ui.setupUi(self)

        self.iface = iface

        myButton = self.ui.pbnUpload
        QtCore.QObject.connect(myButton, QtCore.SIGNAL('clicked()'),
                               self.uploadSelectedLayer)

        #Set up the table view
        layer_list = self.projectLayers()
        self.model = ProjectLayerModel(layer_list)

        self.tableView = self.ui.layerTableView
        self.tableView.setModel(self.model)
        self.resizeColumns()
        self.tableView.setSortingEnabled(True)

    def resizeColumns(self):
        for column in range(3):
            self.tableView.resizeColumnToContents(column)

    def uploadSelectedLayer(self):
        uploaded_layers = []
        qgs_cat = QGSCatalog("http://localhost:8080/geoserver/rest", username="admin", password="geoserver")

        selected_indexes = self.tableView.selectionModel().selection().indexes()

        for index in selected_indexes:
            if index.column() != ProjectLayerModel.NAME:
                continue
            selected_layer_name = str(index.data().toString())
            #Shouldn't require a loop but I didn't find a way to access directly a layer by id or by name
            for lyr in self.iface.mapCanvas().layers():
                if str(lyr.name()) == selected_layer_name:
                    file_path = QtCore.QFileInfo(lyr.dataProvider().dataSourceUri().section('|', 0, 0))
                    #TODO: support sources of data (PostGIS...) by writing the data file first
                    upload_layer_to_gs(qgs_cat, selected_layer_name, str(file_path.absoluteFilePath()))
        return uploaded_layers

    def projectLayers(self):
        canvas = self.iface.mapCanvas()
        all_layers = canvas.layers()
        layer_list = []
        for lyr in all_layers:
            layer_list.append({
                'workspace': '',
                'name': str(lyr.name()),
                'title': '',
                'abstract': '',
                'keywords': ''
            })
        return layer_list
