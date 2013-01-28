import httplib2
import urllib
import requests
import os
import zipfile
import logging
from lxml import etree
from xml.dom import minidom

from geoserver.layer import Layer
from geoserver.support import url
import settings

log = logging.getLogger("geonode-extract")

# Usual logging boilerplate, unnecessary in Python >= 3.1.
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record): pass
log.addHandler(NullHandler())


class QGSLayer(Layer):
    """Class to add some handy attributes and methods the gs_config layer.
    Could be added in gsconfig.py later on"""
    def __init__(self, catalog, name):
        super(QGSLayer, self).__init__(catalog, name)
        self.typename = "%s:%s" % (self.resource.workspace.name, self.resource.name)
        self.title = self.resource.title
        self.abstract = self.resource.abstract
        self.keywords = self.resource.keywords
        #should be added to the Catalog class
        #self.gs_base_url = self.catalog.service_url.rstrip("rest")

    def _get_download_links(self):
        """Returns a list of dictionnary {"extension": , "name": , "mime":, "url":} for downloads of this data
        in various formats."""

        bbox = self.resource.latlon_bbox

        dx = float(bbox[1]) - float(bbox[0])
        dy = float(bbox[3]) - float(bbox[2])

        dataAspect = 1 if dy == 0 else dx / dy

        height = 550
        width = int(height * dataAspect)

        srs = 'EPSG:4326'  # bbox[4] might be None
        bbox_string = ",".join([bbox[0], bbox[2], bbox[1], bbox[3]])

        links = {}
        if self.resource.resource_type == "featureType":
            def wfs_link(mime, extra_params):
                params = {
                    'service': 'WFS',
                    'version': '1.0.0',
                    'request': 'GetFeature',
                    'typename': self.typename,
                    'outputFormat': mime
                }
                params.update(extra_params)
                return self.catalog.gs_base_url + "wfs?" + urllib.urlencode(params)

            types = [
                ("zip", "Zipped Shapefile", "SHAPE-ZIP", {'format_options': 'charset:UTF-8'}),
                ("gml", "GML 2.0", "gml2", {}),
                ("gml", "GML 3.1.1", "text/xml; subtype=gml/3.1.1", {}),
                ("csv", "CSV", "csv", {}),
                ("excel", "Excel", "excel", {}),
                ("json", "GeoJSON", "json", {})
            ]
            for ext, name, mime, extra_params in types:
                links[ext] = {
                    "extension": ext,
                    "name": name,
                    "mime": mime,
                    "url": wfs_link(mime, extra_params)
                }
        elif self.resource.resource_type == "coverage":
            try:
                client = httplib2.Http()
                description_url = self.gs_base_url + "wcs?" + urllib.urlencode({
                        "service": "WCS",
                        "version": "1.0.0",
                        "request": "DescribeCoverage",
                        "coverage": self.typename
                    })
                content = client.request(description_url)[1]
                doc = etree.fromstring(content)
                extent = doc.find(".//%(gml)slimits/%(gml)sGridEnvelope" % {"gml": "{http://www.opengis.net/gml}"})
                low = extent.find("{http://www.opengis.net/gml}low").text.split()
                high = extent.find("{http://www.opengis.net/gml}high").text.split()
                w, h = [int(h) - int(l) for (h, l) in zip(high, low)]

                def wcs_link(mime):
                    return self.catalog.gs_base_url + "wcs?" + urllib.urlencode({
                        "service": "WCS",
                        "version": "1.0.0",
                        "request": "GetCoverage",
                        "CRS": "EPSG:4326",
                        "height": h,
                        "width": w,
                        "coverage": self.typename,
                        "bbox": bbox_string,
                        "format": mime
                    })

                types = [("tiff", "GeoTIFF", "geotiff")]
                for ext, name, mime in types:
                    links[ext] = {"extension": ext, "name": name, "mime": mime, "url": wcs_link(mime)}

            except Exception as e:
                print 'Something is wrong with the WCS:', e
                links['tiff'] = {'extension': "tiff", 'name': "No Tiff", 'url': "#"}

        def wms_link(mime):
            return self.catalog.gs_base_url + "wms?" + urllib.urlencode({
                'service': 'WMS',
                'request': 'GetMap',
                'layers': self.typename,
                'format': mime,
                'height': height,
                'width': width,
                'srs': srs,
                'bbox': bbox_string
            })

        types = [
            ("jpg", "JPEG", "image/jpeg"),
            ("pdf", "PDF", "application/pdf"),
            ("png", "PNG", "image/png")
        ]
        for ext, name, mime in types:
            links[ext] = {
                "extension": ext,
                "name": name,
                "mime": mime,
                "url": wms_link(mime)
            }

        kml_reflector_link_download = self.catalog.gs_base_url + "wms/kml?" + urllib.urlencode({
            'layers': self.typename,
            'mode': "download"
        })

        # kml_reflector_link_view = self.gs_base_url + "wms/kml?" + urllib.urlencode({
        #     'layers': self.typename,
        #     'mode': "refresh"
        # })

        links['KML'] = {'extension': "KML", 'name': "KML", 'mime': "text/xml", 'url': kml_reflector_link_download}
        #links[{'extension': "KML",'name': "View in Google Earth", 'mime': "text/xml", 'url': kml_reflector_link_view})

        return links

    download_links = property(_get_download_links)

    def download(self, dest_dir='downloaded_data'):
        #Dictionnary to store the path of the file downloaded
        file_paths = {'data': None, 'metadata': None, 'style': None}

        links = self.download_links

        # Find out the appropiate download format for this layer
        for f in settings.SUPPORTED_FORMATS:
            if f in links:
                download_format = f
                break
        else:
            msg = 'Only "%s" are supported for the extract, available formats for "%s" are: "%s"' % (
                                             ', '.join(settings.SUPPORTED_FORMATS),
                                             self.name,
                                             ', '.join(links.keys()))
            #log.error(msg)
            raise RuntimeError(msg)

        download_link = links[download_format]['url']
        log.debug('Download link for this layer is "%s"' % download_link)

        try:
            # Download the file
            log.debug('Starting data download for "%s"' % self.name)
            r = requests.get(download_link)
            log.debug('Finished downloading data for "%s"' % self.name)
        except Exception, e:
            log.exception('There was a problem downloading "%s".' % self.name)
            raise e
        else:
            # FIXME(Ariel): This may be dangerous if file is too large.
            content = r.content

            if 'content-disposition' not in r.headers:
                msg = ('Layer "%s" did not have a valid download link "%s"' %
                        (self.name, download_link))
                #log.error(msg)
                raise RuntimeError(msg)

            filename = self.name

            output_dir = os.path.abspath(dest_dir)
            log.info('Getting data from "%s" into "%s"' % (url, output_dir))

            # Create output directory if it does not exist
            if not os.path.isdir(output_dir):
                os.makedirs(dest_dir)

            layer_filename = os.path.join(dest_dir, filename)
            base_filename, extension = os.path.splitext(layer_filename)
            with open(layer_filename, 'wb') as layer_file:
                layer_file.write(content)
                if extension == '.tiff':
                    self.layer_paths['data'] = os.path.abspath(layer_filename)
                log.debug('Saved data from "%s" as "%s"' % (self.name, layer_filename))

        # If this file a zipfile, unpack all files with the same base_filename
        # and remove the downloaded zip
        if zipfile.is_zipfile(layer_filename):
            log.debug('Layer "%s" is zipped, unpacking now' % layer_filename)
            # Create a ZipFile object
            z = zipfile.ZipFile(layer_filename)
            for f in z.namelist():
                log.debug('Found "%s" in "%s"' % (f, layer_filename))
                _, extension = os.path.splitext(f)
                filename = base_filename + extension
                log.debug('Saving "%s" to "%s"' % (f, filename))
                z.extract(f, dest_dir)
                os.rename(os.path.join(dest_dir, f), filename)
                #FIXME(Viv): Needs to be more flexible to take into account different file formats
                if extension == '.shp':
                    file_paths['data'] = os.path.abspath(filename)
            log.debug('Removing "%s" because it is not needed anymore' % layer_filename)
            os.remove(layer_filename)

        #metadata_link = links['xml']['url']
        if self.resource.metadata_links:
        #TODO: manage several metadata links and different types
            metadata_link = self.resource.metadata_links[0][2]

            metadata_filename = base_filename + '.xml'
            try:
                # Download the file
                r = requests.get(metadata_link)
                content = r.content
            except Exception, e:
                log.error('There was a problem downloading "%s": %s' % (self.name, str(e)), e)
                raise e
            else:
                domcontent = minidom.parseString(content)
                gmd_tag = 'gmd:MD_Metadata'
                metadata = domcontent.getElementsByTagName(gmd_tag)

                msg = 'Expected one and only one <%s>' % gmd_tag
                assert len(metadata) == 1, msg

                md_node = metadata[0]

                domcontent.childNodes = [md_node]
                raw_xml = domcontent.toprettyxml().encode('utf-8')

                with open(metadata_filename, 'wb') as metadata_file:
                    metadata_file.write(raw_xml)
                    file_paths['metadata'] = os.path.abspath(metadata_filename)
                    log.debug('Saved metadata from "%s" as "%s"' % (self.name, metadata_filename))

        #style_link = links['sld']['url']
        #TODO: manage alternate styles
        style_filename = base_filename + '.sld'

        try:
            # Get the sld body
            style_data = self.default_style.sld_body
        except Exception, e:
            log.error('There was a problem downloading "%s": %s' % (self.name, str(e)), e)
            raise e
        else:
            xml_style_data = minidom.parseString(style_data)
            pretty_style_data = xml_style_data.toprettyxml().encode('utf-8')

            with open(style_filename, 'wb') as style_file:
                style_file.write(pretty_style_data)
                file_paths['style'] = os.path.abspath(style_filename)
                log.debug('Saved style from "%s" as "%s"' % (self.name, style_filename))

        return file_paths
