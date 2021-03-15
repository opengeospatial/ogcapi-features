# CubeWerx Suite

NOTE: This is outdated content and should be updated.

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
