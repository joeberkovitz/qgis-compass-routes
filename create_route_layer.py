import os
import math
from datetime import *

from qgis.core import (
    QgsPointXY, QgsPoint, QgsFeature, QgsGeometry, QgsField, QgsFields,
    QgsProject, QgsUnitTypes, QgsWkbTypes, QgsCoordinateTransform,
    QgsLineString, QgsDistanceArea, QgsPalLayerSettings,
    QgsLabelLineSettings, QgsVectorLayer, QgsVectorLayerSimpleLabeling)

from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingLayerPostProcessorInterface,
    QgsProcessingFeedback,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterNumber,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterExtent,
    QgsProcessingParameterFeatureSink)

from qgis.PyQt.QtGui import QIcon, QColor
from qgis.PyQt.QtCore import QVariant, QUrl

from .utils import *
from . import geomag

class CreateRouteLayerAlgorithm(QgsProcessingAlgorithm):
    PrmOutputLayer = 'OutputLayer'

    # Set up this algorithm
    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.PrmOutputLayer,
                tr('Output layer'))
        )
        self.feedback = QgsProcessingFeedback()

    def processAlgorithm(self, parameters, context, feedback):
        # obtain our output sink
        (sink, dest_id) = self.parameterAsSink(
            parameters, self.PrmOutputLayer, context, QgsFields(),
            QgsWkbTypes.LineString, epsg4326)

        if context.willLoadLayerOnCompletion(dest_id):
            context.layerToLoadOnCompletionDetails(dest_id).setPostProcessor(StylePostProcessor.create(self))

        return {self.PrmOutputLayer: dest_id}

    def name(self):
        return 'createroutelayer'

    def displayName(self):
        return tr('Create Compass Route Layer')

    def helpUrl(self):
        return ''

    def createInstance(self):
        return CreateRouteLayerAlgorithm()

class StylePostProcessor(QgsProcessingLayerPostProcessorInterface):
    instance = None

    def __init__(self, proc):
        super(StylePostProcessor, self).__init__()
        self.processor = proc

    def postProcessLayer(self, layer, context, feedback):
        if not isinstance(layer, QgsVectorLayer):
            return

        layer.setName(tr('Routes'))
        layer.loadNamedStyle(os.path.join(os.path.dirname(__file__),'styles','routes.qml'))

    @staticmethod
    def create(proc) -> 'StylePostProcessor':
        StylePostProcessor.instance = StylePostProcessor(proc)
        return StylePostProcessor.instance
