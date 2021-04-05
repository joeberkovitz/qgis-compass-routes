<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Forms|MapTips|Temporal" labelsEnabled="1" version="3.16.4-Hannover">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal durationField="" startField="" mode="0" startExpression="" accumulate="0" enabled="0" endField="" endExpression="" durationUnit="min" fixedDuration="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 type="singleSymbol" forceraster="0" symbollevels="0" enableorderby="0">
    <symbols>
      <symbol type="line" clip_to_extent="1" force_rhr="0" name="0" alpha="1">
        <layer locked="0" class="ArrowLine" enabled="1" pass="0">
          <prop v="1" k="arrow_start_width"/>
          <prop v="MM" k="arrow_start_width_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="arrow_start_width_unit_scale"/>
          <prop v="0" k="arrow_type"/>
          <prop v="1" k="arrow_width"/>
          <prop v="MM" k="arrow_width_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="arrow_width_unit_scale"/>
          <prop v="5" k="head_length"/>
          <prop v="MM" k="head_length_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="head_length_unit_scale"/>
          <prop v="5" k="head_thickness"/>
          <prop v="MM" k="head_thickness_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="head_thickness_unit_scale"/>
          <prop v="0" k="head_type"/>
          <prop v="0" k="is_curved"/>
          <prop v="0" k="is_repeated"/>
          <prop v="0" k="offset"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_unit_scale"/>
          <prop v="0" k="ring_filter"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol type="fill" clip_to_extent="1" force_rhr="0" name="@0@0" alpha="1">
            <layer locked="0" class="SimpleFill" enabled="1" pass="0">
              <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
              <prop v="77,175,74,204" k="color"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="35,35,35,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0.26" k="outline_width"/>
              <prop v="MM" k="outline_width_unit"/>
              <prop v="solid" k="style"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option type="QString" name="name" value=""/>
                  <Option name="properties"/>
                  <Option type="QString" name="type" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <labeling type="simple">
    <settings calloutType="simple">
      <text-style blendMode="0" fontStrikeout="0" multilineHeight="1" namedStyle="Bold" fontKerning="1" fontUnderline="0" fontWeight="75" textOrientation="horizontal" useSubstitutions="0" fontFamily=".AppleSystemUIFont" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontSizeUnit="MM" fieldName="if(label,label,label_magnetic)" fontSize="7" allowHtml="0" isExpression="1" textColor="0,0,0,255" fontWordSpacing="0" fontLetterSpacing="0" previewBkgrdColor="255,255,255,255" textOpacity="1" fontItalic="0" capitalization="0">
        <text-buffer bufferNoFill="1" bufferSizeUnits="MM" bufferColor="255,255,255,255" bufferDraw="1" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferOpacity="1" bufferJoinStyle="128" bufferBlendMode="0" bufferSize="1"/>
        <text-mask maskEnabled="0" maskedSymbolLayers="" maskSize="1.5" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskSizeUnits="MM" maskType="0" maskJoinStyle="128" maskOpacity="1"/>
        <background shapeRotation="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeSizeUnit="MM" shapeSizeY="0" shapeBorderWidthUnit="MM" shapeSizeType="0" shapeFillColor="255,255,255,204" shapeSizeX="0" shapeRotationType="0" shapeOffsetY="0" shapeOffsetX="0" shapeType="0" shapeRadiiY="0" shapeBorderWidth="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeJoinStyle="64" shapeOffsetUnit="MM" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeSVGFile="" shapeBlendMode="0" shapeRadiiX="0" shapeDraw="0" shapeBorderColor="128,128,128,255" shapeOpacity="1" shapeRadiiUnit="MM">
          <symbol type="marker" clip_to_extent="1" force_rhr="0" name="markerSymbol" alpha="1">
            <layer locked="0" class="SimpleMarker" enabled="1" pass="0">
              <prop v="0" k="angle"/>
              <prop v="145,82,45,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="circle" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="35,35,35,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="MM" k="outline_width_unit"/>
              <prop v="diameter" k="scale_method"/>
              <prop v="2" k="size"/>
              <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
              <prop v="MM" k="size_unit"/>
              <prop v="1" k="vertical_anchor_point"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option type="QString" name="name" value=""/>
                  <Option name="properties"/>
                  <Option type="QString" name="type" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </background>
        <shadow shadowRadiusUnit="MM" shadowOpacity="0.69999999999999996" shadowDraw="0" shadowUnder="0" shadowOffsetAngle="135" shadowRadius="1.5" shadowColor="0,0,0,255" shadowBlendMode="6" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusAlphaOnly="0" shadowOffsetDist="1" shadowOffsetGlobal="1" shadowScale="100" shadowOffsetUnit="MM" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0"/>
        <dd_properties>
          <Option type="Map">
            <Option type="QString" name="name" value=""/>
            <Option name="properties"/>
            <Option type="QString" name="type" value="collection"/>
          </Option>
        </dd_properties>
        <substitutions/>
      </text-style>
      <text-format autoWrapLength="0" reverseDirectionSymbol="0" useMaxLineLengthForAutoWrap="1" addDirectionSymbol="0" wrapChar="" placeDirectionSymbol="0" multilineAlign="0" leftDirectionSymbol="&lt;" rightDirectionSymbol=">" decimals="3" plussign="0" formatNumbers="0"/>
      <placement distMapUnitScale="3x:0,0,0,0,0,0" dist="2.5" maxCurvedCharAngleOut="-25" preserveRotation="1" polygonPlacementFlags="2" priority="5" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" yOffset="0" offsetType="0" lineAnchorType="0" placementFlags="10" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" geometryGeneratorType="PointGeometry" centroidInside="0" rotationAngle="0" geometryGenerator="" layerType="LineGeometry" fitInPolygonOnly="0" distUnits="MM" placement="2" maxCurvedCharAngleIn="25" overrunDistance="1000" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" repeatDistanceUnits="MM" geometryGeneratorEnabled="0" xOffset="0" centroidWhole="0" overrunDistanceUnit="MM" lineAnchorPercent="0.5" repeatDistance="0" quadOffset="4" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" offsetUnits="MM"/>
      <rendering obstacleType="1" fontLimitPixelSize="0" fontMaxPixelSize="10000" limitNumLabels="0" scaleMax="200000" fontMinPixelSize="3" zIndex="0" labelPerPart="0" obstacle="1" obstacleFactor="1" displayAll="1" maxNumLabels="2000" scaleMin="0" mergeLines="0" upsidedownLabels="0" drawLabels="1" scaleVisibility="1" minFeatureSize="0"/>
      <dd_properties>
        <Option type="Map">
          <Option type="QString" name="name" value=""/>
          <Option name="properties"/>
          <Option type="QString" name="type" value="collection"/>
        </Option>
      </dd_properties>
      <callout type="simple">
        <Option type="Map">
          <Option type="QString" name="anchorPoint" value="pole_of_inaccessibility"/>
          <Option type="Map" name="ddProperties">
            <Option type="QString" name="name" value=""/>
            <Option name="properties"/>
            <Option type="QString" name="type" value="collection"/>
          </Option>
          <Option type="bool" name="drawToAllParts" value="false"/>
          <Option type="QString" name="enabled" value="0"/>
          <Option type="QString" name="labelAnchorPoint" value="point_on_exterior"/>
          <Option type="QString" name="lineSymbol" value="&lt;symbol type=&quot;line&quot; clip_to_extent=&quot;1&quot; force_rhr=&quot;0&quot; name=&quot;symbol&quot; alpha=&quot;1&quot;>&lt;layer locked=&quot;0&quot; class=&quot;SimpleLine&quot; enabled=&quot;1&quot; pass=&quot;0&quot;>&lt;prop v=&quot;0&quot; k=&quot;align_dash_pattern&quot;/>&lt;prop v=&quot;square&quot; k=&quot;capstyle&quot;/>&lt;prop v=&quot;5;2&quot; k=&quot;customdash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;customdash_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;customdash_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;dash_pattern_offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;dash_pattern_offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;dash_pattern_offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;draw_inside_polygon&quot;/>&lt;prop v=&quot;bevel&quot; k=&quot;joinstyle&quot;/>&lt;prop v=&quot;60,60,60,255&quot; k=&quot;line_color&quot;/>&lt;prop v=&quot;solid&quot; k=&quot;line_style&quot;/>&lt;prop v=&quot;0.3&quot; k=&quot;line_width&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;line_width_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;ring_filter&quot;/>&lt;prop v=&quot;0&quot; k=&quot;tweak_dash_pattern_on_corners&quot;/>&lt;prop v=&quot;0&quot; k=&quot;use_custom_dash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;width_map_unit_scale&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option type=&quot;QString&quot; name=&quot;name&quot; value=&quot;&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option type=&quot;QString&quot; name=&quot;type&quot; value=&quot;collection&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>"/>
          <Option type="double" name="minLength" value="0"/>
          <Option type="QString" name="minLengthMapUnitScale" value="3x:0,0,0,0,0,0"/>
          <Option type="QString" name="minLengthUnit" value="MM"/>
          <Option type="double" name="offsetFromAnchor" value="0"/>
          <Option type="QString" name="offsetFromAnchorMapUnitScale" value="3x:0,0,0,0,0,0"/>
          <Option type="QString" name="offsetFromAnchorUnit" value="MM"/>
          <Option type="double" name="offsetFromLabel" value="0"/>
          <Option type="QString" name="offsetFromLabelMapUnitScale" value="3x:0,0,0,0,0,0"/>
          <Option type="QString" name="offsetFromLabelUnit" value="MM"/>
        </Option>
      </callout>
    </settings>
  </labeling>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <fieldConfiguration>
    <field name="label" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="bearing_magnetic" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option type="bool" name="AllowNull" value="true"/>
            <Option type="int" name="Max" value="2147483647"/>
            <Option type="int" name="Min" value="-2147483648"/>
            <Option type="int" name="Precision" value="0"/>
            <Option type="int" name="Step" value="1"/>
            <Option type="QString" name="Style" value="SpinBox"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="bearing_true" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option type="bool" name="AllowNull" value="true"/>
            <Option type="int" name="Max" value="2147483647"/>
            <Option type="int" name="Min" value="-2147483648"/>
            <Option type="int" name="Precision" value="0"/>
            <Option type="int" name="Step" value="1"/>
            <Option type="QString" name="Style" value="SpinBox"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="label_magnetic" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="label_true" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="label" index="0" name=""/>
    <alias field="bearing_magnetic" index="1" name=""/>
    <alias field="bearing_true" index="2" name=""/>
    <alias field="label_magnetic" index="3" name=""/>
    <alias field="label_true" index="4" name=""/>
  </aliases>
  <defaults>
    <default field="label" applyOnUpdate="0" expression=""/>
    <default field="bearing_magnetic" applyOnUpdate="0" expression=""/>
    <default field="bearing_true" applyOnUpdate="0" expression=""/>
    <default field="label_magnetic" applyOnUpdate="0" expression=""/>
    <default field="label_true" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint field="label" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="bearing_magnetic" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="bearing_true" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="label_magnetic" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="label_true" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="label" desc="" exp=""/>
    <constraint field="bearing_magnetic" desc="" exp=""/>
    <constraint field="bearing_true" desc="" exp=""/>
    <constraint field="label_magnetic" desc="" exp=""/>
    <constraint field="label_true" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields>
    <field type="2" name="bearing_magnetic" length="10" precision="0" subType="0" expression="round(to_magnetic(degrees(azimuth(start_point($geometry), end_point($geometry))),y($geometry),x($geometry)))" typeName="integer" comment=""/>
    <field type="2" name="bearing_true" length="10" precision="0" subType="0" expression="round(degrees(azimuth(start_point($geometry), end_point($geometry))))" typeName="integer" comment=""/>
    <field type="10" name="label_magnetic" length="0" precision="0" subType="0" expression="concat(format_number($length,2),' @ ',lpad(to_string(bearing_magnetic),3,'0'),' M')" typeName="string" comment=""/>
    <field type="10" name="label_true" length="0" precision="0" subType="0" expression="concat(format_number($length,2),' @ ',lpad(to_string(bearing_true),3,'0'),' T')" typeName="string" comment=""/>
  </expressionfields>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>1</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field editable="0" name="bearing_magnetic"/>
    <field editable="0" name="bearing_true"/>
    <field editable="1" name="label"/>
    <field editable="0" name="label_magnetic"/>
    <field editable="0" name="label_true"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="bearing_magnetic"/>
    <field labelOnTop="0" name="bearing_true"/>
    <field labelOnTop="0" name="label"/>
    <field labelOnTop="0" name="label_magnetic"/>
    <field labelOnTop="0" name="label_true"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"label_true"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
