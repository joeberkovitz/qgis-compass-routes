# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CompassRoutes
                                 A QGIS plugin
 This plugin creates layers that automatically label route legs with distance and magnetic bearing
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-03-05
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Joe Berkovitz
        email                : joseph.berkovitz@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon, QColor
from qgis.PyQt.QtWidgets import QAction

from qgis.core import (
    Qgis, QgsApplication, QgsCoordinateTransform, QgsCoordinateReferenceSystem,
    QgsExpression,
)

from qgis.core import qgsfunction

from . import geomag
from datetime import *
import math

# Initialize Qt resources from file resources.py
from .resources import *
from .utils import tr

# Import the code for the dialog
from.compass_routes_provider import CompassRoutesProvider

import os.path
import processing


class CompassRoutes:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = iface.mapCanvas()

        self.provider = CompassRoutesProvider()

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'CompassRoutes_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            translator = QTranslator()
            translator.load(locale_path)
            QCoreApplication.installTranslator(translator)

        # Declare instance attributes
        self.actions = []
        self.menu = tr(u'&Compass Routes')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.route_needs_init = None

        QgsApplication.processingRegistry().addProvider(self.provider)

        # Add custom functions to compute the magnetic variation at a point, or for a line
        QgsExpression.registerFunction(self.magnetic_variation)
        QgsExpression.registerFunction(self.to_magnetic)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/compass_routes/icon.png'

        self.add_action(
            icon_path,
            text=tr(u'Create Compass Route Layer'),
            callback=self.createRouteLayer,
            parent=self.iface.mainWindow())
        self.route_needs_init = True

        self.add_action(
            icon_path,
            text=tr(u'Create Magnetic North Lines'),
            callback=self.createMagNorthLayer,
            parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                tr(u'&Compass Routes'),
                action)
            self.iface.removeToolBarIcon(action)

        QgsApplication.processingRegistry().removeProvider(self.provider)

        QgsExpression.unregisterFunction('magnetic_variation')
        QgsExpression.unregisterFunction('to_magnetic')

    def createRouteLayer(self):
        processing.execAlgorithmDialog('compassroutes:createroutelayer', {})

    def createMagNorthLayer(self):
        processing.execAlgorithmDialog('compassroutes:createmagneticnorth', {})

    # Custom expression function to return geomagnetic variation at lat/long coordinates
    @qgsfunction(args=2, group='Compass Routes', register=False)
    def magnetic_variation(values, feature, parent):
        """Obtains the magnetic variation at some given coordinates.

        <br><br>magnetic_variation(lat, long)

        <br><br>lat -- latitude as a number in signed degrees
        <br>long -- longitude as a number in signed degrees
        """

        latitude = values[0]
        longitude = values[1]
        return geomag.declination(latitude, longitude, 0, date.today())

    # Custom expression function to convert a true bearing to a magnetic bearing at the given coordinates
    @qgsfunction(args=3, group='Compass Routes', register=False)
    def to_magnetic(values, feature, parent):
        """Converts a true bearing at some given coordinates to a magnetic bearing in the range 0-360.

        <br><br>to_magnetic(bearing, lat, long)

        <br><br>bearing -- a true bearing in degrees
        <br>lat -- latitude as a number in signed degrees
        <br>long -- longitude as a number in signed degrees
        """
        bearing = values[0]
        latitude = values[1]
        longitude = values[2]
        variation = geomag.declination(latitude, longitude, 0, date.today())
        azimuth = bearing - variation
        while azimuth < 0:
            azimuth += 360
        while azimuth >= 360:
            azimuth -= 360
        return azimuth
