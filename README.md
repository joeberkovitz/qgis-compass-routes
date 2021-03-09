## qgis-compass-routes

This plugin creates vector layers that work with magnetic variation.

The commands in this plugin are available under the **Plugins** menu in QGIS:

### Create Compass Route Layer

This command adds a new Line layer with memory storage rendering as arrows that are automatically labeled with distance and magnetic heading. The variation for the layer is chosen before creating the dialog, and can be defaulted from the center of the map canvas. The `magnetic_var` layer property stores the variation used for the layer.

### Create Magnetic North Lines

This processing script adds a vector layer containing magnetic north lines within a given extent. Lines are spaced by a given distance and are broken and redrawn to preserve this spacing within an error tolerance.

### Credits

For dynamic computation of magnetic declination, uses the `geomag` package by Christopher Weiss - see https://github.com/cmweiss/geomag

Adapted from the geomagc software and World Magnetic Model of the NOAA Satellite and Information Service, [National Geophysical Data Center](http://www.ngdc.noaa.gov/geomag/WMM/).

Model values by NCEI Geomagnetic Modeling Team and British Geological Survey. 2019. World Magnetic Model 2020. NOAA National Centers for Environmental Information. [doi: 10.25921/11v3-da71](https://doi.org/10.25921/11v3-da71), 2020.
