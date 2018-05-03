# Implementations

## Overview

This page points to servers implementing WFS 3.0 drafts.
For now this is limited to implementations of the current
draft of part 1.

## Implementations:

Servers:

* [interactive instruments](#interactive-instruments)
* [CubeWerx Inc.](#cubeWerx)
* [GeoServer](#geoserver)
* [pygeoapi](#pygeoapi)
* [go-wfs](#go-wfs)

Clients:
* [go-wfs3-client](https://github.com/ischneider/go-wfs3-client)
* [ogr/gdal WFS 3.0 client driver](http://gdal.org/drv_wfs3.html)

## interactive instruments

The following are two servers implementing most of the current draft
of part 1. They are using German data and therefore the language
in general is German, including in the HTML.

The first endpoint is for cadastral parcels, buildings and
administrative areas in North-Rhine Westphalia (Germany).
The second endpoint for topographic data in that region.

OpenAPI documents:
* https://www.ldproxy.nrw.de/kataster/api/
* https://www.ldproxy.nrw.de/topographie/api/

HTML landing pages:
* https://www.ldproxy.nrw.de/kataster/
* https://www.ldproxy.nrw.de/topographie/

Since the code generation tools do not yet support OpenAPI 3.0 well, we
have created OpenAPI/Swagger 2.0 definitions for the APIs and published
them on Swagger Hub, too:
* https://app.swaggerhub.com/apis/cportele/lika-nrw/0.0.1
* https://app.swaggerhub.com/apis/cportele/topo-nrw/0.0.1

The implementations are proxy services that sit on top of WFS 2.0 instances.

Here are some example requests for features using GeoJSON output (for HTML output 
simply change `f=json` to `f=html`, for GML to `f=xml`):

* Municipalities close to Bonn (attribute and spatial filter):  
[https://www.ldproxy.nrw.de/kataster/VerwaltungsEinheit?  
f=json&  
art=Gemeinde&  
bbox=7.0,50.6,7.2,50.8&  
count=20](https://www.ldproxy.nrw.de/kataster/VerwaltungsEinheit?f=json&art=Gemeinde&bbox=7.0%2C50.6%2C7.2%2C50.8&count=20)  

* Same filter, just to determine the number of selected municipalities (13):  
[https://www.ldproxy.nrw.de/kataster/VerwaltungsEinheit?  
f=json&  
art=Gemeinde&  
bbox=7.0,50.6,7.2,50.8&  
resultType=hits](https://www.ldproxy.nrw.de/kataster/VerwaltungsEinheit?f=json&art=Gemeinde&bbox=7.0%2C50.6%2C7.2%2C50.8&resultType=hits)  

* All municipalities that start with "Dü":  
[https://www.ldproxy.nrw.de/kataster/VerwaltungsEinheit?  
f=json&  
art=Gemeinde&  
name=Dü\*](https://www.ldproxy.nrw.de/kataster/VerwaltungsEinheit?f=json&art=Gemeinde&name=Dü*)  

* Cadastral parcels at Schadowplatz in Düsseldorf:  
[https://www.ldproxy.nrw.de/kataster/Flurstueck?  
f=json&  
lagebeztxt=Schadowplatz\*&  
bbox=6.7,51.2,6.9,51.4](https://www.ldproxy.nrw.de/kataster/Flurstueck?f=json&lagebeztxt=Schadowplatz*&bbox=6.7%2C51.2%2C6.9%2C51.4)

* Cadastral Parcel for Schadowplatz 14 in Düsseldorf:  
[https://www.ldproxy.nrw.de/kataster/Flurstueck/DENW20AL0000qTfzFL?  
f=json](https://www.ldproxy.nrw.de/kataster/Flurstueck/DENW20AL0000qTfzFL?f=json)

* Railway stations, bus/tram stops, etc. near Düsseldorf:  
[https://www.ldproxy.nrw.de/topographie/AX_Bahnverkehrsanlage?  
f=json&  
bbox=6.70,51.18,6.87,51.27](https://www.ldproxy.nrw.de/topographie/AX_Bahnverkehrsanlage?f=json&bbox=6.70%2C51.18%2C6.87%2C51.27)

* Railway stations near Düsseldorf:  
[https://www.ldproxy.nrw.de/topographie/AX_Bahnverkehrsanlage?  
f=json&  
bahnhofskategorie=1010&  
bbox=6.70,51.18,6.87,51.27](https://www.ldproxy.nrw.de/topographie/AX_Bahnverkehrsanlage?f=json&bahnhofskategorie=1010&bbox=6.70%2C51.18%2C6.87%2C51.27)

## CubeWerx Inc.

The following server implements a good portion of the current draft part 1
standard.  Just to illustrate that GML may still be used, and to contrast
the interactive instruments examples, these queries will return GML rather
than JSON (although GeoJSON can be returned by requesting the appropriate
MIME type).

Like the interactive instruments server, this 3.0 alpha implementation is a
facade sitting on top of our previous WFS 2.X implementation.

HTML landing page:
* http://www.pvretano.com/cubewerx/cubeserv/default/wfs/2.5.0/foundation 

NOTE: The landing page still uses the classic OGC request forms and has not yet been updated to 3.0.

Here are some example requests for features using GML v3.2 output.

* Built up areas around Washington DC:
[http://www.pvretano.com/cubewerx/cubeserv/default/wfs/2.5.0/foundation/builtupa_1m?  
count=20&  
f=application/gml%2Bxml;%20version=3.2&  
bbox=36.8207,-79.5854,39.7519,-74.4218](http://www.pvretano.com/cubewerx/cubeserv/default/wfs/2.5.0/foundation/builtupa_1m?count=20&f=application/gml%2Bxml;%20version=3.2&bbox=36.8207,-79.5854,39.7519,-74.4218)

* Same filter, just to determine the number of built up areas:  
[http://www.pvretano.com/cubewerx/cubeserv/default/wfs/2.5.0/foundation/builtupa_1m?  
resultType=hits&  
f=application/gml%2Bxml;%20version=3.2&  
bbox=36.8207,-79.5854,39.7519,-74.4218](http://www.pvretano.com/cubewerx/cubeserv/default/wfs/2.5.0/foundation/builtupa_1m?resultType=hits&f=application/gml%2Bxml;%20version=3.2&bbox=36.8207,-79.5854,39.7519,-74.4218)

* All municipalities that start with "Wash":  
[http://www.pvretano.com/cubewerx/cubeserv/default/wfs/2.5.0/foundation/builtupa_1m?  
f=application/gml%2Bxml;%20version=3.2&  
nam=Wash\*](http://www.pvretano.com/cubewerx/cubeserv/default/wfs/2.5.0/foundation/builtupa_1m?&f=application/gml%2Bxml;%20version=3.2&nam=Wash*)

## GeoServer

An incomplete implementation of the WFS3 specification is available at http://cloudsdi.geo-solutions.it/geoserver/wfs3/ 
It is a community module developed from scratch during the WFS 3 hackaton. At the time of writing, still misses HTML outputs, conformance call, paging links (supports random paging with startIndex), single feature outputs and attribute filtering.

## pygeoapi

[pygeoapi](https://github.com/geopython/pygeoapi) implements the majority of the current draft.  pygeoapi is implemented in Python, and supports JSON and HTML responses.

### Example requests:
* OpenAPI 3 document: http://geo.kralidis.ca/pygeoapi/api
* All feature collections: http://geo.kralidis.ca/pygeoapi/collections ([HTML](http://geo.kralidis.ca/pygeoapi/collections?f=html))
* Single feature collection: http://geo.kralidis.ca/pygeoapi/collections/ne_110m_populated_places_simple ([HTML](http://geo.kralidis.ca/pygeoapi/collections/ne_110m_populated_places_simple?f=html))
* Feature collection items: http://geo.kralidis.ca/pygeoapi/collections/ne_110m_populated_places_simple/items ([HTML](http://geo.kralidis.ca/pygeoapi/collections/ne_110m_populated_places_simple/items?f=html))
* Feature collection single item: http://geo.kralidis.ca/pygeoapi/collections/ne_110m_populated_places_simple/items/2661552 ([HTML](http://geo.kralidis.ca/pygeoapi/collections/ne_110m_populated_places_simple/items/2661552?f=html))
* Feature collection: populated places in Canada: http://geo.kralidis.ca/pygeoapi/collections/ne_110m_populated_places_simple/items?adm0name=Canada
* Feature collection: bbox query: http://geo.kralidis.ca/pygeoapi/collections/ne_110m_populated_places_simple/items?bbox=-152,42,-52,84

## go-wfs

[go-wfs](https://github.com/go-spatial/go-wfs) implements the majority of the current draft.  go-wfs is implemented in Go, and supports JSON and HTML responses.

### Example requests:
* OpenAPI 3 document: http://features.gospatial.org/api
* All feature collections: http://features.gospatial.org/collections ([HTML](http://features.gospatial.org/collections?f=text/html))
* Single feature collection: http://features.gospatial.org/collections/amenities_points ([HTML](http://features.gospatial.org/collections/amenities_points?f=text/html))
* Feature collection items: http://features.gospatial.org/collections/amenities_points/items ([HTML](http://features.gospatial.org/collections/amenities_points/items?f=text/html))
* Feature collection single item: http://features.gospatial.org/collections/amenities_points/items/2 ([HTML](http://features.gospatial.org/collections/amenities_points/items/2?f=text/html))
* Feature collection: populated places in Canada: http://features.gospatial.org/collections/amenities_points/items?amenity=fast_food
