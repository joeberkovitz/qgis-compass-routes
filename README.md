---
permalink: index.html
---
## qgis-compass-routes

This plugin creates vector layers that work with magnetic variation.

It contains both menu commands (available under **Plugins > Compass Routes**) and Processing plugins.

### Create Compass Route Layer

This menu command adds a new Line layer with memory storage, whose lines
render as arrows that are automatically labeled with distance and magnetic
heading. 

Before running the command, set up your main map canvas to point at the area
of interest. When you run the command, the following dialog will be shown:

<img alt="Compass route layer dialog" src="doc/images/CompassRoutesDialog.png" width="50%">

The *Magnetic variation* field is defaulted to the variation in the center of
the map canvas, but can be changed. Negative values are West variations;
positive values are East. The *Recalculate* button will recalculate the
variation if the map canvas is adjusted.

The new layer is initially empty and is given the name specified in the dialog
plus a suffix noting the variation used for labeling. Lines in the layer are
automatically labeled in this fashion:

![Route segments](doc/images/RouteSegments.png)

The `magnetic_var` layer property stores the variation used for the layer, so you can change
it in the layer's Properties dialog if needed.

### Create Magnetic North Lines

This processing script adds a vector layer containing magnetic north lines
within a given extent, optionally labeled with their variation. Lines are
spaced by a given distance and are broken and redrawn to preserve this spacing
within an error tolerance.

Parameters to the script are as follows:

*Extent* is the rectangle within which lines will be added. It's typically
convenient to use the dropdown to default this to the map canvas view area, or
to draw a rectangle on the map canvas.

*Units of measure* provides the units in which the various other
distance-related parameters are expressed. It defaults to nautical miles.

*Distance between adjacent lines* gives the parallel distance between adjacent
magnetic north lines. This distance is only approximate as field lines will
converge as traced towards the magnetic poles: the plugin preserves the
accuracy of variation at the expense of line spacing.

*Tracing resolution of field lines* governs the resolution of field lines.
Each line is created by repeatedly advancing at roughly this interval along
the field, yielding a number of points. These are then connected to form an
approximation to the field line.

*Maximum error in distance between lines* specifies the largest error in line
spacing that will be tolerated before a traced line is ended and a new one
begun at the proper distance from the previous one. (Note that lines are
traced from south to north, so the initial spacing is correct on the south
side of the extent.) Providing zero for this parameter, forces lines to be
generated continuously with no breaks and with unpredictable spacing on the
north of the extent.

*Labeling interval* specifies the interval at which lines will be labeled. The
default value of 5 indicates that every fifth traced field line gets a label.
1 implies every line is labeled; 0 disables labeling altogether.

*Output layer* is a vector layer in which the results will be placed. The CRS
of the layer is always EPSG:4326 regardless of the project CRS.

An example of a generated grid at a small scale looks like this (accepting the
defaults for a 1 nm spacing):

<img alt="Magnetic north lines" src="doc/images/MagneticNorthLines.png" width="50%">

At a larger scale, the breaking and rebreaking of lines looks like this (this uses a
10 nm spacing with 0.1 nm max error):


<img alt="Broken magnetic north lines" src="doc/images/BrokenMagNorthLines.png" width="50%">

### Credits

For dynamic computation of magnetic declination, uses the `geomag` package by Christopher Weiss - see https://github.com/cmweiss/geomag

Adapted from the geomagc software and World Magnetic Model of the NOAA Satellite and Information Service, [National Geophysical Data Center](http://www.ngdc.noaa.gov/geomag/WMM/).

Model values by NCEI Geomagnetic Modeling Team and British Geological Survey. 2019. World Magnetic Model 2020. NOAA National Centers for Environmental Information. [doi: 10.25921/11v3-da71](https://doi.org/10.25921/11v3-da71), 2020.
