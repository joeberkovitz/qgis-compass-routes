import math
from qgis.core import QgsUnitTypes, QgsPointXY, QgsCoordinateReferenceSystem, QgsDistanceArea
from qgis.PyQt.QtCore import QCoreApplication

def tr(string):
    return QCoreApplication.translate('@default', string)

DISTANCE_LABELS = [tr("Kilometers"), tr("Meters"), tr("Centimeters"), tr("Miles"), tr('Yards'), tr("Feet"), tr("Inches"), tr("Nautical Miles")]

def conversionToMeters(units):
    if units == 0:  # Kilometers
        measureFactor = 1000.0
    elif units == 1:  # Meters
        measureFactor = 1.0
    elif units == 2:  # Centimeters
        measureFactor = QgsUnitTypes.fromUnitToUnitFactor(QgsUnitTypes.DistanceCentimeters, QgsUnitTypes.DistanceMeters)
    elif units == 3:  # Miles
        measureFactor = QgsUnitTypes.fromUnitToUnitFactor(QgsUnitTypes.DistanceMiles, QgsUnitTypes.DistanceMeters)
    elif units == 4:  # Yards
        measureFactor = QgsUnitTypes.fromUnitToUnitFactor(QgsUnitTypes.DistanceYards, QgsUnitTypes.DistanceMeters)
    elif units == 5:  # Feet
        measureFactor = QgsUnitTypes.fromUnitToUnitFactor(QgsUnitTypes.DistanceFeet, QgsUnitTypes.DistanceMeters)
    elif units == 6:  # Inches
        measureFactor = QgsUnitTypes.fromUnitToUnitFactor(QgsUnitTypes.DistanceFeet, QgsUnitTypes.DistanceMeters) / 12.0
    elif units == 7:  # Nautical Miles
        measureFactor = QgsUnitTypes.fromUnitToUnitFactor(QgsUnitTypes.DistanceNauticalMiles, QgsUnitTypes.DistanceMeters)
    return measureFactor

epsg4326 = QgsCoordinateReferenceSystem("EPSG:4326")

nmToMeters = QgsUnitTypes.fromUnitToUnitFactor(QgsUnitTypes.DistanceNauticalMiles, QgsUnitTypes.DistanceMeters)
degToMeters = nmToMeters * 60
metersToDeg = 1 / degToMeters

def addPoints(a, b):
    return QgsPointXY(a.x() + b.x(), a.y() + b.y())

def diffPoints(a, b):
    return QgsPointXY(a.x() - b.x(), a.y() - b.y())

def projectBearing(p, distance, bearing):
    r = math.radians(bearing)
    d = distance * metersToDeg
    n = QgsPointXY(d * math.sin(r) / math.cos(math.radians(p.y())), d * math.cos(r))
    return n
