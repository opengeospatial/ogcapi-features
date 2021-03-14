# OpenLayers

This page shows an example how to connect with OpenLayers to an API that implements OGC API - Features - Part 1: Core.

## Links

- Open the example as a [map](https://ogc.portele.de/maps/openlayers-airports.html)
- Open the example in [Codepen](https://codepen.io/cportele/pen/OJbrgKe)
- [GeoJSON documentation from OpenLayers](https://openlayers.org/en/latest/apidoc/module-ol_format_GeoJSON-GeoJSON.html)
- This [example from the OpenLayers documentation](https://openlayers.org/en/latest/examples/geojson.html) was used as a starting point

## Software version

This example uses Leaflet 6.5.0.

## Required and supported Conformance classes

The API must support the [Core](http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/core) and [GeoJSON](http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/geojson) conformance classes.

OpenLayers has no built-in support for OGC API Features, so the feature data for each collection has to be accessed directly as GeoJSON. For collections that have a high feature count that is larger than the maximum value for the `limit` parameter supported by the API, this is a limitation since not all features can be accessed in a single request. For datasets and collections with a large number of features, the use of vector tiles as supported by OGC API Tiles is recommended.

## Description

To add GeoJSON features accessed from an API implementing OGC API Features, access the features from a Features resource (relative path `collections/{collectionId}/items` from the Landing Page) with a limit value that is sufficient for the number of features in the collection. In this example, the URL is `https://demo.ldproxy.net/zoomstack/collections/airports/items?limit=100` to retrieve the airports in Great Britain. The response is a GeoJSON feature collection that can be added to the OpenLayers map.

Most maps will use WebMercator as the projection, so the GeoJSON feature geometries need to be projected from `EPSG:4326` to `EPSG:3857`.

Here is an example using the Fetch API:

```javascript
(async () => {
  const airports = await fetch('https://demo.ldproxy.net/zoomstack/collections/airports/items?limit=100', {
    headers: {
      'Accept': 'application/geo+json'
    }
  }).then(response => response.json());

  map.addLayer(new ol.layer.Vector({
    source: new ol.source.Vector({
      features: new ol.format.GeoJSON().readFeatures(airports, { featureProjection: 'EPSG:3857' }),
      attributions: 'Contains OS data &copy; Crown copyright and database right 2021.'
    })
  }));
})();
```

Open the complete HTML document as a [map](https://ogc.portele.de/maps/openlayers-airports.html) or in [Codepen](https://codepen.io/cportele/pen/OJbrgKe).
