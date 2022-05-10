# OGC API - Features - Part n: Query by IDs

This folder contains an outline for the "Query by IDs" extension of the OGC API Features standard.

THIS IS CURRENTLY A PROPOSAL DRAFT.

This new part "Query by IDs" will define a new query parameter, which enables clients to query multiple features by their ID.

Individual features already can be queried by ID by using the `/collections/{collectionId}/items/{featureId}` resource specified in Part 1. However, when a client needs to retrieve multiple features by ID, it would need to make multiple requests, one for each feature to be fetched. A query parameter, which enables a client to retrieve multiple features by ID with a single query reduces the number of required requests to one. Sample use cases:

- The client needs to retrieve a unique set of features, but only the IDs of those features are available in the client's context.
- The client presents the features from a collection in a table and needs to retrieve a particular set of features again to update them.

The standard will define one requirement class:

- "Query by IDs" will specify a query parameter for the `/collections/{collectionId}/items` resource:

  - `ids` (default: no effect): The comma separted feature IDs from a collection to query.

For discussion:  When `ids` is used together with other query parameters of the `/collections/{collectionId}/items` resource, such as `bbox`, `datetime`, collection-specific filter parameters, `filter`, `filter-lang`, `filter-crs` and so on, should these query parameters be applied on the features selected by ID or not?

## Example

- https://demo.ldproxy.net/daraa/collections/SettlementSrf/items?ids=1,2,3
- https://demo.ldproxy.net/daraa/collections/SettlementSrf/items?ids=1,2,3&bbox=xmin,ymin,xmax,ymax
- https://demo.ldproxy.net/daraa/collections/SettlementSrf/items?ids=1,2,3&datetime=timestamp

