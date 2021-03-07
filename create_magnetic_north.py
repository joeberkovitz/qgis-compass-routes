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
    PrmRecalibrationInterval = 'RecalibrationInterval'

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
                self.PrmRecalibrationInterval,
                tr('Line recalibration interval'),
                QgsProcessingParameterNumber.Double,
                defaultValue=60,
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
        recalibrationInterval = self.parameterAsDouble(parameters, self.PrmRecalibrationInterval, context)
        units = self.parameterAsInt(parameters, self.PrmUnitsOfMeasure, context)
        measureFactor = conversionToMeters(units)

        # adjust linear units
        lineDistance *= measureFactor
        traceInterval *= measureFactor
        recalibrationInterval *= measureFactor

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

        lastStartPoints = []
        recalibrationSize = round(recalibrationInterval / traceInterval)

        # Our major (longitude) loop starts here
        while True:

            # Initialize our line at the start
            line = [start]
            startPoints = [start]
            p1 = start
            startStepX = -1

            # Now we will trace the line in the field direction until we are out of the rectangle's Y range,
            # restarting a new line whenever the horizontal step gets out of whack due to latitude change.

            while True:
                # get the variation at this point
                variation = geomag.declination(p1.y(), p1.x(), 0, date.today())

                # Determine the longitude step that we will be taking at this latitude. This
                # can vary longitudinally because it's compensated for the magnetic variation.
                nextStep = qda.computeSpheroidProject(p1, lineDistance / math.cos(math.radians(variation)), math.radians(90))
                stepX = nextStep.x() - p1.x()
                if startStepX < 0:
                    startStepX = stepX

                p2 = qda.computeSpheroidProject(p1, traceInterval, math.radians(variation + traceAngle))
                if p2.y() < extent.yMinimum() or p2.y() > extent.yMaximum():
                    # Here we should be clipping the last segment to the extent edge
                    break

                line.append(p2)
                startPoints.append(p2)
                p1 = p2

                # start a new, longitudinally adjusted line if we have strayed too far
                if len(line) >= recalibrationSize:
                    feature = QgsFeature()
                    feature.setGeometry(QgsGeometry.fromPolylineXY(line))
                    sink.addFeature(feature)
                    if len(lastStartPoints) >= len(startPoints) + 1:
                        lastStartPoint = lastStartPoints[len(startPoints)]

                        # This is a hack that simply finds a point orthogonal to the previous trace in the proper
                        # direction, then backtracks along the new trace line a rigid distance. It produces the
                        # proper line spacing in the recalibrated line but has other undesirable effects.
                        p1Adj = qda.computeSpheroidProject(lastStartPoint, lineDistance, math.radians(variation+90))
                        p1Adj = qda.computeSpheroidProject(p1Adj, traceInterval * 2, math.radians(variation + traceAngle + 180))

                        # === This formula doesn't work because it assumes that X and Y distance units are equal
                        #
                        #p1Adj = QgsPointXY(lastStartPoint.x() + stepX, lastStartPoint.y())
                        # This point needs to be adjusted to match the latitude of the previous point              
                        # dy = p1.y() - p1Adj.y()
                        # p1 = QgsPointXY(p1Adj.x() + (dy * math.sin(math.radians(variation + traceAngle))), p1.y())
                        p1 = p1Adj

                    line = [p1]

            # end field tracing loop

            if len(line) >= 2:
                feature = QgsFeature()
                feature.setGeometry(QgsGeometry.fromPolylineXY(line))
                sink.addFeature(feature)

            if p2.x() > extent.xMaximum():
                break

            # now advance the start point to the east, correcting for the variation angle
            start.setX(start.x() + startStepX)
            startStepX = -1
            lastStartPoints = startPoints

        # end longitude loop

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

