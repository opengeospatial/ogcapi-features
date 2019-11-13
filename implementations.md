# Implementations

## Overview

This page points to servers implementing drafts of the OGC API Features series.
For now this is limited to implementations of the current draft of Part 1. Core.

## Implementations:

Servers:

* [interactive instruments](#interactive-instruments)
* [CubeWerx Inc.](#cubeWerx)
* [GeoServer](#geoserver)
* [pygeoapi](#pygeoapi)
* [jivan](#jivan)
* [sofp](#sofp)
* [STAC](#STAC)
* [nls-fi](#nls-fi)

Clients:
* [go-wfs3-client](https://github.com/ischneider/go-wfs3-client)
* [GDAL/OGR OGC API - Features driver](https://gdal.org/drivers/vector/oapif.html)
* [OWSLib WFS 3.0 client](https://geopython.github.io/OWSLib)
* [STAC](#STAC)

## interactive instruments

The following are two servers implementing most of the current draft
of part 1. They are using German data and therefore the language
in general is German, including in the HTML.

The first endpoint is for cadastral parcels, buildings and
administrative areas in North-Rhine Westphalia (Germany).
The second endpoint for topographic data in that region.

For more details about the implementation and a discussion about
how this implements the Spatial Data on the Web Best Practies see
the [Implementation Report](https://github.com/w3c/sdw/blob/gh-pages/bp/BP-implementation-report-00003.md).

OpenAPI documents:
* https://www.ldproxy.nrw.de/kataster/api/
* https://www.ldproxy.nrw.de/topographie/api/
* https://www.ldproxy.nrw.de/dvg/api/

HTML landing pages:
* https://www.ldproxy.nrw.de/kataster/
* https://www.ldproxy.nrw.de/topographie/
* https://www.ldproxy.nrw.de/dvg/

The implementations are proxy services that sit on top of WFS 2.0 instances.

Here are some example requests for features using GeoJSON output (for HTML output
simply change `f=json` to `f=html`, for GML to `f=xml`):

* Municipalities close to Bonn (attribute and spatial filter):  
[https://www.ldproxy.nrw.de/kataster/collections/verwaltungseinheit/items?  
f=json&  
art=Gemeinde&  
bbox=7.0,50.6,7.2,50.8&  
count=20](https://www.ldproxy.nrw.de/kataster/collections/verwaltungseinheit/items?f=json&art=Gemeinde&bbox=7.0%2C50.6%2C7.2%2C50.8&count=20)  

* Same filter, just to determine the number of selected municipalities (13):  
[https://www.ldproxy.nrw.de/kataster/collections/verwaltungseinheit/items?  
f=json&  
art=Gemeinde&  
bbox=7.0,50.6,7.2,50.8&  
resultType=hits](https://www.ldproxy.nrw.de/kataster/collections/verwaltungseinheit/items?f=json&art=Gemeinde&bbox=7.0%2C50.6%2C7.2%2C50.8&resultType=hits)  

* Cadastral parcels at Schadowplatz in Düsseldorf:  
[https://www.ldproxy.nrw.de/kataster/collections/flurstueck/items?  
f=json&  
lagebeztxt=Schadowplatz\*&  
bbox=6.7,51.2,6.9,51.4](https://www.ldproxy.nrw.de/kataster/collections/flurstueck/items?f=json&lagebeztxt=Schadowplatz*&bbox=6.7%2C51.2%2C6.9%2C51.4)

* Cadastral Parcel for Schadowplatz 14 in Düsseldorf:  
[https://www.ldproxy.nrw.de/kataster/collections/flurstueck/items/DENW20AL0000qTfzFL?  
f=json](https://www.ldproxy.nrw.de/kataster/collections/flurstueck/items/DENW20AL0000qTfzFL?f=json)

* Railway stations, bus/tram stops, etc. near Düsseldorf:  
[https://www.ldproxy.nrw.de/topographie/collections/ax_bahnverkehrsanlage/items?  
f=json&  
bbox=6.70,51.18,6.87,51.27](https://www.ldproxy.nrw.de/topographie/collections/ax_bahnverkehrsanlage/items?f=json&bbox=6.70%2C51.18%2C6.87%2C51.27)

* Railway stations near Düsseldorf:  
[https://www.ldproxy.nrw.de/topographie/collections/ax_bahnverkehrsanlage/items?  
f=json&  
bahnhofskategorie=1010&  
bbox=6.70,51.18,6.87,51.27](https://www.ldproxy.nrw.de/topographie/collections/ax_bahnverkehrsanlage/items?f=json&bahnhofskategorie=1010&bbox=6.70%2C51.18%2C6.87%2C51.27)

Another server is from the [OGC Vector Tiles Pilot](http://www.opengeospatial.org/projects/initiatives/vt-pilot-2018) 
and it includes extensions for vector tile and style resources:

* OpenAPI definition: https://services.interactive-instruments.de/vtp/daraa/api
* Landing page: https://services.interactive-instruments.de/vtp/daraa

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

An incomplete implementation of the WFS3 specification is available at http://cloudsdi.geo-solutions.it/geoserver/wfs3/
It is a community module developed from scratch during the WFS 3 hackaton. At the time of writing, still misses HTML outputs, conformance call, paging links (supports random paging with startIndex), single feature outputs and attribute filtering.

## pygeoapi

[pygeoapi](https://geopython.github.io/pygeoapi) implements the majority of the current draft.  pygeoapi is implemented in Python, and supports JSON and HTML responses.

### Example requests:
* OpenAPI 3 document: ([JSON](https://demo.pygeoapi.io/master/api?f=json)) ([HTML](https://demo.pygeoapi.io/master/api))
* All feature collections: ([JSON](https://demo.pygeoapi.io/master/collections?f=json)) ([HTML](https://demo.pygeoapi.io/master/collections?f=html))
* Single feature collection: ([JSON](https://demo.pygeoapi.io/master/collections/utah_city_locations?f=json)) ([HTML](https://demo.pygeoapi.io/master/collections/utah_city_locations?f=html))
* Feature collection items: ([JSON](https://demo.pygeoapi.io/master/collections/utah_city_locations/items?f=json)) ([HTML](https://demo.pygeoapi.io/master/collections/utah_city_locations/items?f=html))
* Feature collection single item: ([JSON](https://demo.pygeoapi.io/master/collections/utah_city_locations/items/Fairfield?f=json) ([HTML](https://demo.pygeoapi.io/master/collections/utah_city_locations/items/Fairfield?f=html))
* Feature collection: bbox query: ([JSON](https://demo.pygeoapi.io/master/collections/lakes/items?bbox=-152,42,-52,84&f=json)) ([HTML](https://demo.pygeoapi.io/master/collections/lakes/items?bbox=-152,42,-52,84&f=html))

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
