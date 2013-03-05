import requests
import urllib
from lxml import etree
from geoserver.catalog import Catalog
from geoserver.support import url
from qgslayer import QGSLayer

#TODO: here or in gsconfig.py, we should catch the socket.error exception when the url is not accessible


class QGSCatalog(Catalog):
    def __init__(self, *args, **kwargs):
        super(QGSCatalog, self).__init__(*args, **kwargs)
        self.gs_base_url = self.service_url.rstrip("rest")
        #self.gs_catalog = Catalog(*args, **kwargs)

    def get_layers(self, resource=None):
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

    def get_layers_from_capabilities(self):

        wms_getcap_url = self.gs_base_url + "wms?" + urllib.urlencode({
            'version': '1.1.1',
            'request': 'getcapabilities'
        })

        r = requests.get(wms_getcap_url)
        #                 auth=('dmc', 'dmc@123'))
        doc = etree.fromstring(r.content)
        capability = doc.find('Capability')
        svr = capability.find('Layer')

        lyrs = []

        for lyr in svr.findall("Layer"):
            typename = lyr.find('Name')
            if typename is not None:
                typename = typename.text
                #To avoid parsing layer groups
                if ':' not in typename:
                    break
                workspace, name = typename.split(':')
            else:
                typename, workspace = None, None
            title = lyr.find('Title')
            title = title.text if title is not None else None
            abstract = lyr.find('Abstract')
            abstract = abstract.text if abstract is not None else None
            keyword_list_node = lyr.find('KeywordList')
            keyword_list = None
            if len(keyword_list_node):
                keyword_list = [keyword.text for keyword in keyword_list_node.findall("Keyword")]
            lyrs.append(QGSLayer(self, name, workspace, title, abstract, keyword_list))

        layers = {}
        for layer in lyrs:
            name = layer.name
            layers[name] = layer

        return layers
