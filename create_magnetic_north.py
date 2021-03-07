import os
import math
from datetime import *

from qgis.core import (
    QgsPointXY, QgsPoint, QgsFeature, QgsGeometry, QgsField, QgsFields,
    QgsProject, QgsUnitTypes, QgsWkbTypes, QgsCoordinateTransform,
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

nmToMeters = QgsUnitTypes.fromUnitToUnitFactor(QgsUnitTypes.DistanceNauticalMiles, QgsUnitTypes.DistanceMeters)

class CreateMagneticNorthAlgorithm(QgsProcessingAlgorithm):
    PrmOutputLayer = 'OutputLayer'
    PrmExtent = 'Extent'
    PrmUnitsOfMeasure = 'UnitsOfMeasure'
    PrmLineDistance = 'LineDistance'
    PrmTraceInterval = 'TraceInterval'
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
                self.PrmTraceInterval,
                tr('Field trace interval'),
                QgsProcessingParameterNumber.Double,
                defaultValue=1.0,
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
        traceInterval = self.parameterAsDouble(parameters, self.PrmTraceInterval, context)
        distanceTolerance = self.parameterAsDouble(parameters, self.PrmDistanceTolerance, context)
        units = self.parameterAsInt(parameters, self.PrmUnitsOfMeasure, context)
        measureFactor = conversionToMeters(units)

        # adjust linear units
        lineDistance *= measureFactor
        traceInterval *= measureFactor
        distanceTolerance *= measureFactor

        (sink, dest_id) = self.parameterAsSink(
            parameters, self.PrmOutputLayer, context, QgsFields(),
            QgsWkbTypes.LineString, epsg4326)


        heightInMeters = extent.height() * 60 * nmToMeters

        qda = QgsDistanceArea()
        qda.setEllipsoid('WGS84')

        # Determine an initial origin and direction in which to trace field lines, either the NW (or SW)
        # of the extent based on sign of the variation in the extent's center. This roughly ensures that a
        # field line to magnetic S (or N) from this origin will be the westernmost line visible in the extent.

        centerVar = geomag.declination(extent.center().y(), extent.center().x(), 0, date.today())
        if centerVar < 0:
            start = QgsPointXY(extent.xMinimum(), extent.yMinimum())
            traceAngle = 0 # trace towards mag N
        else:
            start = QgsPointXY(extent.xMinimum(), extent.yMaximum())
            traceAngle = 180 # trace towards mag S

        feedback.pushDebugInfo('start=' + str(start) + ', traceAngle=' + str(traceAngle))

        # Our major loop begins with a check that the start point has not gone past the E of the extent
        prevLine = None

        while True:
            # Initialize our line at the start
            line = []
            line.append(start)

            # Now we will trace the line until we are out of the rectangle's Y range
            p1 = start
            while True:
                variation = geomag.declination(p1.y(), p1.x(), 0, date.today())
                p2 = qda.computeSpheroidProject(p1, traceInterval, math.radians(variation + traceAngle))

                feedback.pushDebugInfo('p1=' + str(p1) + ', p2=' + str(p2))

                if p2.y() < extent.yMinimum() or p2.y() > extent.yMaximum():
                    # Here we should be clipping to the extent edge
                    break

                line.append(p2)
                p1 = p2

            feature = QgsFeature()
            feature.setGeometry(QgsGeometry.fromPolylineXY(line))
            sink.addFeature(feature)

            if p2.x() > extent.xMaximum():
                break

            # now advance the start point to the east, correcting for the variation angle
            start = qda.computeSpheroidProject(start, lineDistance / math.cos(math.radians(centerVar)), math.radians(90))

        # variation = geomag.declination(extent.center().y(), extent.center().x(), 0, date.today())
        # varRadians = math.radians(variation)
        # start = QgsPointXY(extent.xMinimum(), extent.yMinimum())
        # end = qda.computeSpheroidProject(start, heightInMeters/math.cos(varRadians), varRadians)
        # if end.x() > start.x():
        #     start.setX(end.x())
        #     end = qda.computeSpheroidProject(start, heightInMeters/math.cos(varRadians), varRadians)

        return {self.PrmOutputLayer: dest_id}

    def name(self):
        return 'createmagneticnorth'

    def displayName(self):
        return tr('Create Magnetic North Lines')

    def helpUrl(self):
        return ''

    def createInstance(self):
        return CreateMagneticNorthAlgorithm()

