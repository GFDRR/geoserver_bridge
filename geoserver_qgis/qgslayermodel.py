from PyQt4.QtCore import *
from PyQt4.QtGui import *


class QGSLayerModel(QAbstractTableModel):

    WORKSPACE, NAME, TITLE, ABSTRACT, KEYWORDS = range(5)

    def __init__(self, qgslayers):
        super(QGSLayerModel, self).__init__()
        self.qgslayers = qgslayers.values()

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or \
           not (0 <= index.row() < len(self.qgslayers)):
            return QVariant()
        layer = self.qgslayers[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == self.WORKSPACE:
                return QVariant(layer.workspace)
            elif column == self.NAME:
                return QVariant(layer.name)
            elif column == self.TITLE:
                return QVariant(layer.title)
            elif column == self.ABSTRACT:
                return QVariant(layer.abstract)
            elif column == self.KEYWORDS:
                return QVariant("; ".join(layer.keywords))
        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return QVariant(int(Qt.AlignLeft | Qt.AlignVCenter))
            return QVariant(int(Qt.AlignRight | Qt.AlignVCenter))
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            if section == self.WORKSPACE:
                return QVariant("Workspace")
            elif section == self.NAME:
                return QVariant("Name")
            elif section == self.TITLE:
                return QVariant("Title")
            elif section == self.ABSTRACT:
                return QVariant("Abstract")
            elif section == self.KEYWORDS:
                return QVariant("Keywords")
        return QVariant(int(section + 1))

    def rowCount(self, index=QModelIndex()):
        return len(self.qgslayers)

    def columnCount(self, index=QModelIndex()):
        return 5
