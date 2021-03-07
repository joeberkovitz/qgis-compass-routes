import os
import math
from datetime import *

from qgis.core import (
    QgsPointXY, QgsPoint, QgsFeature, QgsGeometry, QgsField, QgsFields,
    QgsProject, QgsWkbTypes, QgsCoordinateTransform,
    QgsLineString, QgsDistanceArea)

from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingFeedback,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterNumber,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterExtent,
    QgsProcessingParameterFeatureSink)

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QVariant, QUrl

from .utils import tr, conversionToMeters, DISTANCE_LABELS, epsg4326
from . import geomag

class CreateMagneticNorthAlgorithm(QgsProcessingAlgorithm):
    PrmOutputLayer = 'OutputLayer'
    PrmExtent = 'Extent'
    PrmUnitsOfMeasure = 'UnitsOfMeasure'
    PrmLineDistance = 'LineDistance'
    PrmBearingTolerance = 'BearingTolerance'
    PrmDistanceTolerance = 'DistanceTolerance'

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterExtent(
                self.PrmExtent,
                tr('Extent')
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                self.PrmUnitsOfMeasure,
                tr('Units of measure'),
                options=DISTANCE_LABELS,
                defaultValue=7,
                optional=False)
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.PrmLineDistance,
                tr('Distance between lines'),
                QgsProcessingParameterNumber.Double,
                defaultValue=1.0,
                optional=True)
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.PrmBearingTolerance,
                tr('Variation tolerance'),
                QgsProcessingParameterNumber.Double,
                defaultValue=0.5,
                optional=True)
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.PrmDistanceTolerance,
                tr('Line distance tolerance'),
                QgsProcessingParameterNumber.Double,
                defaultValue=0.5,
                optional=True)
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.PrmOutputLayer,
                tr('Output layer'))
        )
        self.feedback = QgsProcessingFeedback()

    def processAlgorithm(self, parameters, context, feedback):
        extent = self.parameterAsExtent(parameters, self.PrmExtent, context, epsg4326)
        lineDistance = self.parameterAsDouble(parameters, self.PrmLineDistance, context)
        bearingTolerance = self.parameterAsDouble(parameters, self.PrmBearingTolerance, context)
        distanceTolerance = self.parameterAsDouble(parameters, self.PrmDistanceTolerance, context)
        units = self.parameterAsInt(parameters, self.PrmUnitsOfMeasure, context)
        measureFactor = conversionToMeters(units)

        # adjust linear units
        lineDistance *= measureFactor
        distanceTolerance *= measureFactor

        (sink, dest_id) = self.parameterAsSink(
            parameters, self.PrmOutputLayer, context, QgsFields(),
            QgsWkbTypes.LineString, epsg4326)

        # sink.renderer().symbol().setColor(QColor.fromRgb(0xCC0000))
        # sink.renderer().symbol().setWidth(0.25)
        heightInMeters = extent.height() * 60 * 1852

        qda = QgsDistanceArea()
        qda.setEllipsoid('WGS84')

        variation = geomag.declination(extent.center().y(), extent.center().x(), 0, date.today())
        varRadians = math.radians(variation)
        start = QgsPointXY(extent.xMinimum(), extent.yMinimum())
        end = qda.computeSpheroidProject(start, heightInMeters/math.cos(varRadians), varRadians)
        if end.x() > start.x():
            start.setX(end.x())
            end = qda.computeSpheroidProject(start, heightInMeters/math.cos(varRadians), varRadians)

        feedback.pushDebugInfo('extent:' + str(extent) + ', start:' + str(start))
        while start.x() < extent.xMaximum() or end.x() < extent.xMaximum():
            line = QgsLineString()
            line.addVertex(QgsPoint(start.x(), start.y()))
            line.addVertex(QgsPoint(end.x(), end.y()))
            feature = QgsFeature()
            feature.setGeometry(line)
            sink.addFeature(feature)

            start = qda.computeSpheroidProject(start, lineDistance / math.cos(varRadians), math.radians(90))
            end = qda.computeSpheroidProject(start, heightInMeters/math.cos(varRadians), varRadians)
            feedback.pushDebugInfo('..extent:' + str(extent) + ', start:' + str(start))

        return {self.PrmOutputLayer: dest_id}

    def name(self):
        return 'createmagneticnorth'

    def displayName(self):
        return tr('Create Magnetic North Lines')

    def helpUrl(self):
        return ''

    def createInstance(self):
        return CreateMagneticNorthAlgorithm()

