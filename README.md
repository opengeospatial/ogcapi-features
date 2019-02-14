# Web Feature Service 3.0

This GitHub repository contains the new revision of the [OGC](http://opengeospatial.org)'s
Web Feature Service standard for querying geospatial information on the web. It is a complete
rewrite of previous versions, focusing on a simple RESTful core specified
as reusable [OpenAPI](http://openapis.org) components with responses
in JSON and HTML.

## Overview

A Web Feature Service is a standard API that represents collections of geospatial data.

```
GET /collections
```

Lists the collections of data on the server that can be queried ([7.11](https://cdn.rawgit.com/opengeospatial/WFS_FES/3.0.0-draft.1/docs/17-069.html#_feature_collections_metadata)),
and each describes basic information about the geospatial data collection, like its id and description, as well as the
spatial and temporal extents of all the data contained

```
GET /collections/{collectionId}/items?bbox=160.6,-55.95,-170,-25.89
```

Requests all the data in the collection that is in the New Zealand economic zone.
The response format (typically HTML or a [GeoJSON](http://geojson.org/) feature
collection, but GML is supported, too, and extensions can easily supply others) is determined using
[HTTP content negotiation](https://restfulapi.net/content-negotiation/).

Data is returned in pageable chunks, with each response containing a `next` link
as many collections are quite large. The core specification supports a few basic filters, in
addition to the `bbox` filter above, with extensions providing more advanced options.
([7.13](https://cdn.rawgit.com/opengeospatial/WFS_FES/3.0.0-draft.1/docs/17-069.html#_feature_collections))

```
GET /collections/{collectionId}/items/{featureId}
```

Returns a single geographic 'feature' - something in the real-world (a building,
a stream, a county, etc.) that typically is described by a geometry plus other properties.
This provides a stable, canonical URL to link to the 'thing'.

## Using the standard

A draft of WFS 3.0 is available:

* [OGC Web Feature Service 3.0 - Part 1: Core, First Draft Release](https://cdn.rawgit.com/opengeospatial/WFS_FES/3.0.0-draft.1/docs/17-069.html)

Those who want to just see the endpoints and responses can explore the generic
OpenAPI definition on SwaggerHub:

* [WFS 3.0.0-draft.1 openapi.yaml](https://app.swaggerhub.com/apis/cholmesgeo/WFS3/M1)

There have been several implementations of the draft standard, though they are
still getting up to compliance with the first draft release:

* [Implementations of the draft specification / demo services](implementations.md)

## Communication

Join the [mailing list](https://lists.opengeospatial.org/mailman/listinfo/wfs-fes.swg) or [![chat at https://gitter.im/opengeospatial/WFS_FES](https://badges.gitter.im/opengeospatial/WFS_FES.svg)](https://gitter.im/opengeospatial/WFS_FES?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Most all work on the specification takes place in [GitHub issues](https://github.com/opengeospatial/WFS_FES/issues),
so browse there to get a good idea of what is happening, as well as past decisions.

## Additional Information

* [Checklist for implementers](guide/conformance_checklist.md)

Also a non-normative document, the "WFS 3.0 Users Guide", is being developed.

In addition to feedback from the initial implementations as well as discussions on GitHub and in the OGC/ISO working group,
the current draft standard has been tested in a [WFS 3.0 Hackathon](http://www.opengeospatial.org/blog/2764).
The first draft release is used as input for the [OGC Testbed-14](http://www.opengeospatial.org/projects/initiatives/testbed14), the [OGC Vector Tiles Pilot](https://www.opengeospatial.org/projects/initiatives/vt-pilot-2018) and other activities.

Feedback for the Core is collected and discussed in the
[GitHub issues for Part 1, Core](https://github.com/opengeospatial/WFS_FES/issues?q=is%3Aissue+is%3Aopen+label%3A%22Document%3A+Part+1+-+Core%22).
The goal is to agree on resolutions for the open issues starting in 2019. We want to wait for sufficient
implementation feedback, mature implementations including a test suite, the results of OGC Testbed-14 and experience with
draft extensions first.

The current expectation is to have a stable version of the Core specification around mid-2019. This version would
then be the input for the next steps in the standardization process in OGC and ISO/TC 211.

* [Background of this activity](background.md)
* [The next version of WFS - an overview](overview.md)
* [OGC Web Feature Service 3.0 - Part 1: Core, Editor's Draft](https://rawgit.com/opengeospatial/WFS_FES/master/docs/17-069.html)

## Contributing

The contributor understands that any contributions, if accepted by the OGC Membership and ISO/TC 211, shall be incorporated into OGC and ISO/TC 211 Web Feature Service standards documents and that all copyright and intellectual property shall be vested to the OGC.

The WFS/FES Standards Working Group (SWG) is the group at OGC responsible for the stewardship of the standard, but is working to do as much work in public as possible.

* [Open issues](https://github.com/opengeospatial/WFS_FES/issues)
* [Proposing changes](https://github.com/opengeospatial/WFS_FES/wiki/Propose-a-change-to-a-draft-of-a-WFS-specification-document)
* [Copy of License Language](https://raw.githubusercontent.com/opengeospatial/WFS_FES/master/LICENSE)
