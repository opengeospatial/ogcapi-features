# pygeoapi

[pygeoapi](https://pygeoapi.io/) is implemented in Python, and supports JSON and HTML responses.

## Demo deployment

Example requests:

* OpenAPI 3 document: ([JSON](https://demo.pygeoapi.io/master/?f=json)) ([HTML](https://demo.pygeoapi.io/master/))
* All feature collections: ([JSON](https://demo.pygeoapi.io/master/collections?f=json)) ([HTML](https://demo.pygeoapi.io/master/collections?f=html))
* Single feature collection: ([JSON](https://demo.pygeoapi.io/master/collections/utah_city_locations?f=json)) ([HTML](https://demo.pygeoapi.io/master/collections/utah_city_locations?f=html))
* Feature collection items: ([JSON](https://demo.pygeoapi.io/master/collections/utah_city_locations/items?f=json)) ([HTML](https://demo.pygeoapi.io/master/collections/utah_city_locations/items?f=html))
* Feature collection single item: ([JSON](https://demo.pygeoapi.io/master/collections/utah_city_locations/items/Fairfield?f=json) ([HTML](https://demo.pygeoapi.io/master/collections/utah_city_locations/items/Fairfield?f=html))
* Feature collection: bbox query: ([JSON](https://demo.pygeoapi.io/master/collections/lakes/items?bbox=-152,42,-52,84&f=json)) ([HTML](https://demo.pygeoapi.io/master/collections/lakes/items?bbox=-152,42,-52,84&f=html))

## [British Geological Survey](https://www.bgs.ac.uk/)

Production deployment using an custom jinja template running on Kubernetes at https://ogcapi.bgs.ac.uk/. Code available at https://github.com/BritishGeologicalSurvey/bgs-pygeoapi.

Example requests:

* OpenAPI 3 document: ([JSON](https://ogcapi.bgs.ac.uk/?f=json)) ([HTML](https://ogcapi.bgs.ac.uk/))
* All feature collections: ([JSON](https://ogcapi.bgs.ac.uk/collections?f=json)) ([HTML](https://ogcapi.bgs.ac.uk/collections))
* Single feature collection: ([JSON](https://ogcapi.bgs.ac.uk/collections/BGSGeology625kBedrock?f=json)) ([HTML](https://ogcapi.bgs.ac.uk/collections/BGSGeology625kBedrock))
* Feature collection items: ([JSON](https://ogcapi.bgs.ac.uk/collections/BGSGeology625kBedrock/items?f=json)) ([HTML](https://ogcapi.bgs.ac.uk/collections/BGSGeology625kBedrock/items))
* Feature collection single item: ([JSON](https://ogcapi.bgs.ac.uk/collections/BGSGeology625kBedrock/items/7?f=json) ([HTML](https://ogcapi.bgs.ac.uk/collections/BGSGeology625kBedrock/items/7))
* * Feature collection: bbox query: ([JSON](https://ogcapi.bgs.ac.uk/collections/BGSGeology625kBedrock/items/?bbox=0,51,0.5,51.5&f=json)) ([HTML](https://ogcapi.bgs.ac.uk/collections/BGSGeology625kBedrock/items/?bbox=0,51,0.5,51.5&f=html))
* SpatioTemporal Assets: ([JSON](https://ogcapi.bgs.ac.uk/stac/ogl-data?f=json) ([HTML](https://ogcapi.bgs.ac.uk/stac/ogl-data))

## Meteorological Service of Canada

The Meteorological Service of Canada uses pygeoapi in production at https://api.weather.gc.ca.
