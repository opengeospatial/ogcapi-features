# Implementations

## Overview

This page points to servers implementing the OGC API - Features - Part 1: Core specification and extensions (e.g. Part 2, Part 3, etc.) thereof.  If you feel so inclined, feel free to indicate whether your server is listed in the compliance database (see Issue #416).

We may start managing this page a little more actively from now on (22-JUL-2020) so please include a contact email with your listing so that we can get in touch with you should we test your server and find out that it is unreachable.

## Implementations:

Servers:

* [ldproxy](#ldproxy), portele [at] interactive-instruments.de
* [CubeWerx Inc.](#cubeWerx), pvretano [at] cubewerx.com
* [GeoServer](#geoserver)
* [pygeoapi](#pygeoapi)
* [jivan](#jivan)
* [sofp](#sofp)
* [STAC](#STAC)
* [nls-fi](#nls-fi)
* [QGIS](#QGIS)
* [SDI Rhineland-Palatinate - mapbender2](#sdi-rhineland-palatinate---mapbender2)

Clients:
* [go-wfs3-client](https://github.com/ischneider/go-wfs3-client)
* [GDAL/OGR OGC API - Features driver](https://gdal.org/drivers/vector/oapif.html)
* [OWSLib WFS 3.0 client](https://geopython.github.io/OWSLib)
* [STAC](#STAC)
* [QGIS](#QGIS)
* [ogcapi-js](#ogcapi-js)
* [FME](#FME)

## ldproxy

The following APIs are available as an [OGC Reference Implementation](https://www.opengeospatial.org/resource/products/details/?pid=1598). The APIs support Features part 1, 2 and 3. They also implement drafts of OGC API Tiles and Styles.

* Daraa dataset (used in several OGC testbeds and pilots):
  * OpenAPI definition: https://demo.ldproxy.net/daraa/api
  * Landing page: https://demo.ldproxy.net/daraa
* Vineyards in Rhineland-Palatinate dataset:
  * OpenAPI definition: https://demo.ldproxy.net/vineyards/api
  * Landing page: https://demo.ldproxy.net/vineyards

Most resources are available as HTML and JSON. Add `f=json` or `f=html` to override HTTP content negotiation.

Sample requests:

* A conformance declaration: https://demo.ldproxy.net/vineyards/conformance
* Available collections: https://demo.ldproxy.net/daraa/collections
* A collection in a dataset (agricultural surfaces): https://demo.ldproxy.net/daraa/collections/AgricultureSrf
* First page of features in a collection (ground transportation points): https://demo.ldproxy.net/daraa/collections/TransportationGroundPnt/items
* The same features in Web Mercator: https://demo.ldproxy.net/daraa/collections/TransportationGroundPnt/items?f=json&crs=http%3A%2F%2Fwww.opengis.net%2Fdef%2Fcrs%2FEPSG%2F0%2F3857
* A single feature (a cemetery): https://demo.ldproxy.net/daraa/collections/CulturePnt/items/1
* Queryable attributes of a collection (ground transportation curves): https://demo.ldproxy.net/daraa/collections/TransportationGroundCrv/queryables
* JSON Schema of the features of a collection (ground transportation curves): https://demo.ldproxy.net/daraa/collections/TransportationGroundCrv/schema
* Features in a spatial area (vineyards between 7.0° and 7.1° East and between 49.9° and 50.0° North): https://demo.ldproxy.net/vineyards/collections/vineyards/items?bbox=7.0%2C49.9%2C7.1%2C50.0
* Features selected by an attribute value (vineyards in Lieser): https://demo.ldproxy.net/vineyards/collections/vineyards/items?village=Lieser
* Same query using a CQL filter: https://demo.ldproxy.net/vineyards/collections/vineyards/items?filter=village%3D%27Lieser%27
* Features selected by time (ground transportation curves last updated in 2011/2012): https://demo.ldproxy.net/daraa/collections/TransportationGroundCrv/items?datetime=2011-01-01/2012-12-31
* Features selected by space, time and attributes (ground transportation curves last updated in 2011/2012, in the city of Daraa, restricted to roads): https://demo.ldproxy.net/daraa/collections/TransportationGroundCrv/items?F_CODE=AP030&bbox=36.08%2C32.59%2C36.12%2C32.64&datetime=2011-01-01%2F2012-12-31

## CubeWerx Inc.

The following server implements a good portion of the current draft part 1
standard.  Just to illustrate that GML may still be used, and to contrast
the interactive instruments examples, these queries will return GML rather
than JSON (although GeoJSON can be returned by requesting the appropriate
MIME type).

Like the interactive instruments server, this 3.0 alpha implementation is a
facade sitting on top of our previous WFS 2.X implementation.

HTML landing page:
* http://www.pvretano.com/cubewerx/cubeserv/default/wfs/3.0/foundation
* http://www.pvretano.com/cubewerx/cubeserv/default/wfs/3.0/usbuildingfootprints

Here are some example requests for features using GML v3.2 output.

* Built up areas around Washington DC:
[http://www.pvretano.com/cubewerx/cubeserv/default/wfs/3.0/foundation/collections/builtupa_1m/items?  
count=20&  
f=application/gml%2Bxml;%20version=3.2&  
bbox=36.8207,-79.5854,39.7519,-74.4218](http://www.pvretano.com/cubewerx/cubeserv/default/wfs/3.0/foundation/collections/builtupa_1m/items?count=20&f=application/gml%2Bxml;%20version=3.2&bbox=36.8207,-79.5854,39.7519,-74.4218)

* ... and the corresponding building footprints
[http://www.pvretano.com/cubewerx/cubeserv/default/wfs/3.0/usbuildingfootprints/collections/US_Building_Footprints/items?count=1000&f=application/gml%2Bxml;%20version=3.2&bbox=36.8207,-79.5854,39.7519,-74.4218](http://www.pvretano.com/cubewerx/cubeserv/default/wfs/3.0/usbuildingfootprints/collections/US_Building_Footprints/items?count=1000&f=application/gml%2Bxml;%20version=3.2&bbox=36.8207,-79.5854,39.7519,-74.4218)

* Same filter, just to determine the number of built up areas:  
[http://www.pvretano.com/cubewerx/cubeserv/default/wfs/3.0/foundation/collections/builtupa_1m/items?  
resultType=hits&  
f=application/gml%2Bxml;%20version=3.2&  
bbox=36.8207,-79.5854,39.7519,-74.4218](http://www.pvretano.com/cubewerx/cubeserv/default/wfs/3.0/foundation/collections/builtupa_1m/items?resultType=hits&f=application/gml%2Bxml;%20version=3.2&bbox=36.8207,-79.5854,39.7519,-74.4218)

* All municipalities that start with "Wash":  
[http://www.pvretano.com/cubewerx/cubeserv/default/wfs/3.0/foundation/collections/builtupa_1m/items?  
f=application/gml%2Bxml;%20version=3.2&  
nam=Wash\*](http://www.pvretano.com/cubewerx/cubeserv/default/wfs/3.0/foundation/collections/builtupa_1m/items?&f=application/gml%2Bxml;%20version=3.2&nam=Wash*)

## GeoServer

An complete implementation of the Features API specification is available at https://vtp2.geo-solutions.it/geoserver/web/
At the time of writing, it supports core, HTML, GML and GeoJSON (as well as other output formats), queriables, CQL extensions, tiles.

## pygeoapi

[pygeoapi](https://geopython.github.io/pygeoapi) implements the majority of the current draft.  pygeoapi is implemented in Python, and supports JSON and HTML responses.

### Example requests:
* OpenAPI 3 document: ([JSON](https://demo.pygeoapi.io/master/?f=json)) ([HTML](https://demo.pygeoapi.io/master/))
* All feature collections: ([JSON](https://demo.pygeoapi.io/master/collections?f=json)) ([HTML](https://demo.pygeoapi.io/master/collections?f=html))
* Single feature collection: ([JSON](https://demo.pygeoapi.io/master/collections/utah_city_locations?f=json)) ([HTML](https://demo.pygeoapi.io/master/collections/utah_city_locations?f=html))
* Feature collection items: ([JSON](https://demo.pygeoapi.io/master/collections/utah_city_locations/items?f=json)) ([HTML](https://demo.pygeoapi.io/master/collections/utah_city_locations/items?f=html))
* Feature collection single item: ([JSON](https://demo.pygeoapi.io/master/collections/utah_city_locations/items/Fairfield?f=json) ([HTML](https://demo.pygeoapi.io/master/collections/utah_city_locations/items/Fairfield?f=html))
* Feature collection: bbox query: ([JSON](https://demo.pygeoapi.io/master/collections/lakes/items?bbox=-152,42,-52,84&f=json)) ([HTML](https://demo.pygeoapi.io/master/collections/lakes/items?bbox=-152,42,-52,84&f=html))

### [British Geological Survey](https://www.bgs.ac.uk/)

Demo deployment using an ammeded [pygeoapi-skin-dashboard](https://github.com/BritishGeologicalSurvey/pygeoapi-skin-dashboard) running on Kubenetes at https://osgeodev.bgs.ac.uk/pygeoapi/. Code available @ https://github.com/BritishGeologicalSurvey/bgs-pygeoapi

#### Example requests:
* OpenAPI 3 document: ([JSON](https://osgeodev.bgs.ac.uk/pygeoapi/?f=json)) ([HTML](https://osgeodev.bgs.ac.uk/pygeoapi/))
* All feature collections: ([JSON](https://osgeodev.bgs.ac.uk/pygeoapi/collections?f=json)) ([HTML](https://osgeodev.bgs.ac.uk/pygeoapi/collections))
* Single feature collection: ([JSON](https://osgeodev.bgs.ac.uk/pygeoapi/collections/BGSGeology625kBedrock?f=json)) ([HTML](https://osgeodev.bgs.ac.uk/pygeoapi/collections/BGSGeology625kBedrock))
* Feature collection items: ([JSON](https://osgeodev.bgs.ac.uk/pygeoapi/collections/BGSGeology625kBedrock/items?f=json)) ([HTML](https://osgeodev.bgs.ac.uk/pygeoapi/collections/BGSGeology625kBedrock/items))
* Feature collection single item: ([JSON](https://osgeodev.bgs.ac.uk/pygeoapi/collections/BGSGeology625kBedrock/items/7?f=json) ([HTML](https://osgeodev.bgs.ac.uk/pygeoapi/collections/BGSGeology625kBedrock/items/7))

### Meteorological Service of Canada

The Meteorological Service of Canada uses pygeoapi in production at https://geo.weather.gc.ca/geomet/features


## jivan

[jivan](https://github.com/go-spatial/jivan) implements the majority of the current draft.  jivan is implemented in Go, and supports JSON and HTML responses.

### Example requests:
* OpenAPI 3 document: http://features.gospatial.org/api
* All feature collections: http://features.gospatial.org/collections ([HTML](http://features.gospatial.org/collections?f=text/html))
* Single feature collection: http://features.gospatial.org/collections/amenities_points ([HTML](http://features.gospatial.org/collections/amenities_points?f=text/html))
* Feature collection items: http://features.gospatial.org/collections/amenities_points/items ([HTML](http://features.gospatial.org/collections/amenities_points/items?f=text/html))
* Feature collection single item: http://features.gospatial.org/collections/amenities_points/items/2 ([HTML](http://features.gospatial.org/collections/amenities_points/items/2?f=text/html))
* Feature collection: populated places in Canada: http://features.gospatial.org/collections/amenities_points/items?amenity=fast_food


## sofp

SOFP is an acronym for Simple Observation Features Project. The server carrying the same name is being developed as a part of a joint venture between Vaisala, Finnish Meteorological Institute and Spatineo. The goal is to test WFS 3.0 and a simple feature encoding for observations and measurements (https://github.com/opengeospatial/omsf-profile).

The server is implemented in TypeScript and runs in NodeJS. The architecture allows plugging in any backend or backends, also written in TypeScript. This makes it possible to integrate into existing infrastructure. The open source server includes only an example backend that serves features from a local GeoJSON file. The core server and the example backend are available on dockerhub: https://hub.docker.com/u/sofp

SOFP focuses also on usability and browseability. Using content-negotiation, the server is easy to browse using a typical browser. The server also produces map previews of data returned by the server when data is retrieved as HTML.

Code is available on GitHub:
* SOFP Core (the server itself): https://github.com/vaisala-oss/sofp-core
* SOFP Library (shared code between backends and the core): https://github.com/vaisala-oss/sofp-lib
* SOFP Example Backend: https://github.com/vaisala-oss/sofp-example-backend
* FMI SmartMet Backend: https://github.com/fmidev/smartmet-sofp-backend

Finnish Meteorological Institute hosts a demo server at http://beta.fmi.fi/data/3/wfs/sofp

### Example requests:
* OpenAPI 3 document: http://beta.fmi.fi/data/3/wfs/sofp/api.json
* OpenAPI 3 as HTML: http://beta.fmi.fi/data/3/wfs/sofp/api.html
* All feature collections: http://beta.fmi.fi/data/3/wfs/sofp/collections
* Weather observations: http://beta.fmi.fi/data/3/wfs/sofp/collections/opendata_1h/items?observedPropertyName=Temperature,WindSpeedMS,WindDirection&bbox=24.5,60,25.5,60.5&limit=100

## STAC

The [SpatioTemporal Asset Catalog (STAC) specification](https://github.com/radiantearth/stac-spec), more precisely the [STAC API specification](https://github.com/radiantearth/stac-spec/tree/master/api-spec), is based on WFS 3 API. Thus STAC API is a superset of the core WFS3 API, in that WFS 3 defines many of the endpoints that STAC uses. A STAC API should be compatible and usable with WFS3 clients and a STAC server should also be a valid WFS3 server. However, WFS 3 is still under development and while STAC tries to stay in sync with WFS3 developments, there may be discrepencies prior to final versions of both specifications.

### Implementations
* Client: [STAC Browser](https://github.com/radiantearth/stac-browser/)
* Server: [sat-api](https://github.com/sat-utils/sat-api)

See the [STAC implementations page](https://github.com/radiantearth/stac-spec/blob/master/implementations.md#api-active-catalog-examples) for more implementations.

## nls-fi
Topographical database of National Land Survey of Finland as an OGC API - Features with some 130 collections. Powered by a server called hakuna-wfs3, implemented in Java at the NLS-Finland. Currently supporting JSON/GeoJSON (and also MVT for /tiles). Pagination via primary keys, fully streaming approach.

### Example requests:
* OpenAPI document: https://beta-paikkatieto.maanmittauslaitos.fi/maastotiedot/wfs3/v1/api
* First 10 roadlinks: https://beta-paikkatieto.maanmittauslaitos.fi/maastotiedot/wfs3/v1/collections/tieviiva/items?limit=10
* Roadlink with id 11: https://beta-paikkatieto.maanmittauslaitos.fi/maastotiedot/wfs3/v1/collections/tieviiva/items/11
* First 1000 buildings inside 380000,6670000,390000,6680000,EPSG:3067: https://beta-paikkatieto.maanmittauslaitos.fi/maastotiedot/wfs3/v1/collections/rakennus/items?bbox=380000,6670000,390000,6680000&bbox-crs=http://www.opengis.net/def/crs/EPSG/0/3067&crs=http://www.opengis.net/def/crs/EPSG/0/3067&limit=1000

## QGIS
* [QGIS](https://github.com/qgis/QGIS/) implements both a server and a client
* [Server documentation](https://docs.qgis.org/testing/en/docs/user_manual/working_with_ogc/server/services.html#wfs3-ogc-api-features)
* [Demo server](http://138.201.120.72:8084/qgisserver_demo_wfs3/wfs3/)

## SDI Rhineland-Palatinate - mapbender2
The SDIs of the three German Federal States Rhineland-Palatinate, Hesse and Saarland use the mapbender2 ows registry as backend
for their geoportal solutions. In the SDIs there are registered many OpenData classified WFS 2.0 resources and it was straightforward to develop a proxy solution, that implements the OGC API - Features interface at one central location.
Most of the core functions are implemented. The WFS behind the proxy are either based on mapserver or geoserver. The proxy does also create service metadata in form of iso19139 records. One extension is the usage of json-schema to define human readable attribute titles and descriptions at WFS level. The next extension will be the usage of json-ld to give semantical information for the attributes and allow the dynamical creation of rdf-a and other formats.
The code of the current productional solution is available on the [OSGEO GIT](https://git.osgeo.org/gitea/armin11/GeoPortal.rlp)
and [OSGEO SVN](https://trac.osgeo.org/mapbender/browser/trunk/mapbender/).

### Productive list of available Interfaces
* List of all registrated OpenData WFS: https://www.geoportal.rlp.de/mapbender/php/mod_linkedDataProxy.php (some of them wont work, cause the database tables don't have primary keys exposed and therefor paging is not possible).

### Example requests:

#### Transport network (classified roads)
* Start page: https://www.geoportal.rlp.de/spatial-objects/513
* API definition (only available in json): https://www.geoportal.rlp.de/spatial-objects/513/api
* HTML representation for the collection of highway objects: https://www.geoportal.rlp.de/spatial-objects/513/collections/ms:Autobahnen/items?&f=html
* HTML represenation of single highway 'A3': https://www.geoportal.rlp.de/spatial-objects/513/collections/ms:Autobahnen/items/Autobahnen.A3?f=html

#### UNESCO world heritage of the city of Trier (point objects)
* Start page: https://www.geoportal.rlp.de/spatial-objects/486
* API definition (only available in json): https://www.geoportal.rlp.de/spatial-objects/486/api
* HTML representation objects: https://www.geoportal.rlp.de/spatial-objects/486/collections/ms:unesco_welterbe/items?&f=html
* HTML representation of the description of the amphitheater: https://www.geoportal.rlp.de/spatial-objects/486/collections/ms:unesco_welterbe/items/unesco_welterbe.3730?f=html

## ogcapi-js

[ogcapi-js](https://github.com/haoliangyu/ogcapi-js) is a lightweight and modular JavaScript/Tyescript library for OGC APIs. It provides a developer-friendly way to interact with Features API and useful features like query parameter validation and error handling. Developers can use this library to build both client-side (browser) or server-side applications.

## FME
[FME](https://www.safe.com/support/downloads/#beta) (FME 2021.0+) implements a client which is accessible from FME Workbench, Data Inspector and FME Server.

