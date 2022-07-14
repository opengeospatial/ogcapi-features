# Leaflet.FeatureGroup.OGCAPI

Leaflet supports loading GeoJSON data, but the Leaflet plugin "Leaflet.FeatureGroup.OGCAPI" offers a more complete implementation - with details such as using the bbox and attribution found in the collection metadata.

## Links

- The plugin is available in a gitlab repository at [https://gitlab.com/IvanSanchez/leaflet.featuregroup.ogcapi](https://gitlab.com/IvanSanchez/leaflet.featuregroup.ogcapi)
- There is a live demo at [https://ivansanchez.gitlab.io/leaflet.featuregroup.ogcapi/demo.html](https://ivansanchez.gitlab.io/leaflet.featuregroup.ogcapi/demo.html)

## Software version

This example uses Leaflet 1.8.0, Leaflet.FeatureGroup.OGCAPI 0.1.0 and Leaflet-GeoMan 2.13.0.

## Required and supported Conformance classes

The plugin supports the [Core](http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/core) and [GeoJSON](http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/geojson) conformance classes.

Neither Part 2 (CRSs) nor Part 3 (CQL) are supported.

There is partial support for the Part 4 draft: the plugin offers basic capabilities
to create, replace, and remove features. These capabilities do not have a user
interface - developers are encouraged to use other Leaflet plugins such as Leafler-Draw
or Leaflet-GeoMan to create this UI.

## Description

The plugin offers a new class (`L.FeatureGroup.OGCAPI`) and corresponding factory method (`L.featureGroup.ogcApi`). To instantiate it, provide the URL to the landing page and the **ID** (not the name, not the description) of the desired collection.

The functionality of `L.GeoJSON` can be used as well. Most importantly, this includes the `style` and `pointToLayer` options to style the features, and the `onEachFeature` option to modify or attach interactivity to the symbolized features, e.g.:

```javascript
var trees = L.featureGroup.ogcApi("https://maps.ecere.com/ogcapi/", {
      collection: "SanDiegoCDB:Trees",
      onEachFeature: function (feat, layer) {
         layer.bindPopup("Feature ID" + feat.id);
      },
   })
   .addTo(map);
```

The [gitlab repository](https://gitlab.com/IvanSanchez/leaflet.featuregroup.ogcapi) contains a complete demo, including loading the plugin, and a demo implementing some Part 4 operations which leverages Leaflet-GeoMan as the UI.
