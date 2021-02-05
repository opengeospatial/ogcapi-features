# OGC API - Features

This GitHub repository contains [OGC](http://opengeospatial.org)'s
multi-part standard for querying geospatial information on the web, "OGC API - Features".
All approved versions of the specification can be found [here](https://www.opengeospatial.org/standards/ogcapi-features).

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

## Overview

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

## Using the standard

The standard is on the OGC website:

* OGC API - Features - Part 1: Core
  * [Version 1.0.0 (latest approved version)](http://docs.ogc.org/is/17-069r3/17-069r3.html)
  * [Editor's draft (includes errata and clarifications)](http://docs.ogc.org/DRAFTS/17-069r4.html)
* OGC API - Features - Part 2: Coordinate Reference Systems by Reference
  * [Version 1.0.0 (latest approved version)](http://docs.ogc.org/is/18-058/18-058.html)
  * [Editor's draft (includes errata and clarifications)](http://docs.ogc.org/DRAFTS/18-058r1.html)

Those who want to just see the endpoints and responses can explore [examples of
OpenAPI definitions](https://github.com/opengeospatial/ogcapi-features/tree/master/core/examples/openapi).

The reference version of the OpenAPI components and XML schemas are published
in the [OGC schema repository](http://schemas.opengis.net/ogcapi/features/).

Several implementations exist:

* [Implementations / demo services](implementations.md)

## Communication

Join the [mailing list](https://lists.opengeospatial.org/mailman/listinfo/wfs-fes.swg) or [![chat at https://gitter.im/opengeospatial/WFS_FES](https://badges.gitter.im/opengeospatial/WFS_FES.svg)](https://gitter.im/opengeospatial/WFS_FES?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Most all work on the specification takes place in [GitHub issues](https://github.com/opengeospatial/ogcapi-features/issues),
so browse there to get a good idea of what is happening, as well as past decisions.

## Additional parts of OGC API - Features

The OGC Features API SWG has identified the following extensions as the highest priority:

* [OGC API - Features - Part 3: Filtering and the Common Query Language (CQL)](http://docs.ogc.org/DRAFTS/19-079.html)
  * Draft with multiple implementations. The grammar of the query language should be fairly stable. The final Public Review will run until April 2021. Once all comments have been resolved, the release candidate will enter the OGC approval process. The release of version 1.0.0 is expected in Q3 of 2021.
* [OGC API - Features - Part 4: Create, Replace, Update and Delete](http://docs.ogc.org/DRAFTS/20-002.html)
  * The draft is fairly complete, but needs more implementations, testing and review to move to the final Public Review.
* OGC API - Features - Part 5: OpenAPI 3.1
  * Waiting for the release of OpenAPI Specification version 3.1.0.

## Additional information

Part 1 (Core) has also been published by ISO as [ISO 19168-1:2020](https://www.iso.org/standard/32586.html).

Open issues for all parts are organized in [GitHub projects](https://github.com/opengeospatial/ogcapi-features/projects):

* [Open issues for Part 1: Core](https://github.com/opengeospatial/ogcapi-features/projects/1), 
* [Open issues for Part 2: Coordinate Reference Systems by Reference](https://github.com/opengeospatial/ogcapi-features/projects/2)
* [Open issues for Part 3: Filtering and the Common Query Language (CQL)](https://github.com/opengeospatial/ogcapi-features/projects/4)
* [Open issues for Part 4: Create, Replace, Update and Delete](https://github.com/opengeospatial/ogcapi-features/projects/3)
* [Open issues for Part 5: OpenAPI 3.1](https://github.com/opengeospatial/ogcapi-features/projects/7)

Additional links:

* [Background of this activity](background.md)
* [The next version of WFS - an overview](overview.md)
* [UML for Part 1, Core](uml/README.md)
* [Status of Part 1, Core, in ISO](https://www.iso.org/standard/32586.html)
* [Home of the standard on the OGC website](https://www.opengeospatial.org/standards/ogcapi-features)

## Building

The latest drafts of each standard in this repository are build daily (based on the configuration contained in the [asciidoctor.json](https://github.com/opengeospatial/ogcapi-features/blob/master/asciidoctor.json) file):

* [Part 1: Core](http://docs.ogc.org/DRAFTS/17-069r4.html)
* [Part 2: Coordinate Reference Systems by Reference](http://docs.ogc.org/DRAFTS/18-058r1.html)
* [Part 3: Filtering and the Common Query Language (CQL)](http://docs.ogc.org/DRAFTS/19-079.html)
* [Part 4: Create, Replace, Update and Delete](http://docs.ogc.org/DRAFTS/20-002.html)

To generate the HTML versions of the standards from this repository yourself, ensure that you have [Ruby](https://www.ruby-lang.org/en/) and
[Asciidoctor](https://asciidoctor.org/) set up and [installed](https://asciidoctor.org/docs/#get-started-with-asciidoctor).
Then run:

```
# Part 1: Core
asciidoctor -a data-uri -r asciidoctor-diagram core/standard/17-069.adoc
# Part 2: Coordinate Reference Systems by Reference
asciidoctor -a data-uri -r asciidoctor-diagram extensions/crs/standard/18-058.adoc
# Part 3: Filtering and the Common Query Language (CQL)
asciidoctor -a data-uri -r asciidoctor-diagram extensions/cql/standard/19-079.adoc
# Part 4: Create, Replace, Update and Delete
asciidoctor -a data-uri -r asciidoctor-diagram extensions/transactions/simple/standard/20-002.adoc
```

The resulting HTML files will be built in the same directory as the AsciiDoc file, e.g. as `core/standard/17-069.html`.

## [Contributing](CONTRIBUTING.md)

The contributor understands that any contributions, if accepted by the OGC Membership and ISO/TC 211, shall be incorporated into OGC and ISO/TC 211 OGC API standards documents and that all copyright and intellectual property shall be vested to the OGC.

The Features API Standards Working Group (SWG) is the group at OGC responsible for the stewardship of the standard, but is working to do as much work in public as possible.

* [Features API Standards Working Group Charter](CHARTER.adoc)
* [Open issues](https://github.com/opengeospatial/ogcapi-features/issues)
* [Proposing changes](https://github.com/opengeospatial/ogcapi-features/wiki/Propose-a-change-to-a-draft-of-a-specification-document)
* [Copy of License Language](https://raw.githubusercontent.com/opengeospatial/ogcapi-features/master/LICENSE)

Pull Requests from contributors are welcomed. However, please note that by sending a Pull Request or Commit to this GitHub repository, you are agreeing to the terms in the Observer Agreement https://portal.ogc.org/files/?artifact_id=92169
