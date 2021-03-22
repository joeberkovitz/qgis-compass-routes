import os
from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon
from .create_magnetic_north import CreateMagneticNorthAlgorithm
from .create_route_layer import CreateRouteLayerAlgorithm

class CompassRoutesProvider(QgsProcessingProvider):

    def unload(self):
        QgsProcessingProvider.unload(self)

    def loadAlgorithms(self):
        self.addAlgorithm(CreateMagneticNorthAlgorithm())
        self.addAlgorithm(CreateRouteLayerAlgorithm())

    def id(self):
        return 'compassroutes'

    def name(self):
        return 'Compass Routes'

    def longName(self):
        return self.name()
