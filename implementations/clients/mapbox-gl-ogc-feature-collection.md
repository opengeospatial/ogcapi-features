# mapbox-gl-ogc-feature-collection

Mapbox GL JS supports loading GeoJSON data, but `mapbox-gl-ogc-feature-collection` offers a more complete implementation - with details such as using the bbox and filtering.

## Links

- The plugin is available in a gitlab repository at [https://github.com/mkeller3/mapbox-gl-ogc-feature-collection](https://github.com/mkeller3/mapbox-gl-ogc-feature-collection)
- There is a live demo at [https://mkeller3.github.io/mapbox-gl-ogc-feature-collection/](https://mkeller3.github.io/mapbox-gl-ogc-feature-collection/)

## Software version

This example uses Maplibre GL JS 2.4.0.

## Required and supported Conformance classes

The plugin supports the [Core](http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/core), [CRS](https://docs.ogc.org/DRAFTS/18-058r1.html), [Filtering](https://docs.ogc.org/DRAFTS/19-079r1.html), and [GeoJSON](http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/geojson) conformance classes.

## Description

The package offers a new class (`OGCFeatureCollection`) To instantiate it, provide the URL to the landing page and the **ID** (not the name, not the description) of the desired collection.

```javascript
import OGCFeatureCollection from 'mapbox-gl-ogc-feature-collection'

map.on('load', () => {
    const sourceId = 'collection-src'

    new OGCFeatureCollection(sourceId, map, {
        url: 'https://demo.pygeoapi.io/stable',
        collectionId: 'lakes',
        limit: 10000
    })

    map.addLayer({
        'id': 'lyr',
        'source': sourceId,
        'type': 'fill',
        'paint': {
            'fill-color': '#B42222',
            'fill-opacity': 0.7
        }
    })
})
```

The [gitlab repository](https://github.com/mkeller3/mapbox-gl-ogc-feature-collection) contains a complete demo, including loading the class, and a demo.
