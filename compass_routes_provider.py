import os
from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon
from .create_magnetic_north import CreateMagneticNorthAlgorithm

class CompassRoutesProvider(QgsProcessingProvider):

    def unload(self):
        QgsProcessingProvider.unload(self)

    def loadAlgorithms(self):
        self.addAlgorithm(CreateMagneticNorthAlgorithm())

    def id(self):
        return 'compassroutes'

    def name(self):
        return 'Compass Routes'

    def longName(self):
        return self.name()
