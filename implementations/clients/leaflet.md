# Leaflet

This page shows an example how to connect with Leaflet to an API that implements OGC API - Features - Part 1: Core.

## Links

- Open the example as a [map](https://ogc.portele.de/maps/leaflet-airports.html)
- Open the example in [Codepen](https://codepen.io/cportele/pen/VwmqPWy)
- [GeoJSON documentation from Leaflet](https://leafletjs.com/reference-1.7.1.html#geojson)
- This [tutorial from the Leaflet documentation](https://leafletjs.com/examples/geojson/) may also be helpful

## Software version

This example uses Leaflet 1.7.1.

## Required and supported Conformance classes

The API must support the [Core](http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/core) and [GeoJSON](http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/geojson) conformance classes.

Leaflet has no built-in support for OGC API Features, so the feature data for each collection has to be accessed directly as GeoJSON. For collections that have a high feature count that is larger than the maximum value for the `limit` parameter supported by the API, this is a limitation since not all features can be accessed in a single request. For datasets and collections with a large number of features, the use of vector tiles as supported by OGC API Tiles is recommended.

## Description

To add GeoJSON features accessed from an API implementing OGC API Features, access the features from a Features resource (relative path `collections/{collectionId}/items` from the Landing Page) with a limit value that is sufficient for the number of features in the collection. In this example, the URL is `https://demo.ldproxy.net/zoomstack/collections/airports/items?limit=100` to retrieve the airports in Great Britain. The response is a GeoJSON feature collection that can be added to the Leaflet map.

Here is an example using the Fetch API:

```javascript
(async () => {
   const airports = await fetch('https://demo.ldproxy.net/zoomstack/collections/airports/items?limit=100', {
      headers: {
        'Accept': 'application/geo+json'
      }
   }).then(response => response.json());

   L.geoJSON(airports).addTo(map);
})();
```

Open the complete HTML document as a [map](https://ogc.portele.de/maps/leaflet-airports.html) or in [Codepen](https://codepen.io/cportele/pen/VwmqPWy).