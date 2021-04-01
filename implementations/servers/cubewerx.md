# CubeWerx Suite

## Introduction 

For features, CubeSERV implements Parts 1, 2, 3 and 4 plus some of the proposed
extensions like geometry simplification and search.  This page, however, will
concentrate on Part 1, 2 and 3.  CubeSERV also implements a lot of other OGC
API modules.

* To test the latest version of OGC API - Features:
  * https://www.pvretano.com/cubewerx/cubeserv/default/ogcapi

* To test the other OGC API modules:
  * https://test.cubewerx.com/cubewerx/cubeserv/demo

## HTML landing page:

The following examples are performed on the [VMAP Level 0 datastore](https://www.pvretano.com/cubewerx/cubeserv/default/ogcapi/foundation).

## Example queries

* See what the server implements:
[https://www.pvretano.com/cubewerx/cubeserv/default/ogcapi/foundation/conformance?f=json](https://www.pvretano.com/cubewerx/cubeserv/default/ogcapi/foundation/conformance?f=json)

* Built up areas around Washington DC (in XML just for fun):
[https://pvretano.com/cubewerx/cubeserv/default/ogcapi/foundation/collections/builtupa_1m/items?
count=20&  
f=application/gml%2Bxml;%20version=3.2&  
bbox=-79.5854,36.8207,-74.4218,39.7519](https://pvretano.com/cubewerx/cubeserv/default/ogcapi/foundation/collections/builtupa_1m/items?count=20&f=application/gml%2Bxml;%20version=3.2&bbox=-79.5854,36.8207,-74.4218,39.7519)

* Get the list of supported CRS's:
[https://www.pvretano.com/cubewerx/cubeserv/default/ogcapi/foundation/collections/builtupa_1m?f=json](https://www.pvretano.com/cubewerx/cubeserv/default/ogcapi/foundation/collections/builtupa_1m?f=json)

* Request the features in another CRS (3857):
[https://pvretano.com/cubewerx/cubeserv/default/ogcapi/foundation/collections/builtupa_1m/items?
count=20&
f=application/gml%2Bxml;%20version=3.2
&bbox=-79.5854,36.8207,-74.4218,39.7519&
crs=http://www.opengis.net/def/crs/EPSG/0/3857](https://pvretano.com/cubewerx/cubeserv/default/ogcapi/foundation/collections/builtupa_1m/items?count=20&f=application/gml%2Bxml;%20version=3.2&bbox=-79.5854,36.8207,-74.4218,39.7519&crs=http://www.opengis.net/def/crs/EPSG/0/3857)

* Get the list of queryables for this collection:
[https://pvretano.com/cubewerx/cubeserv/default/ogcapi/foundation/collections/builtupa_1m/queryables?f=json](https://pvretano.com/cubewerx/cubeserv/default/ogcapi/foundation/collections/builtupa_1m/queryables?f=json)

* Add a CQL filter expression to the query:
[https://pvretano.com/cubewerx/cubeserv/default/ogcapi/foundation/collections/builtupa_1m/items?
count=20&
f=application/gml%2Bxml;%20version=3.2&
bbox=-79.5854,36.8207,-74.4218,39.7519&
filter-lang=cql-text&
filter=nam like 'A%'](https://pvretano.com/cubewerx/cubeserv/default/ogcapi/foundation/collections/builtupa_1m/items?count=20&f=application/gml%2Bxml;%20version=3.2&bbox=-79.5854,36.8207,-74.4218,39.7519&filter-lang=cql-text&filter=nam%20like%20%27A%25%27)

* Refine the query further by adding an additional predicate to the filter (in JSON just to show that):
[https://pvretano.com/cubewerx/cubeserv/default/ogcapi/foundation/collections/builtupa_1m/items?
count=20&
f=json&
bbox=-79.5854,36.8207,-74.4218,39.7519&
filter-lang=cql-text&
filter=nam like 'A%'and fac_id>140](https://pvretano.com/cubewerx/cubeserv/default/ogcapi/foundation/collections/builtupa_1m/items?count=20&f=json&bbox=-79.5854,36.8207,-74.4218,39.7519&filter-lang=cql-text&filter=nam%20like%20%27A%25%27%20and%20fac_id%3E140)

