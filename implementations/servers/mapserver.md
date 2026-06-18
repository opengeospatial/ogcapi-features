# MapServer

[MapServer](https://www.mapserver.org) 8.6.4 has support for [OGC Features API](https://www.mapserver.org/ogc/ogc_api.html) Part 1 Core, Part 2: Coordinate Reference Systems by Reference and Part 3: Filtering.
into the main code branch.

## Demo deployment

* Conformance declaration: ([JSON] https://demo.mapserver.org/cgi-bin/mapserv/localdemo/ogcapi/conformance?f=json) ([HTML] https://demo.mapserver.org/cgi-bin/mapserv/localdemo/ogcapi/conformance?f=html)

Example requests:

* All feature collections: ([JSON](https://demo.mapserver.org/cgi-bin/mapserv/localdemo/ogcapi/collections?f=json)) ([HTML](https://demo.mapserver.org/cgi-bin/mapserv/localdemo/ogcapi/collections?f=html))
* Single feature collection: ([JSON](https://demo.mapserver.org/cgi-bin/mapserv/localdemo/ogcapi/collections/countries?f=json)) ([HTML](https://demo.mapserver.org/cgi-bin/mapserv/localdemo/ogcapi/collections/countries?f=html))
* Feature collection items: ([JSON](https://demo.mapserver.org/cgi-bin/mapserv/localdemo/ogcapi/collections/countries/items?f=json)) ([HTML](https://demo.mapserver.org/cgi-bin/mapserv/localdemo/ogcapi/collections/countries/items?f=html))
* Feature collection single item: ([JSON](https://demo.mapserver.org/cgi-bin/mapserv/localdemo/ogcapi/collections/countries/items/1159320625?f=json) ([HTML](https://demo.mapserver.org/cgi-bin/mapserv/localdemo/ogcapi/collections/countries/items/1159320625?f=html))
* Feature collection: bbox query: ([JSON](https://demo.mapserver.org/cgi-bin/mapserv/localdemo/ogcapi/collections/countries/items?bbox=-152,42,-52,84&f=json)) ([HTML](https://demo.mapserver.org/cgi-bin/mapserv/localdemo/ogcapi/collections/countries/items?bbox=-152,42,-52,84&f=html))
