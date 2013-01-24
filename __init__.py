"""
Geoserver Geonode QGIS Bridge
A QGS plugin to download and upload data, styles metadata to and from GeoServer 

This script initializes the plugin, making it known to QGIS.


Contact: vivien.deparday@gmail.com

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

""" 

__copyright__ = ('Copyright 2013, Global Facility for Disaster Reduction')


def name():
	"""A user friendly name for the plugin."""
	return "Geoserver QGIS Bridge"

def author():
	"""Author name."""
	return "Global Facility for Disaster Reduction"

def email():
    return "vivien.deparday@gmail.com"

def description():
    return ("A plugin to download and upload data, styles to and from GeoServer "
    		"developed by GFDDR")

def version():
    return "Version 0.1"

def qgisMinimumVersion():
	"""Minimum version of QGIS needed to run this plugin."""
	return "1.9"

def icon():
    """Icon path for the plugin - metadata.txt will override this."""
    return 'icon.png'

def classFactory(iface):
    # load GeoserverQGIS class from file GeoserverQGIS
    from geoserver_qgis import GeoserverQGIS
    return GeoserverQGIS(iface)


