## qgis-compass-routes

This plugin creates vector layers that work with magnetic variation.

The commands in this plugin are available under the **Plugins** menu in QGIS:

### Create Compass Route Layer

This command adds a new Line layer with memory storage rendering as arrows that are automatically labeled with distance and magnetic heading. The variation for the layer is chosen before creating the dialog, and can be defaulted from the center of the map canvas. The `magnetic_var` layer property stores the variation used for the layer.

### Create Magnetic North Lines

This processing script adds a vector layer containing magnetic north lines within a given extent. Lines are spaced by a given distance and are broken and redrawn to preserve this spacing within an error tolerance.
