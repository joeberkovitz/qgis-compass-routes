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

from .utils import *
from . import geomag

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
                optional=False)
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.PrmTraceInterval,
                tr('Field trace interval'),
                QgsProcessingParameterNumber.Double,
                defaultValue=5.0,
                optional=False)
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.PrmDistanceTolerance,
                tr('Line distance tolerance (zero means disregard)'),
                QgsProcessingParameterNumber.Double,
                defaultValue=0.05,
                optional=False)
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


        heightInMeters = extent.height() * degToMeters # works since it's latitude

        # Determine the longitude step direction based on sign of the variation in the extent's center,
        # so that we start at a place where we will fill in partial lines at the corner.

        centerVar = geomag.declination(extent.center().y(), extent.center().x(), 0, date.today())
        start = QgsPointXY(extent.xMinimum(), extent.yMinimum())
        if centerVar > 0:
            lineDistance = -lineDistance
            start.setX(extent.xMaximum())

        lastStartPoints = []
        traceIntervalDeg = traceInterval * metersToDeg
        numTraces = math.ceil(extent.height() / traceIntervalDeg)
        traceY = extent.height() / numTraces

        lineCount = 0

        # Our major (longitude) loop starts here
        while True:
            # Initialize our line at the start
            empty = True
            line = []
            startPoints = []
            p1 = start
            if p1.x() >= extent.xMinimum() and p1.x() <= extent.xMaximum():
                line.append(p1)
                empty = False

            # Now we will trace the line in the field direction until we are out of the rectangle's Y range,
            # restarting a new line whenever the horizontal step gets out of whack due to latitude change.

            for t in range(0, numTraces + 1):
                y = extent.yMinimum() + (t * traceY)

                # get the variation at this point
                variation = geomag.declination(p1.y(), p1.x(), 0, date.today())

                # determine a 1-meter vector in the direction of magnetic north
                magN = projectBearing(p1, 1, variation)

                # Scale this to find a vector taking us from p1 to the desired latitude
                d = QgsPointXY(magN)
                d.multiply((y - p1.y()) / d.y())  # note that d.y() will be nonzero for reasonable variations
                p2 = addPoints(p1, d)

                if p2.x() >= extent.xMinimum() and p2.x() <= extent.xMaximum():
                    line.append(p2)
                    empty = False

                # start a new, longitudinally adjusted line if distance exceeds tolerance
                if distanceTolerance > 0 and len(lastStartPoints) > t:
                    lastP2 = lastStartPoints[t]
                    eastUnitP2 = projectBearing(lastP2, 1, 90)
                    correction = eastUnitP2.x() / math.cos(math.radians(variation))
                    if abs(p2.x() - lastP2.x() - (lineDistance * correction)) > distanceTolerance * correction:
                        if len(line) >= 2:
                            feature = QgsFeature()
                            feature.setGeometry(QgsGeometry.fromPolylineXY(line))
                            sink.addFeature(feature)

                        p2 = QgsPointXY(p2) # make a copy since it was appended to the prior line
                        p2.setX(lastP2.x() + (lineDistance * correction))
                        line = []
                        if p2.x() >= extent.xMinimum() and p2.x() <= extent.xMaximum():
                            line.append(p2)
                            empty = False

                startPoints.append(p2)
                p1 = p2

            # end field tracing loop

            if len(line) >= 2:
                feature = QgsFeature()
                feature.setGeometry(QgsGeometry.fromPolylineXY(line))
                sink.addFeature(feature)

            # now advance the start point to the east, correcting for the variation angle
            variation = geomag.declination(start.y(), start.x(), 0, date.today())
            start = addPoints(start, projectBearing(start, lineDistance, variation + 90))
            magN = projectBearing(start, 1, variation)
            magN.multiply((extent.yMinimum() - start.y()) / magN.y())
            start = addPoints(start, magN)

            if empty:
                break

            lastStartPoints = startPoints

            lineCount += 1
            if lineCount % 10 == 0:
                feedback.pushInfo('Field lines added: ' + str(lineCount))

        # end longitude loop

        # variation = geomag.declination(extent.center().y(), extent.center().x(), 0, date.today())
        # varRadians = math.radians(variation)
        # start = QgsPointXY(extent.xMinimum(), extent.yMinimum())
        # end = wgs84.computeSpheroidProject(start, heightInMeters/math.cos(varRadians), varRadians)
        # if end.x() > start.x():
        #     start.setX(end.x())
        #     end = wgs84.computeSpheroidProject(start, heightInMeters/math.cos(varRadians), varRadians)

        return {self.PrmOutputLayer: dest_id}

    def name(self):
        return 'createmagneticnorth'

    def displayName(self):
        return tr('Create Magnetic North Lines')

    def helpUrl(self):
        return ''

    def createInstance(self):
        return CreateMagneticNorthAlgorithm()

