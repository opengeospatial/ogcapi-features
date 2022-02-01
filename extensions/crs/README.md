# OGC API - Features - Part 2: Coordinate Reference Systems by Reference

This folder contains the content for the standard [OGC API - Features - Part 2: Coordinate Reference Systems by Reference](http://docs.opengeospatial.org/is/18-058/18-058.html).

# Overview

In Part 1 (Core) the default spatial coordinate reference system (CRS) is WGS 84 longitude/latitude with or without height. Part 2 extends Part 1 to support presenting geometry-valued properties in a response document in additional CRSs. Each supported CRS must be identified by a URI such as http://www.opengis.net/def/crs/EPSG/0/4326.

## Discovery of information

The server publishes the CRS information for each feature collection. For example, for a collection `buildings` the response to

```
GET /collections/buildings
```

will typically include the following properties:

* `crs`: an array of CRS URIs supported by the service. If no value is provided, the default is `[ "http://www.opengis.net/def/crs/OGC/1.3/CRS84" ]`.
* `storageCrs`: the URI of the CRS in which geometries are stored in the data set; if provided, this is a hint that features in this CRS can be retrieved without the need to apply a CRS transformation.

In addition, a property `storageCrsCoordinateEpoch` may be provided, if the storage CRS is a dynamic coordinate reference system. This property can be used to declare the point in time at which coordinates are referenced to that CRS. It is expressed as a decimal year in the Gregorian calendar, e.g., epoch '2017.23' is 3rd March 2017 in the Gregorian calendar. Depending on the point in time when the geometries are requested and the required coordinate precision, the returned coordinates may need to be converted to the current coordinate epoch.

## Retrieve geometries in a specific CRS

In requests to fetch one or more features, add the parameter `crs` with one of the supported CRSs. For example, use the following to retrieve building in ETRS89 UTM Zone 32 North (a projected CRS):

```
GET /collections/buildings/items?
crs=http%3A%2F%2Fwww.opengis.net%2Fdef%2Fcrs%2FEPSG%2F0%2F25832
```

As usual, don't forget to percent-encode the parameter value.

## Use a bounding box with another CRS

By default, the `bbox` parameter specified in Part 1 expects a bounding box in the default CRS - unless another CRS is specified in the parameter `bbox-crs`.

The following requests the buildings in Bonn, Germany, using a bounding box in ETRS89 UTM Zone 32 North:

```
GET /collections/buildings/items?
bbox=280375,5577680,531792,5820212&
bbox-crs=http%3A%2F%2Fwww.opengis.net%2Fdef%2Fcrs%2FEPSG%2F0%2F25832
```

## The CRS is declared in a HTTP header

Servers will also return the CRS used in the response in an additional HTTP header `Content-Crs`.

For example:

```
$ curl -i "https://example.com/api/v1/collections/buildings/items/1?crs=http%3A%2F%2Fwww.opengis.net%2Fdef%2Fcrs%2FEPSG%2F0%2F25832"

HTTP/1.1 200 OK
Date: Sun, 24 May 2020 15:30:56 GMT
Content-Type: application/geo+json
Content-Language: en
Content-Crs: <http://www.opengis.net/def/crs/EPSG/0/25832>
Vary: Accept-Language,Accept-Encoding
Content-Length: 1064
```

# Folder structure

This folder is organized as follows:

* standard - the main standard document content
  - organized in multiple sections and directories
* openapi - normative OpenAPI components specified by the standard
* xml - normative XML/XSD components specified by the standard
* examples - JSON and XML examples
* release-notes.md - overview of changes in new releases
