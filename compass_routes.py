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
    Qgis, QgsCoordinateTransform, QgsCoordinateReferenceSystem,
    QgsUnitTypes, QgsWkbTypes, QgsGeometry, QgsFields, QgsField,
    QgsProject, QgsVectorLayer, QgsFeature, QgsPoint, QgsPointXY, QgsLineString, QgsDistanceArea,
    QgsArrowSymbolLayer, QgsLineSymbol, QgsSingleSymbolRenderer,
    QgsPalLayerSettings, QgsVectorLayerSimpleLabeling, QgsSettings,QgsExpressionContextUtils)

from . import geomag
from datetime import *
import math

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .create_compass_routes_layer_dialog import CreateCompassRoutesLayerDialog
from .create_mag_north_layer_dialog import CreateMagNorthLayerDialog
import os.path


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

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'CompassRoutes_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Compass Routes')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.route_needs_init = None
        self.mag_north_needs_init = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('CompassRoutes', message)


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
            text=self.tr(u'Create Compass Route Layer'),
            callback=self.createRouteLayer,
            parent=self.iface.mainWindow())
        self.route_needs_init = True

        self.add_action(
            icon_path,
            text=self.tr(u'Create Magnetic North Layer'),
            callback=self.createMagNorthLayer,
            parent=self.iface.mainWindow())
        self.mag_north_needs_init = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Compass Routes'),
                action)
            self.iface.removeToolBarIcon(action)


    def createRouteLayer(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.route_needs_init == True:
            self.route_needs_init = False
            self.routeDialog = CreateCompassRoutesLayerDialog()
            self.routeDialog.addLayerButton.clicked.connect(self.doCreateRouteLayer)
            self.routeDialog.calculateButton.clicked.connect(self.calcRouteDeclination)

        # always default declination on startup
        self.calcRouteDeclination()

        # show the dialog
        self.routeDialog.show()
        # Run the dialog event loop
        result = self.routeDialog.exec_()

        # do nothing here since either we added the layer, or we got cancelled

    def calcRouteDeclination(self):
        self.routeDialog.variationBox.setValue(self.calculateDeclination())

    def createMagNorthLayer(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.mag_north_needs_init == True:
            self.mag_north_needs_init = False
            self.magNorthDialog = CreateMagNorthLayerDialog()
            self.magNorthDialog.addLayerButton.clicked.connect(self.doCreateMagNorthLayer)
            self.magNorthDialog.calculateButton.clicked.connect(self.calcMagNorthDeclination)

        # always default declination on startup
        self.calcMagNorthDeclination()

        # show the dialog
        self.magNorthDialog.show()
        # Run the dialog event loop
        result = self.magNorthDialog.exec_()

        # do nothing here since either we added the layer, or we got cancelled

    def calcMagNorthDeclination(self):
        self.magNorthDialog.variationBox.setValue(self.calculateDeclination())

    def calculateDeclination(self):
        xform = QgsCoordinateTransform(self.iface.mapCanvas().mapSettings().destinationCrs(),
            QgsCoordinateReferenceSystem('EPSG:4326'),
            QgsProject.instance())
        center = xform.transform(self.iface.mapCanvas().center())
        return round(geomag.declination(center.y(), center.x(), 0, date.today()))

    def doCreateRouteLayer(self):
        # Create a temporary layer with appropriate symbology and labeling that will
        # automatically label each line with distance and heading.

        variation = self.routeDialog.variationBox.value()
        canvasCrs = self.canvas.mapSettings().destinationCrs()
        fields = QgsFields()   # there are no fields.

        degrees = str(abs(variation)) + 'º' + ('W' if variation < 0 else 'E')
        layerName = self.routeDialog.layerEdit.text() + " (var. " + degrees + ")"
        layer = QgsVectorLayer("LineString?crs={}".format(canvasCrs.authid()), layerName, "memory")
        dp = layer.dataProvider()
        dp.addAttributes(fields)
        layer.updateFields()

        # Set up the layer with an expression label that does what we want
        label = QgsPalLayerSettings()
        label.fieldName = (
            "concat(format_number($length,2),' @ ',"
            "lpad(format_number("
            "round(degrees(azimuth(start_point($geometry), end_point($geometry)))+360-@magnetic_var)%360,0),3,'0'),"
            "' M')")
        try:
            label.placement = QgsPalLayerSettings.Line
        except Exception:
            label.placement = QgsPalLayerSettings.AboveLine
        label.dist = 2.5
        label.isExpression = True
        label.overrunDistance = 1000

        # configure the text, background and symbology to a reasonable default
        format = label.format()
        format.setSizeUnit(QgsUnitTypes.RenderUnit.RenderMillimeters)
        format.setColor(QColor.fromRgb(0))
        format.setNamedStyle('Bold')
        format.setSize(7)
        format.background().setFillColor(QColor.fromRgba(0xCCFFFFFF))
        format.background().setEnabled(True)

        label.setFormat(format)
        labeling = QgsVectorLayerSimpleLabeling(label)
        layer.setLabeling(labeling)
        layer.setLabelsEnabled(True)

        arrow = QgsArrowSymbolLayer()
        arrow.setArrowStartWidth(1)
        arrow.setArrowWidth(1)
        arrow.setHeadThickness(5)
        arrow.setHeadLength(5)
        arrow.setIsCurved(False)
        arrow.setIsRepeated(False)
        arrow.setColor(QColor.fromRgba(0xCC4daf4a))

        layer.renderer().symbol().changeSymbolLayer(0,arrow)

        QgsExpressionContextUtils.setLayerVariable(layer,'magnetic_var',str(variation))

        layer.updateExtents()
        QgsProject.instance().addMapLayer(layer)

        self.routeDialog.close()  

    def doCreateMagNorthLayer(self):
        # Create a temporary layer with appropriate symbology and labeling that will
        # automatically label each line with distance and heading.

        variation = self.magNorthDialog.variationBox.value()
        units = QgsUnitTypes.DistanceNauticalMiles
        canvasCrs = self.canvas.mapSettings().destinationCrs()
        layerCrs = QgsCoordinateReferenceSystem('EPSG:4326')  # always WGS84 for these grids
        fields = QgsFields()   # there are no fields.

        degrees = str(abs(variation)) + 'º' + ('W' if variation < 0 else 'E')
        layerName = self.magNorthDialog.layerEdit.text() + " (var. " + degrees + ")"
        layer = QgsVectorLayer("LineString?crs={}".format(layerCrs.authid()), layerName, "memory")
        dp = layer.dataProvider()
        dp.addAttributes(fields)
        layer.updateFields()

        layer.startEditing()

        layer.renderer().symbol().setColor(QColor.fromRgb(0xCC0000))

        xform = QgsCoordinateTransform(canvasCrs, layerCrs, QgsProject.instance())
        extent = xform.transformBoundingBox(self.canvas.mapSettings().visibleExtent())
        heightInMeters = extent.height() * 60 * QgsUnitTypes.fromUnitToUnitFactor(QgsUnitTypes.DistanceNauticalMiles, QgsUnitTypes.DistanceMeters)

        line = QgsLineString()
        qda = QgsDistanceArea()
        qda.setEllipsoid('WGS84')

        varRadians = 2*math.pi*variation/360
        start = QgsPointXY(extent.xMinimum(), extent.yMinimum())
        end = qda.computeSpheroidProject(start, heightInMeters/math.cos(varRadians), varRadians)

        line.addVertex(QgsPoint(start.x(), start.y()))
        line.addVertex(QgsPoint(end.x(), end.y()))

        feature = QgsFeature()
        feature.setGeometry(line)
        layer.addFeature(feature)

        layer.commitChanges()

        layer.updateExtents()
        QgsProject.instance().addMapLayer(layer)

        self.magNorthDialog.close()  
