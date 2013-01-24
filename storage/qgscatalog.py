from geoserver.catalog import Catalog
from geoserver.support import url
from qgslayer import QGSLayer

class QGSCatalog(Catalog):
	def __init__(self, *args, **kwargs):
		super(QGSCatalog, self).__init__(*args, **kwargs)
		self.gs_base_url = self.service_url.rstrip("rest")
		#self.gs_catalog = Catalog(*args, **kwargs)

	def get_layers(self,resource=None):
		"""Get the list of layers from a GeoServer Catalog with some basic metadata

		Return a dictionary of QGSlayers the with layer name as a key"""

		if isinstance(resource, basestring):
			resource = self.get_resources(resource)
		layers_url = url(self.service_url, ["layers.xml"])
		description = self.get_xml(layers_url)
		lyrs = [QGSLayer(self, l.find("name").text) for l in description.findall("layer")]
		if resource is not None:
				lyrs = [l for l in lyrs if l.resource.hrf == resource.href]
		#Transform the list of layers in a dictionnary of layers for ease of use later on
	    #In Python 3 use a dict comprehension instead: layers = {qgs_layer.name:layer for layer in all_layers}
		layers = {}
		for layer in lyrs:
			name = layer.name
			layers[name] = layer
		return layers



