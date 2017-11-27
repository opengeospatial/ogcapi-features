# Implementations

## Overview

This page points to servers implementing WFS 3.0 drafts.
For now this is limited to implementations of the current
draft of part 1.

Implementations:
* [interactive instruments](#interactive-instruments)
* [CubeWerx Inc.](#CubeWerx-Inc.)
* 

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

Here are some example requests for features using GeoJSON output (for HTML output simply change `f=json` to `f=html`):

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

## CubeWerx-Inc.

The following server implements a good portion of the current draft part 1
standard.  Just to illustrate that GML may still be used, and to contrast
the interactive instruments examples, these queries will return GML rather
than JSON (although GeoJSON can be returned by requesting the appropriate
MIME type).

Like the interactive instruments server, this 3.0 alpha implementation is a
facade sitting on top of our previous WFS 2.X implementation.

HTML landing page:
* http://www.pvretano.com/cubewerx/cubeserv/default/wfs/2.5.0/foundation

Here are some example requests for features using GML v3.2 output.

* Built up areas around Washington DC:  
[http://www.cubewerx-pvretano.com/cubewerx/cubeserv/default/wfs/2.5.0/foundation/builtupa_1m?  
count=20&  
f=application/gml%2Bxml;%20version=3.2&  
bbox=36.8207,-79.5854,39.7519,-74.4218](http://www.cubewerx-pvretano.com/cubewerx/cubeserv/default/wfs/2.5.0/foundation/builtupa_1m?count=20&f=application/gml%2Bxml;%20version=3.2&bbox=36.8207,-79.5854,39.7519,-74.4218)

* Same filter, just to determine the number of built up areas:    
[http://www.cubewerx-pvretano.com/cubewerx/cubeserv/default/wfs/2.5.0/foundation/builtupa_1m?  
resultType=hits&  
f=application/gml%2Bxml;%20version=3.2&  
bbox=36.8207,-79.5854,39.7519,-74.4218](http://www.cubewerx-pvretano.com/cubewerx/cubeserv/default/wfs/2.5.0/foundation/builtupa_1m?resultType=hits&f=application/gml%2Bxml;%20version=3.2&bbox=36.8207,-79.5854,39.7519,-74.4218)

* All municipalities that start with "Wash":   
[http://www.pvretano.com/cubewerx/cubeserv/default/wfs/2.5.0/foundation/builtupa_1m?  
f=application/gml%2Bxml;%20version=3.2&  
nam=Wash*](http://www.pvretano.com/cubewerx/cubeserv/default/wfs/2.5.0/foundation/builtupa_1m?&f=application/gml%2Bxml;%20version=3.2&nam=Wash*)
