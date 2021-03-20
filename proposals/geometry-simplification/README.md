# OGC API - Features - Part n: Geometry Simplification

This folder contains an outline for the "Geometry Simplification" extension of the OGC API Features standard.

THIS IS CURRENTLY A PROPOSAL DRAFT.

A new part "Geometry simplification" will specify a query parameter to indicate a scale or zoom level at which the features will be displayed (resources Features and Features). The returned curve/surface/solid geometries will be simplified accordingly. The planned schedule is: Public Review by October 2021.

By default, OGC API Features always returns the complete feature geometry in a response. However, the client sometimes need the geometry only at a certain scale or zoom level for presenting the feature on a map. A capability to restrict the response to the necessary detail can reduce the volume of data to be transmitted.

The standard will define two requirements classes:

- "Geometry Simplification" will specifies a query parameter for the `/collections/{collectionId}/items` and `/collections/{collectionId}/items/{featureId}` endpoints:
  - `maxAllowableOffset` (default: no simplification): The input parameter ε to the [Douglas–Peucker algorithm](https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm). The value is in the units of the response coordinate reference system.
    - Alternate ways to specify such a parameter could be the use of a map scale denominator or a zoom level. For the zoom level we would need to define a fixed mapping from zoom level to scale, e.g. using the well-known WebMercatorQuad zoom levels: http://docs.opengeospatial.org/is/17-083r2/17-083r2.html#62. The details how the API simplifies the geometry based on the scale information is left to the implementation.
- "Geometry Simplification (Features) will specify the requirements for implementations that support "Geometry Simplification" and http://www.opengis.net/spec/ogcapi-features-1/1.0/req/core. The requirements apply only to collections with no `itemType` or with a value "feature".

For discussion: Should the parameter on the `/collections/{collectionId}/items` endpoint also act as a filter? For example, at a zoom level 3 only national roads could be returned from a collection with road features.

## Example

Compare:

- https://demo.ldproxy.net/daraa/collections/SettlementSrf/items/34
- https://demo.ldproxy.net/daraa/collections/SettlementSrf/items/34?maxAllowableOffset=0.001
- https://demo.ldproxy.net/daraa/collections/SettlementSrf/items/34?maxAllowableOffset=0.01
