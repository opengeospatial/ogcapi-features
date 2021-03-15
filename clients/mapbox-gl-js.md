# Mapbox GL JS

This page shows an example how to connect with Mapbox GL JS to an API that implements OGC API - Features - Part 1: Core.

## Links

- Open the example as a [map](https://ogc.portele.de/maps/mapbox-gl-js-airports.html)
- Open the example in [Codepen](https://codepen.io/cportele/pen/GRNPWyR)
- [GeoJSON documentation from Mapbox](https://docs.mapbox.com/mapbox-gl-js/api/sources/#geojsonsource)

## Software version

This example uses Mapbox GL JS 1.13.0.

## Required and supported Conformance classes

The API must support the [Core](http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/core) and [GeoJSON](http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/geojson) conformance classes.

Mapbox GL JS has no built-in support for OGC API Features, so the feature data for each collection has to be accessed directly as GeoJSON. For collections that have a high feature count that is larger than the maximum value for the `limit` parameter supported by the API, this is a limitation since not all features can be accessed in a single request. For datasets and collections with a large number of features, the use of vector tiles as supported by OGC API Tiles is recommended.

## Description

To add GeoJSON features accessed from an API implementing OGC API Features, access the features from a Features resource (relative path `collections/{collectionId}/items` from the Landing Page) with a limit value that is sufficient for the number of features in the collection. In this example, the URL is `https://demo.ldproxy.net/zoomstack/collections/airports/items?limit=100` to retrieve the airports in Great Britain. The response is a GeoJSON feature collection that can be added to the Mapbox GL JS map.

Here is an example using the Fetch API:

```javascript
(async () => {
   const airports = await fetch('https://demo.ldproxy.net/zoomstack/collections/airports/items?limit=100', {
   headers: {
      'Accept': 'application/geo+json'
   }
   }).then(response => response.json());

   map.addSource('airports', {
      type: 'geojson',
      data: airports
   });

   map.addLayer({
      'id': 'airports',
      'type': 'symbol',
      'source': 'airports',
      "layout": {
         "icon-image": "topo_airport-15"
      }
   });
})();
```

Open the complete HTML document as a [map](https://ogc.portele.de/maps/mapbox-gl-js-airports.html) or in [Codepen](https://codepen.io/cportele/pen/GRNPWyR).
