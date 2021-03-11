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

    # Set up this algorithm
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
                tr('Distance between adjacent lines'),
                QgsProcessingParameterNumber.Double,
                defaultValue=1.0,
                optional=False)
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.PrmTraceInterval,
                tr('Tracing resolution of field lines'),
                QgsProcessingParameterNumber.Double,
                defaultValue=5.0,
                optional=False)
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.PrmDistanceTolerance,
                tr('Maximum error in distance between lines (zero=disregard)'),
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
        # gather parameters
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

        # obtain our output sink
        (sink, dest_id) = self.parameterAsSink(
            parameters, self.PrmOutputLayer, context, QgsFields(),
            QgsWkbTypes.LineString, epsg4326)


        # Determine the longitude step direction based on sign of the variation in the extent's center,
        # so that we start on the side of the extent such that we will fill in partial lines at the corner.
        # TODO: this is not ideal when the extent intersects an agonic line.
        centerVar = geomag.declination(extent.center().y(), extent.center().x(), 0, date.today())
        start = QgsPointXY(extent.xMinimum(), extent.yMinimum())
        if centerVar > 0:
            lineDistance = -lineDistance
            start.setX(extent.xMaximum())

        # We trace between points at a fixed longitude interval, so that the distance-preservation logic below
        # is straightforward and we can compare points in successive traces easily.
        traceIntervalDeg = traceInterval * metersToDeg
        numTraces = math.ceil(extent.height() / traceIntervalDeg)
        traceY = extent.height() / numTraces

        lineCount = 0
        lastStartPoints = []

        # Our major (longitude) loop starts here
        while True:
            # Initialize our line at the start
            empty = True
            line = []
            startPoints = []

            # Add the first point
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
                # and scale this to find a vector taking us from p1 to the next latitude step
                magN = projectBearing(p1, 1, variation)
                magN.multiply((y - p1.y()) / magN.y())  # note that Y magnitude will be nonzero for reasonable variations
                p2 = addPoints(p1, magN)

                if p2.x() >= extent.xMinimum() and p2.x() <= extent.xMaximum():
                    line.append(p2)
                    empty = False

                # start a new, longitudinally adjusted line if distance exceeds tolerance
                if distanceTolerance > 0 and len(lastStartPoints) > t:
                    lastP2 = lastStartPoints[t]
                    (factor, nextX) = self.adjustLongForVariation(lastP2, lineDistance, variation)
                    if abs(p2.x() - nextX) > distanceTolerance * factor:
                        # Flush any line that is in progress
                        if len(line) >= 2:
                            feature = QgsFeature()
                            feature.setGeometry(QgsGeometry.fromPolylineXY(line))
                            sink.addFeature(feature)

                        # Now start a new line, properly spaced from the previous trace
                        p2 = QgsPointXY(nextX, p2.y())
                        line = []
                        if p2.x() >= extent.xMinimum() and p2.x() <= extent.xMaximum():
                            line.append(p2)
                            empty = False

                startPoints.append(p2)
                p1 = p2

            # end field tracing loop

            # Flush any accumulated points to a polyline
            if len(line) >= 2:
                feature = QgsFeature()
                feature.setGeometry(QgsGeometry.fromPolylineXY(line))
                sink.addFeature(feature)

            # If we did not manage to find any points inside the extent on this trace, we're done
            if empty:
                break

            # hold onto our point list for spacing check on the next trace
            lastStartPoints = startPoints

            # now advance the start point to the east, correcting for the variation angle
            variation = geomag.declination(start.y(), start.x(), 0, date.today())
            (factor, nextX) = self.adjustLongForVariation(start, lineDistance, variation)
            start.setX(nextX)

            lineCount += 1
            if lineDistance > 0:
                feedback.setProgress(100*(start.x() - extent.xMinimum())/extent.width())
            else:
                feedback.setProgress(100*(extent.xMaximum() - start.x())/extent.width())

        # end longitude loop

        return {self.PrmOutputLayer: dest_id}

    # Compute a factor converting longitudinal distance into degrees at a given point's latitude
    # and also give an adjusted X coordinate moving the point a given distance.
    def adjustLongForVariation(self, p, distance, variation):
        east = projectBearing(p, 1, 90)
        factor = east.x() / math.cos(math.radians(variation))
        return (factor, p.x() + (distance * factor))

    def name(self):
        return 'createmagneticnorth'

    def displayName(self):
        return tr('Create Magnetic North Lines')

    def helpUrl(self):
        return ''

    def createInstance(self):
        return CreateMagneticNorthAlgorithm()

