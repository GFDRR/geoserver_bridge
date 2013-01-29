"""**Utilities for storage module**
"""

import os
import re
import glob
#import errno
#import logging
#logger = logging.getLogger('geoserver_qgis.utilities')

from geoserver.resource import FeatureType, Coverage
from storage.qgslayer import QGSLayer
import geoserver


def write_sld_file():
    pass


def write_metadata_file():
    #TODO: Management of .keywords inaSafe files
    pass


def export(layer):
    pass


def upload_layer_to_gs(catalog, layer_name, base_file, overwrite=True, title=None,
         abstract=None, permissions=None, keywords=()):
    """Upload layer data to Geoserver.

       If specified, the layer given is overwritten, otherwise a new layer
       is created.
    """
    #TODO: validation of the name
    #TODO: in case the name already exist, prompt user to ask for overwrite
    #TODO: manage PostGIS datastore type

    #logger.info(_separator)
    #logger.info('Uploading layer: [%s], base filename: [%s]', layer, base_file)

    # Step 0. Verify the file exists
    #logger.info('>>> Step 0. Verify if the file %s exists so we can create '
    #            'the layer [%s]' % (base_file, layer))
    if not os.path.exists(base_file):
        msg = ('Could not open %s to save %s. Make sure you are using a '
               'valid file' % (base_file, layer_name))
        #logger.warn(msg)
        raise Exception(msg)

    # Step 1. Figure out the name for the new layer, the one passed might not
    # be valid or being used, if it already exist prompt for overwrite
    name = layer_name

    # Step 2. If a store already exist with the same name
    #check that it is uploading to the same resource type as the existing resource

    # Step 3. Identify whether it is vector or raster and which extra files
    # are needed.

    #logger.info('>>> Step 3. Identifying if [%s] is vector or raster and '
    #            'gathering extra files', name)
    the_layer_type = layer_type(base_file)
    if the_layer_type == FeatureType.resource_type:
        #logger.debug('Uploading vector layer: [%s]', base_file)
        #if settings.DB_DATASTORE:
        #    create_store_and_resource = _create_db_featurestore
        #else:
        create_store_and_resource = create_featurestore
    elif the_layer_type == Coverage.resource_type:
        #logger.debug("Uploading raster layer: [%s]", base_file)
        create_store_and_resource = create_coveragestore
    else:
        msg = ('The layer type for name %s is %s. It should be '
               '%s or %s,' % (layer_name,
                              the_layer_type,
                              FeatureType.resource_type,
                              Coverage.resource_type))
        #logger.warn(msg)
        raise Exception(msg)

    # Step 4. Create the store in GeoServer
    #logger.info('>>> Step 4. Starting upload of [%s] to GeoServer...', name)

    # Get the helper files if they exist
    files = get_files(base_file)

    data = files

    #FIXME: DONT DO THIS
    #-------------------
    if 'shp' not in files:
        main_file = files['base']
        data = main_file
    # ------------------

    try:
        store, gs_resource = create_store_and_resource(catalog,
                                                       name,
                                                       data,
                                                       overwrite=overwrite)
    except geoserver.catalog.UploadError, e:
        msg = ('Could not save the layer %s, there was an upload '
               'error: %s' % (name, str(e)))
        #logger.warn(msg)
        e.args = (msg,)
        raise
    except geoserver.catalog.ConflictingDataError, e:
        # A datastore of this name already exists
        msg = ('GeoServer reported a conflict creating a store with name %s: '
               '"%s". This should never happen because a brand new name '
               'should have been generated. But since it happened, '
               'try renaming the file or deleting the store in '
               'GeoServer.' % (name, str(e)))
        #logger.warn(msg)
        e.args = (msg,)
        raise
    else:
        pass
        #logger.debug('Finished upload of [%s] to GeoServer without '
        #             'errors.', name)

    # Step 5. Create the resource in GeoServer
    #logger.info('>>> Step 5. Generating the metadata for [%s] after '
    #            'successful import to GeoSever', name)

    # Verify the resource was created
    if gs_resource is not None:
        assert gs_resource.name == name
    else:
        msg = ('GeoNode encounterd problems when creating layer %s.'
               'It cannot find the Layer that matches this Workspace.'
               'try renaming your files.' % name)
        #logger.warn(msg)
        raise Exception(msg)

    # Step 6. Make sure our data always has a valid projection
    # FIXME: Put this in gsconfig.py
    #logger.info('>>> Step 6. Making sure [%s] has a valid projection' % name)

    if gs_resource.latlon_bbox is None:
        box = gs_resource.native_bbox[:4]
        minx, maxx, miny, maxy = [float(a) for a in box]
        if -180 <= minx <= 180 and -180 <= maxx <= 180 and \
           -90 <= miny <= 90 and -90 <= maxy <= 90:
            #logger.info('GeoServer failed to detect the projection for layer '
            #            '[%s]. Guessing EPSG:4326', name)
            # If GeoServer couldn't figure out the projection, we just
            # assume it's lat/lon to avoid a bad GeoServer configuration

            gs_resource.latlon_bbox = gs_resource.native_bbox
            gs_resource.projection = "EPSG:4326"
            catalog.save(gs_resource)
        else:
            msg = ('GeoServer failed to detect the projection for layer '
                   '[%s]. It doesn\'t look like EPSG:4326, so backing out '
                   'the layer.')
    #       logger.info(msg, name)
    #        cascading_delete(layer.catalog, name)
            raise Exception(msg % name)

    # Step 7. Create the style and assign it to the created resource
    # FIXME: Put this in gsconfig.py
    #logger.info('>>> Step 7. Creating style for [%s]' % name)
    publishing = catalog.get_layer(name)

    if 'sld' in files:
        f = open(files['sld'], 'r')
        sld = f.read()
        f.close()
    else:
    #   sld = get_sld_for(publishing)
        sld = None

    if sld is not None:
        try:
            catalog.create_style(name, sld)
        except geoserver.catalog.ConflictingDataError, e:
            msg = ('There was already a style named %s in GeoServer, '
                   'cannot overwrite: "%s"' % (name, str(e)))
            #logger.warn(msg)
            e.args = (msg,)

        #FIXME: Should we use the fully qualified typename?
        publishing.default_style = catalog.get_style(name)
        catalog.save(publishing)

    new_layer = QGSLayer(catalog, layer_name)

    return new_layer


def layer_type(filename):
    """Finds out if a filename is a Feature or a Vector
       returns a gsconfig resource_type string
       that can be either 'featureType' or 'coverage'
    """
    extension = os.path.splitext(filename)[1]
    if extension.lower() in ['.shp']:
        return FeatureType.resource_type
    elif extension.lower() in ['.tif', '.tiff', '.geotiff', '.geotif']:
        return Coverage.resource_type
    else:
        msg = ('Saving of extension [%s] is not implemented' % extension)
        raise Exception(msg)


def create_featurestore(cat, name, data, overwrite):
    #cat = Layer.objects.gs_catalog
    cat.create_featurestore(name, data, overwrite=overwrite)
    return cat.get_store(name), cat.get_resource(name)


def create_coveragestore(cat, name, data, overwrite):
    #cat = Layer.objects.gs_catalog
    cat.create_coveragestore(name, data, overwrite=overwrite)
    return cat.get_store(name), cat.get_resource(name)


def get_files(filename):
    """Converts the data to Shapefiles or Geotiffs and returns
       a dictionary with all the required files
    """
    files = {'base': filename}

    base_name, extension = os.path.splitext(filename)
    #Replace special characters in filenames - []{}()
    glob_name = re.sub(r'([\[\]\(\)\{\}])', r'[\g<1>]', base_name)

    if extension.lower() == '.shp':
        required_extensions = dict(
            shp='.[sS][hH][pP]', dbf='.[dD][bB][fF]', shx='.[sS][hH][xX]')
        for ext, pattern in required_extensions.iteritems():
            matches = glob.glob(glob_name + pattern)
            if len(matches) == 0:
                msg = ('Expected helper file %s does not exist; a Shapefile '
                       'requires helper files with the following extensions: '
                       '%s') % (base_name + "." + ext,
                                required_extensions.keys())
                raise Exception(msg)
            elif len(matches) > 1:
                msg = ('Multiple helper files for %s exist; they need to be '
                       'distinct by spelling and not just case.') % filename
                raise Exception(msg)
            else:
                files[ext] = matches[0]

        matches = glob.glob(glob_name + ".[pP][rR][jJ]")
        if len(matches) == 1:
            files['prj'] = matches[0]
        elif len(matches) > 1:
            msg = ('Multiple helper files for %s exist; they need to be '
                   'distinct by spelling and not just case.') % filename
            raise Exception(msg)

    matches = glob.glob(glob_name + ".[sS][lL][dD]")
    if len(matches) == 1:
        files['sld'] = matches[0]
    elif len(matches) > 1:
        msg = ('Multiple style files for %s exist; they need to be '
               'distinct by spelling and not just case.') % filename
        raise Exception(msg)

    matches = glob.glob(base_name + ".[xX][mM][lL]")

    # shapefile XML metadata is sometimes named base_name.shp.xml
    # try looking for filename.xml if base_name.xml does not exist
    if len(matches) == 0:
        matches = glob.glob(filename + ".[xX][mM][lL]")

    if len(matches) == 1:
        files['xml'] = matches[0]
    elif len(matches) > 1:
        msg = ('Multiple XML files for %s exist; they need to be '
               'distinct by spelling and not just case.') % filename
        raise Exception(msg)

    return files

# def cascading_delete(cat, layer_name):
#     resource = None
#     try:
#         if layer_name.find(':') != -1:
#             workspace, name = layer_name.split(':')
#             ws = cat.get_workspace(workspace)
#             resource = cat.get_resource(name, workspace=workspace)
#         else:
#             resource = cat.get_resource(layer_name)
#     except EnvironmentError, e:
#         if e.errno == errno.ECONNREFUSED:
#             msg = ('Could not connect to geoserver at "%s"'
#                    'to save information for layer "%s"' % (
#                    cat.url, layer_name)
#                   )
#             #logger.warn(msg, e)
#             return None
#         else:
#             raise e

#     if resource is None:
#         # If there is no associated resource,
#         # this method can not delete anything.
#         # Let's return and make a note in the log.
#         #logger.debug('cascading_delete was called with a non existant resource')
#         return
#     resource_name = resource.name
#     lyr = cat.get_layer(resource_name)
#     if(lyr is not None):  # Already deleted
#         store = resource.store
#         styles = lyr.styles + [lyr.default_style]
#         cat.delete(lyr)
#         for s in styles:
#             if s is not None and s.name not in _default_style_names:
#                 try:
#                     cat.delete(s, purge=True)
#                 except FailedRequestError as e:
#                     # Trying to delete a shared style will fail
#                     # We'll catch the exception and log it.
#                     logger.debug(e)

#         cat.delete(resource)
#         #if store.resource_type == 'dataStore' and 'dbtype' in store.connection_parameters and store.connection_parameters['dbtype'] == 'postgis':
#         #    delete_from_postgis(resource_name)
#         #else:
#         cat.delete(store)
