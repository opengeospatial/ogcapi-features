# ArcGIS API for JavaScript

This page shows an example how to connect with the ArcGIS API for JavaScript to an API that implements OGC API - Features - Part 1: Core.

## Links

- Open the example as a [map](https://ogc.portele.de/maps/arcgis-js-vineyards.html)
- Open the example in [Codepen](https://codepen.io/cportele/pen/ZEBVpby)
- The [example from Esri](https://developers.arcgis.com/javascript/latest/sample-code/layers-ogcfeaturelayer/) that was used as a starting point
- [OGCFeatureLayer documentation from Esri](https://developers.arcgis.com/javascript/latest/api-reference/esri-layers-OGCFeatureLayer.html)
- [ArcGIS API for JavaScript - Licensing & Attribution requirements](https://developers.arcgis.com/javascript/latest/licensing/)

## Software version

This example uses ArcGIS API for JavaScript 4.18.

## Required and supported Conformance classes

The API must support the [Core](http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/core) and [GeoJSON](http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/geojson) conformance classes.

The CRS conformance class from Part 2 (Coordinate Reference Systems by Reference) is not supported. ArcGIS API for JavaScript will convert the coordinates to other coordinate reference systems as needed.

## Description

A collection in an API implementing OGC API Features is represented in the ArcGIS API for JavaScript as an [OGCFeatureLayer](https://developers.arcgis.com/javascript/latest/api-reference/esri-layers-OGCFeatureLayer.html).

The definition below creates a feature layer for the use in a map from the vineyard features in this API: https://demo.ldproxy.net/vineyards

Open the complete HTML document as a [map](https://ogc.portele.de/maps/arcgis-js-vineyards.html) or in [Codepen](https://codepen.io/cportele/pen/ZEBVpby).

```javascript
const vineyards = new OGCFeatureLayer({
   // URI of the Landing Page resource
   url: "https://demo.ldproxy.net/vineyards", 
   // identifier of the collection
   collectionId: "vineyards", 
   // the layer title is derived from the API
   // displayField is the property used to label features, e.g. in popups
   displayField: "name",
   // show the name of the vineyard in larger scales
   labelingInfo: [{
      labelExpressionInfo: {
         expression: "$feature.NAME"
      },
      symbol: {
         type: "text",
         color: "black",
         haloSize: 1,
         haloColor: "white"
      },
      maxScale: 0,
      minScale: 100000
   }],
   // display the attribution
   copyright: "Landwirtschaftskammer RLP (2020), dl-de/by-2-0, <a href='http://weinlagen.lwk-rlp.de/'' target='_blank'>weinlagen.lwk-rlp.de</a>, <a href='http://weinlagen.lwk-rlp.de/portal/nutzungsbedingungen/gewaehrleistung-haftung.html' target='_blank'>Regelungen zu Gewährleistung und Haftung</a>",
   // hide the vineyards in very small scales
   minScale: 5000000,
   // define a simple rendering
   renderer: {
      type: "simple",
      symbol: {
         type: "simple-fill",
         style: "solid",
         color: "green",
         outline: {
            width: "0"
         }
      }
   },
   opacity: 0.6
});
```
