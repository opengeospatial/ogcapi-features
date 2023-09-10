# MapServer

[MapServer](https://www.mapserver.org) added [OGC Features API](https://www.mapserver.org/ogc/ogc_api.html) Part 1 Core support in version 8.0. 
OGC API - Features - Part 2: Coordinate Reference Systems by Reference will be part of the upcoming MapServer 8.2 release and has been [merged](https://github.com/MapServer/MapServer/pull/6893)
into the main code branch.

## Demo deployment

Example requests:

* All feature collections: ([JSON](https://demo.mapserver.org/cgi-bin/mapserv/localdemo/ogcapi/collections?f=json)) ([HTML](https://demo.mapserver.org/cgi-bin/mapserv/localdemo/ogcapi/collections?f=html))
* Single feature collection: ([JSON](https://demo.mapserver.org/cgi-bin/mapserv/localdemo/ogcapi/collections/countries?f=json)) ([HTML](https://demo.mapserver.org/cgi-bin/mapserv/localdemo/ogcapi/collections/countries?f=html))
* Feature collection items: ([JSON](https://demo.mapserver.org/cgi-bin/mapserv/localdemo/ogcapi/collections/countries/items?f=json)) ([HTML](https://demo.mapserver.org/cgi-bin/mapserv/localdemo/ogcapi/collections/countries/items?f=html))
* Feature collection single item: ([JSON](https://demo.mapserver.org/cgi-bin/mapserv/localdemo/ogcapi/collections/countries/items/1159320625?f=json) ([HTML](https://demo.mapserver.org/cgi-bin/mapserv/localdemo/ogcapi/collections/countries/items/1159320625?f=html))
* Feature collection: bbox query: ([JSON](https://demo.mapserver.org/cgi-bin/mapserv/localdemo/ogcapi/collections/countries/items?bbox=-152,42,-52,84&f=json)) ([HTML](https://demo.mapserver.org/cgi-bin/mapserv/localdemo/ogcapi/collections/countries/items?bbox=-152,42,-52,84&f=html))
