# pygeoapi

[pygeoapi](https://geopython.github.io/pygeoapi) is implemented in Python, and supports JSON and HTML responses.

## Demo deployment

Example requests:

* OpenAPI 3 document: ([JSON](https://demo.pygeoapi.io/master/?f=json)) ([HTML](https://demo.pygeoapi.io/master/))
* All feature collections: ([JSON](https://demo.pygeoapi.io/master/collections?f=json)) ([HTML](https://demo.pygeoapi.io/master/collections?f=html))
* Single feature collection: ([JSON](https://demo.pygeoapi.io/master/collections/utah_city_locations?f=json)) ([HTML](https://demo.pygeoapi.io/master/collections/utah_city_locations?f=html))
* Feature collection items: ([JSON](https://demo.pygeoapi.io/master/collections/utah_city_locations/items?f=json)) ([HTML](https://demo.pygeoapi.io/master/collections/utah_city_locations/items?f=html))
* Feature collection single item: ([JSON](https://demo.pygeoapi.io/master/collections/utah_city_locations/items/Fairfield?f=json) ([HTML](https://demo.pygeoapi.io/master/collections/utah_city_locations/items/Fairfield?f=html))
* Feature collection: bbox query: ([JSON](https://demo.pygeoapi.io/master/collections/lakes/items?bbox=-152,42,-52,84&f=json)) ([HTML](https://demo.pygeoapi.io/master/collections/lakes/items?bbox=-152,42,-52,84&f=html))

## [British Geological Survey](https://www.bgs.ac.uk/)

Demo deployment using an amended [pygeoapi-skin-dashboard](https://github.com/BritishGeologicalSurvey/pygeoapi-skin-dashboard) running on Kubenetes at https://osgeodev.bgs.ac.uk/pygeoapi/. Code available at https://github.com/BritishGeologicalSurvey/bgs-pygeoapi.

Example requests:

* OpenAPI 3 document: ([JSON](https://osgeodev.bgs.ac.uk/pygeoapi/?f=json)) ([HTML](https://osgeodev.bgs.ac.uk/pygeoapi/))
* All feature collections: ([JSON](https://osgeodev.bgs.ac.uk/pygeoapi/collections?f=json)) ([HTML](https://osgeodev.bgs.ac.uk/pygeoapi/collections))
* Single feature collection: ([JSON](https://osgeodev.bgs.ac.uk/pygeoapi/collections/BGSGeology625kBedrock?f=json)) ([HTML](https://osgeodev.bgs.ac.uk/pygeoapi/collections/BGSGeology625kBedrock))
* Feature collection items: ([JSON](https://osgeodev.bgs.ac.uk/pygeoapi/collections/BGSGeology625kBedrock/items?f=json)) ([HTML](https://osgeodev.bgs.ac.uk/pygeoapi/collections/BGSGeology625kBedrock/items))
* Feature collection single item: ([JSON](https://osgeodev.bgs.ac.uk/pygeoapi/collections/BGSGeology625kBedrock/items/7?f=json) ([HTML](https://osgeodev.bgs.ac.uk/pygeoapi/collections/BGSGeology625kBedrock/items/7))

## Meteorological Service of Canada

The Meteorological Service of Canada uses pygeoapi in production at https://geo.weather.gc.ca/geomet/features.
