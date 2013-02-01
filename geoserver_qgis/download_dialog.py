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
from qgslayermodel import QGSLayerModel


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

        #Set up the tree view
        qgs_cat = QGSCatalog("http://localhost:8080/geoserver/rest", username="admin", password="geoserver")
        self.all_layers = qgs_cat.get_layers()
        self.model = QGSLayerModel(self.all_layers)

        self.tableView = self.ui.layerTreeView
        self.tableView.setModel(self.model)
        #header = self.tableView.horizontalHeader()
        #self.connect(header, SIGNAL("sectionClicked(int)"),
        #                 self.sortTable)

    def sortTable(self, section):
        pass

    def downloadLayers(self):
        downloaded_layers = []
        selected_indexes = self.tableView.selectionModel().selection().indexes()
        for index in selected_indexes:
            if index.column() != QGSLayerModel.NAME:
                continue
            selected_layer_name = str(index.data().toString())
            selected_layer = self.all_layers[selected_layer_name]
            selected_layer.download()
            downloaded_layers.append(selected_layer)
        return downloaded_layers

    def AddLayers(self, layer_list):
        for layer in layer_list:
            layer_type = layer.resource.resource_type
            if layer_type == "featureType":
                self.iface.addVectorLayer(layer.file_paths['data'], layer.name, "ogr")
            elif layer_type == "coverage":
                self.iface.addRasterLayer(layer.file_paths['data'], "raster")

    def downloadAddLayers(self):
        downloaded_layers = self.downloadLayers()
        self.AddLayers(downloaded_layers)
