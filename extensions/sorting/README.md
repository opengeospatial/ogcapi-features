# OGC API - Features - Part 3: Filtering

This folder contains the content for the candidate standard [OGC API - Features - Part 3: Filtering](https://docs.ogc.org/DRAFTS/19-079r1.html).

## Status

The candidate standard is in the [OGC public comment period](https://www.ogc.org/standards/requests/229). Candidate standards of the OGC API Features series are all developed from the beginning in public GitHub repositories and welcome public comments at any time. This period is the last step in the OGC process before submitting the candidate standard to the OGC Technical Committee for the approval process - after the comments received during the public comment period have been resolved.

The public comment period for candidate standards of the OGC API Features series is at least two months (instead of the 30-day period that OGC normally uses) to allow for feedback from implementations. The public comment period of this candidate standard officially ended on April 19, 2021. However, the OGC Features API SWG has decided to continue to accept new comments and issues, because server implementations implementing public comment period baseline (version "1.0.0-draft.2") that can be used to test client implementations only became available during April 2021. 

The issues are managed in a [GitHub project board](https://github.com/opengeospatial/ogcapi-features/projects/4).

Originally Part 3 also included the Common Query Language (CQL2), but CQL2 has now been moved to be a standalone standard since CQL2 can also be used independent of the OGC API standards. No technical changes were introduced by the split.

## Overview

The candidate standard specifies three query parameters that can be used to select a subset of the features:

- `filter`: The filter expression, like a WHERE clause in SQL.
- `filter-lang`: The language of the filter expression. The candidate standard recognizes both encodings of the [Common Query Language (CQL2)](https://docs.ogc.org/DRAFTS/21-065.html) - a text grammar (`cql2-text`, the default) and a JSON representation (`cql2-json`).
- `filter-crs`: By default, all geometries in filter expressions are in the coordinate reference system WGS 84 (longitude, latitude, optional height). If the geometries in the filter expression are in a different coordinate reference system, that coordinate reference system is specified in this parameter. It must be one of the coordinate reference systems that is supported by the API for the feature collection as declared in the [`crs` property of the Collection](https://docs.opengeospatial.org/is/18-058/18-058.html#crs-discovery).

## Filtering capabilities specified in other parts of OGC API Features

Part 1 (Core) specifies minimal filtering capabilities that almost everyone will need when sharing geospatial feature data via an API:

- [spatial filtering](http://www.opengis.net/doc/IS/ogcapi-features-1/1.0#_parameter_bbox) (`bbox`): selecting features in a bounding box in WGS 84
- [temporal filtering](http://www.opengis.net/doc/IS/ogcapi-features-1/1.0#_parameter_datetime) (`datetime`): selecting features at a time instant or for a time interval
- [attribute filtering](http://www.opengis.net/doc/IS/ogcapi-features-1/1.0#_parameters_for_filtering_on_feature_properties): selecting features by value for selected properties (optional)
- every filter is combined with a logical `AND`

An example: [https://demo.ldproxy.net/daraa/collections/CulturePnt/items?datetime=../2012-12-31T23:59:59Z&bbox=36.0,32.6,36.1,32.7&F_CODE=AL030](https://demo.ldproxy.net/daraa/collections/CulturePnt/items?datetime=../2012-12-31T23:59:59Z&bbox=36.0,32.6,36.1,32.7&F_CODE=AL030)

Part 2 (Coordinate Reference Systems by Reference) adds support for other coordinate reference systems that can be used in the `bbox` parameter through a [parameter `bbox-crs`](https://docs.opengeospatial.org/is/18-058/18-058.html#_parameter_bbox_crs).

These filtering capabilities can be combined with the capabilities specified in Part 3. All filter expressions are combined with `AND`.

## Implementations available for testing

The following servers are available for testing and implement version "1.0.0-draft.2" (the version from early 2021 before the OGC public comment period). For each implementation, the supported conformance classes and any deviations from [version "1.0.0-draft.2"](https://portal.ogc.org/files/?artifact_id=96288&version=2) are documented.

### ldproxy / interactive instruments

Endpoint:

- https://demo.ldproxy.net/daraa (or any of the other APIs on https://demo.ldproxy.net/)

Conformance classes:

- Filter
- Features Filter
- Simple CQL
- Enhanced Spatial Operators
- CQL2 Text
- CQL2 JSON

Limitations:

- The following `BOOLEAN` literals are not accepted: "T" | "t" | "F" | "f" | "1" | "0". See #545, #550.
- `IN` operator: currently restricted to a property on the left side and literals on the right side, `NOCASE` is not supported.
- In addition to `ANYINTERACTS`, the following temporal operators are supported: `AFTER`, `BEFORE`, `TEQUALS` (instants only), `DURING` (right side must be an interval).
- Array predicates, functions or arithmetic expressions are not yet supported.

### cubeserv / CubeWerx

Endpoint:

- https://www.pvretano.com/cubewerx/cubeserv/default/ogcapi/foundation (or any landing page endpoint off https://www.pvretano.com/cubewerx/cubeserv)

Conformance classes:

- Filter
- Features Filter
- Simple CQL
- CQL2 Text

Limitations:

- The following `BOOLEAN` literals are not accepted: "T" | "t" | "F" | "f" | "1" | "0". See #545, #550.
- `IN` operator: currently restricted to a property on the left side and literals on the right side, `NOCASE` is not supported.
- The spatial/temporal operators are not yet supported.
- Array predicates are not supported.
