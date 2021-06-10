# OGC API - Features

[OGC API standards](https://ogcapi.ogc.org/) define modular API building blocks to spatially enable Web APIs
in a consistent way. [OpenAPI](http://openapis.org) is used to define the reusable
API building blocks with responses in JSON and HTML.

The OGC API family of standards is organized by resource type. OGC API Features
specifies the fundamental API building blocks for interacting with features.
The spatial data community uses the term 'feature' for things in the real world
that are of interest.

If you are unfamiliar with the term 'feature', the explanations on
[Spatial Things, Features and Geometry](https://www.w3.org/TR/sdw-bp/#spatial-things-features-and-geometry)
in the W3C/OGC Spatial Data on the Web Best Practice document provide more detail.

## Overview of OGC API - Features - Part 1: Core

OGC API Features provides access to collections of geospatial data.

```
GET /collections
```

Lists the collections of data on the server that can be queried ([section 7.13](http://www.opengis.net/doc/IS/ogcapi-features-1/1.0#_collections_)),
and each describes basic information about the geospatial data collection, like its id and description, as well as the
spatial and temporal extents of all the data contained.

```
GET /collections/buildings/items?bbox=160.6,-55.95,-170,-25.89
```

Requests all the data in the collection "buildings" that is in the New Zealand economic zone.
The response format (typically HTML or a [GeoJSON](http://geojson.org/) feature
collection, but GML is supported, too, and extensions can easily supply others) is determined using
[HTTP content negotiation](https://restfulapi.net/content-negotiation/).

Data is returned in pageable chunks, with each response containing a `next` link
as many collections are quite large. The core specification supports a few basic filters, in
addition to the `bbox` filter above, with extensions providing more advanced options
([section 7.15](http://www.opengis.net/doc/IS/ogcapi-features-1/1.0#_items_)).

```
GET /collections/{collectionId}/items/{featureId}
```

Returns a single 'feature' - something in the real-world (a building,
a stream, a county, etc.) that typically is described by a geometry plus other properties.
This provides a stable, canonical URL to link to the 'thing'
([section 7.16](http://www.opengis.net/doc/IS/ogcapi-features-1/1.0#_feature_)).

See [here](https://github.com/opengeospatial/ogcapi-features/tree/master/extensions/crs) for
an overview of the extensions to support additional coordinate reference systems beyond WGS 84.

## Overview of OGC API - Features - Part 2: Coordinate Reference Systems By Reference

In Part 1 (Core) the default spatial coordinate reference system (CRS) is WGS 84 longitude/latitude with or without height. Part 2 extends Part 1 to support presenting geometry-valued properties in a response document in additional CRSs. Each supported CRS must be identified by a URI such as http://www.opengis.net/def/crs/EPSG/0/4326.

### Discovery of information

The server publishes the CRS information for each feature collection. For example, for a collection `buildings` the response to

```
GET /collections/buildings
```

will typically include the following properties:

* `crs`: an array of CRS URIs supported by the service. If no value is provided, the default is `[ "http://www.opengis.net/def/crs/OGC/1.3/CRS84" ]`.
* `storageCrs`: the URI of the CRS in which geometries are stored in the data set; if provided, this is a hint that features in this CRS can be retrieved without the need to apply a CRS transformation.

In addition, a property `storageCrsCoordinateEpoch` may be provided, if the storage CRS is a dynamic coordinate reference system. This property can be used to declare the point in time at which coordinates are referenced to that CRS. It is expressed as a decimal year in the Gregorian calendar, e.g., epoch '2017.23' is 3rd March 2017 in the Gregorian calendar. Depending on the point in time when the geometries are requested and the required coordinate precision, the returned coordinates may need to be converted to the current coordinate epoch.

### Retrieve geometries in a specific CRS

In requests to fetch one or more features, add the parameter `crs` with one of the supported CRSs. For example, use the following to retrieve building in ETRS89 UTM Zone 32 North (a projected CRS):

```
GET /collections/buildings/items?
crs=http%3A%2F%2Fwww.opengis.net%2Fdef%2Fcrs%2FEPSG%2F0%2F25832
```

As usual, don't forget to percent-encode the parameter value.

### Use a bounding box with another CRS

By default, the `bbox` parameter specified in Part 1 expects a bounding box in the default CRS - unless another CRS is specified in the parameter `bbox-crs`.

The following requests the buildings in Bonn, Germany, using a bounding box in ETRS89 UTM Zone 32 North:

```
GET /collections/buildings/items?
bbox=280375,5577680,531792,5820212&
bbox-crs=http%3A%2F%2Fwww.opengis.net%2Fdef%2Fcrs%2FEPSG%2F0%2F25832
```
