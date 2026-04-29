# Versioned Features

## Metadata

|Tag |Value |
|---- | ---------------- |
|Proposal |[Versioned Features](https://github.com/opengeospatial/ogcapi-features/tree/master/proposals/versioned-features.md)|
|Authors|[Clemens Portele](https://github.com/cportele)|
|Status |Draft|
|Implementations |implementation in ldproxy is planned|
|Issues |[#430](https://github.com/opengeospatial/ogcapi-features/issues/430), [#764](https://github.com/opengeospatial/ogcapi-features/issues/764)|

**Change Log**

|Date |Responsible Party |Description |
|---- | ---------------- | ---------- |
|2026-04-27 |[Clemens Portele](https://github.com/cportele) |Initial version |

## Introduction

This proposal defines a mechanism to discover, access and mutate versioned feature resources.

A versioned feature is a feature whose state may change over time. Any change in a feature - that is, any change in a property including geometry, temporal properties, or feature relationships - creates a new version. Each feature is therefore a sequence of one or more versions, where each version is temporally connected to the predecessor and successor version, except the first version which has no predecessor and the latest version which has no successor.

Two distinct interpretations of the time axis are common in versioned datasets:

- **Transaction time** semantics: the timestamp of a version reflects when the change was recorded in the dataset. The version history is a faithful audit trail of what the dataset asserted at any past moment, regardless of whether the underlying real-world state was correct at that time.
- **Validity time** semantics: the timestamp of a version reflects when the represented real-world state began to be true. Corrections to historical real-world states are not modelled; only changes that take effect from a point in time onward are recorded.

This extension supports both semantics. A server declares which interpretation applies to a collection in the Collection resource (see [Collection metadata](#collection-metadata)). In both cases, version identifiers are permanent: once a version exists, its timestamp does not change. In particular, no operation alters or inserts a version with a timestamp earlier than the latest existing version of the same feature ("no backdating").

Validity intervals of two versions of the same feature do not overlap, except that the end instant of one version may coincide with the start instant of the immediately following version. This convention is consistent with the closed-interval semantics used by OGC API Features and JSON-FG and avoids artificial gaps between consecutive versions.

Bitemporal modelling - recording both transaction time and validity time independently - is out of scope for this extension and may be addressed by a future extension.

While this extension is designed for feature resources, the general design should be applicable to other OGC API resources as well.

The design is inspired by [RFC 7089 "HTTP Framework for Time-Based Access to Resource States -- Memento"](https://www.rfc-editor.org/rfc/rfc7089.html), in particular pattern 1.2, and uses link relations from [RFC 5829 "Link Relation Types for Simple Version Navigation between Web Resources"](https://www.rfc-editor.org/rfc/rfc5829.html).

## Motivation

Some feature datasets include a version history of the features to record the changes over time. Typical examples are datasets about land use, land cover or cadastral parcels.

The design of OGC API Features Part 1: Core does not support such data properly and requires hacks and workarounds for such data.

The standard approach is to represent each feature version as a feature and define your own conventions to identify other versions of the same feature. This has side effects that are not desirable in most cases: Queries will return multiple versions of the same feature unless carefully crafted filters are submitted with each query; CRUD operations will not work as expected - changing a feature is not a "Replace" as a new version has to be added and the current version needs to be retired; etc.

Additional API components are needed to properly represent such datasets consistent with the current resource design of OGC API Features Part 1: Core.

## Proposed solution

The proposed design is based on pattern 1.2 of [RFC 7089 "HTTP Framework for Time-Based Access to Resource States -- Memento"](https://www.rfc-editor.org/rfc/rfc7089.html). For background information look at [Memento - Time Travel for the Web](https://mementoweb.org/about/). While these HTTP extensions never saw uptake in mainstream, we can still learn from all the thoughts that went into the Memento design and adapt it so that the API extensions feel "natural". The main difference between the Memento pattern 1.2 and the proposed solution is that instead of an `Accept-Datetime` header for time negotiation the query parameter `datetime` is used.

In addition, the link relations from [RFC 5829 "Link Relation Types for Simple Version Navigation between Web Resources"](https://www.rfc-editor.org/rfc/rfc5829.html) are used.

### Relationship to the existing `datetime` parameter

OGC API Features Part 1: Core already defines a `datetime` query parameter for filtering by a feature's intrinsic temporal property. This extension intentionally does not introduce a new parameter; instead, in collections that conform to this extension the existing `datetime` parameter is interpreted as a selector over the temporal validity of feature versions. The two interpretations coincide by construction, because the temporal validity of a version is encoded as the feature's primary interval (see below). A client unaware of the extension will therefore observe filtering behaviour identical to Part 1: Core.

If OGC API Features Part 5: Schemas is supported, the schema of the collection has to identify an interval describing the temporal validity of a feature version using the `primary-interval` role or the `primary-interval-start`/`primary-interval-end` roles. Conformance to this extension requires the primary interval to be present.

All RFC 3339 timestamps used by this extension in URIs, request headers, and feature data are expressed in UTC. `Memento-Datetime` headers and `datetime` link attributes use the HTTP-date syntax from RFC 7089, expressed in GMT.

#### Version resolution at shared transition instants

Version validity intervals are encoded and interpreted as closed intervals. Both the start instant and the end instant are included. This follows the semantics of OGC API Features and JSON-FG.

Two consecutive versions of the same feature may share a transition instant where the end instant of the earlier version is identical to the start instant of the later version. Such endpoint sharing is not treated as a temporal conflict.

When an operation resolves an instant to a single version of a feature and more than one version matches only because of such a shared transition instant, the later version is selected. Equivalently, for an instant `t`, the selected version is the matching version with the greatest version timestamp that is less than or equal to `t`.

This tie-break rule applies to feature access (`/collections/{collectionId}/items/{featureId}`) and to instant queries on the Features resource (`/collections/{collectionId}/items?datetime=<instant>`). It ensures that a snapshot at a transition instant contains the version that became effective at that instant.

For interval queries on the Features resource (`datetime=<interval>`), the normal OGC API Features temporal-intersection semantics apply. Every version whose closed validity interval intersects the query interval is selected. The tie-break rule is not used to remove endpoint-only matches from interval queries.

### Collection metadata

A collection that conforms to this extension declares the time-axis semantics that apply to its features as part of the Collection resource (`/collections/{collectionId}`) in a `versioning` object carrying a `timeAxis` property. The declared value is exactly one of:

- `validity-time`: the timestamp of a feature version reflects when the represented real-world state began to be true;
- `transaction-time`: the timestamp of a feature version reflects when the change was recorded in the dataset.

This metadata element is mandatory for any collection conforming to this extension: clients rely on it to interpret version timestamps correctly.

For collections that support mutations, the `versioning` object also carries a `mutationTime` property. This property is separate from `timeAxis`; it describes how timestamps for new versions and retirements are determined during mutations. The `mutationTime` property is required if and only if the collection conforms to the *Mutations* requirements class; its presence is therefore an unambiguous indicator that the collection accepts mutations. The declared value is exactly one of:

- `server`: the server determines mutation timestamps, typically from the time at which the transaction is processed;
- `client`: the client supplies mutation timestamps using receivable properties - or in case of a DELETE operation via the `OGC-Mutation-Datetime` HTTP request header.

The combination `timeAxis: "transaction-time"` with `mutationTime: "server"` as well as `timeAxis: "validity-time"` with `mutationTime: "client"` is expected to be common, but other combinations are possible. For example, a transaction-time collection that is a replicate of an upstream database may accept client-provided transaction timestamps in such a workflow.

Example for a mutable collection:

```
"versioning": {
  "timeAxis": "transaction-time",
  "mutationTime": "server"
}
```

Example for a read-only collection that is updated through other means:

```
"versioning": {
  "timeAxis": "validity-time"
}
```

### Access to a feature and its versions

Access to a feature and its versions is as follows (in terms of the Memento framework):

- Original Resource and Time Gate (coinciding in pattern 1.2): the feature (`/collections/{collectionId}/items/{featureId}`)
  - Without a query parameter `datetime`, the response is the feature version that is valid at the time the request is processed. This extension does not define a literal `datetime=now` parameter value. Note: Adding "now" as a value could be discussed in the v1.1 revision of OGC API Features Part 1: Core.
  - With a query parameter `datetime` containing an RFC 3339 timestamp, the response is the feature version that is valid at that moment in time, after applying the version-resolution rule at shared transition instants.
  - If the feature does not exist at the requested time, the response is 410 Gone (or 404 Not Found, if the feature never existed).
  - All 200 responses include a `Memento-Datetime` HTTP header carrying the canonical start timestamp of the returned version (this is the timestamp embedded in the canonical Memento URI for that version, which may differ from the timestamp the client supplied).
  - All 200 responses include a `self` link reflecting the request URI (with the `datetime` query parameter as supplied by the client, if any), a `canonical` link pointing to the canonical Memento URI of the returned version (per [RFC 6596](https://www.rfc-editor.org/rfc/rfc6596.html)), an `original` link pointing to the feature URI without a `datetime` parameter, a `timemap` link and a `version-history` link referencing the Time Map (also as `Link` headers), and `predecessor-version` and `successor-version` links if a predecessor or successor exists. The `self` and `canonical` links may resolve to the same URI when the request was already made with the canonical timestamp; the `self` and `original` links may resolve to the same URI when the request was made without a `datetime` parameter.
  - All 410 responses include a `latest-version` link, a `timemap` link, and a `version-history` link.
  - Responses are returned with status 200 directly (no 302/303/307 redirect to the canonical Memento URI). Clients identify the canonical version via the `canonical` link and the `Memento-Datetime` header.
- Memento: a feature version (`/collections/{collectionId}/items/{featureId}?datetime={timestamp}`)
  - The `timestamp` in the canonical Memento URI is the start of the validity of the feature version. Because version timestamps are permanent, this URI is a stable, permanent identifier for the version.
- Time Map: the available versions of a feature (`/collections/{collectionId}/items/{featureId}/versions`)
  - Returns all TimeMap links, in particular including a `memento` link for each feature version.
  - Each `memento` link includes a `datetime` link parameter carrying the `Memento-Datetime` value of the linked version, expressed in the HTTP-date syntax from RFC 7089 (GMT).
  - The first and last feature version are identified by `first` and `last`/`latest-version` links.
  - If the "JSON" requirements class is supported, the JSON encoding of the Time Map returns a JSON object with a `links` array. Links use a single relation value per link object; where several relation values apply to the same target, separate link objects are used.
  - Support for the Media Type `application/link-format` as defined by [RFC 6690](https://www.rfc-editor.org/rfc/rfc6690.html) is recommended.

### Caching

Mementos - i.e., responses to GET requests with a fully-specified `datetime` query parameter that resolves to a non-current version - are immutable: once a version has been retired, neither its content nor its canonical timestamp will ever change. Servers can therefore return such responses with strong validators (e.g., `ETag`) and aggressive freshness directives (e.g., `Cache-Control: public, max-age=..., immutable`).

The canonical version timestamp carried by `Memento-Datetime` is permanent for both current and non-current versions. However, responses that represent the current version are not immutable, because the open end of the version interval may later be replaced by a concrete end timestamp when the version is retired. Such responses are usually served with shorter freshness lifetimes or with cache validation only.

### Behaviour on the Features resource

For GET requests to the Features resource (`/collections/{collectionId}/items`), the behaviour is as follows:

- If the `datetime` parameter is absent, only feature versions valid at the time the request is processed are returned.
- When using the `datetime` parameter with a timestamp, the query returns versions that were valid at that specific time, after applying the version-resolution rule at shared transition instants. The result is a snapshot with at most one version per feature identity.
- When using the `datetime` parameter with an interval, the query returns all feature versions whose closed validity intervals intersect that time period.
- Other filter parameters (`bbox`, `filter` with CQL2, `filter` with property/value, etc.) are evaluated against the version set selected by `datetime`. That is, a filter such as `height_m > 12` matches a feature version if and only if that specific version satisfies the filter; versions of the same feature that do not satisfy the filter are excluded, even if other versions of the same feature would have satisfied it. The selection by `datetime` therefore happens conceptually first, and the remaining filters are applied to the resulting set of versions.
- If a response includes multiple versions of a feature, there are multiple options how to represent the feature and its versions, all with drawbacks. What works best depends on the data, the use case and the capabilities/constraints of the selected feature format. Three representations are defined as profiles:
  - Profile `versions-as-features`: Each version is represented as a feature.
    - A consequence is that multiple features in the response will have the same feature id.
    - Clients may not be prepared for duplicate feature ids and this could lead to errors or side effects (if a client maintains a map of features by id, the map will only include one of the versions). For this reason, this profile is only a good default profile in APIs where it is known that clients are able to handle duplicate ids.
    - This profile cannot be used with feature formats that require unique ids, e.g., GML.
    - `numberMatched`/`numberReturned` represent the number of feature versions in the response feature collection.
  - Profile `versions-as-features-unique-ids`: Each version is represented as a feature - with a unique id.
    - Similar to `versions-as-features` with the difference that the feature id is a combination of the feature id and the version id (the timestamp).
    - This ensures uniqueness, but results in differences between the feature ids depending on the temporal selection criteria.
    - Where the selected feature format supports feature-level links, `original` and `canonical` links can be used to expose both identities explicitly: the stable feature URI and the canonical version URI.
    - `numberMatched`/`numberReturned` represent the number of feature versions in the response feature collection (same as `versions-as-features`).
  - Profile `features-with-time-slices`: The versions are merged into a single feature.
    - All (selected) versions of a feature are encoded as a single feature, with the version history represented in a more complex representation of the properties. This is conceptually cleaner than the other profiles, but it may be more difficult to handle in implementations:
      - Most feature formats are not designed for such a representation.
        - Take GeoJSON/JSON-FG as an example: If the geometry changes over time, there is no way to encode this in `geometry` or `place`. In addition, while time-varying property values can in general be represented in a more complex representation in `properties`, where, for example, time slices are represented separately (similar to GML's dynamic features), most clients will not be able to handle such a representation, which is significantly more complex to process. For this reason, this profile is only a good default profile in APIs where it is known that clients are able to handle time slices.
        - Other feature formats that only support a tabular structure, e.g., FlatGeobuf, will not be able to be used in such APIs.
      - This approach also loses the capability to access only the current features via the same API without any overhead introduced by an extension for versioned features.
      - For cases where the versioned data is stored as a database row per version, the first two profiles are straightforward to implement, while it could be very complex to encode a feature with all its changes over time.
    - `numberMatched`/`numberReturned` represent the number of features in the response feature collection (one entry per distinct feature identity, not per version).

In all profiles, `numberMatched`/`numberReturned` always count the entries in the response feature collection.

### Mutations

For CRUD requests to a feature, the following applies:

- Creation of the first version of a feature occurs using POST to `/collections/{collectionId}/items` (or using PUT to `/collections/{collectionId}/items/{featureId}`, if `supportsNonAutogeneratedResourceIds: true` for the collection).
  - If PUT is used to create the first version, the stable feature identifier is taken from the target URI.
- PUT applied to a feature with a current version retires the current version at the time when the new version starts.
- PATCH, if supported, has the same versioning behaviour as PUT: the current version is retired and a new version is created.
- DELETE retires the current version and the feature. The retirement timestamp is determined by the collection's `mutationTime` value:
  - If `mutationTime` is `server`, the server uses its own clock at the time the transaction is processed.
  - If `mutationTime` is `client`, the client supplies the retirement timestamp via the `OGC-Mutation-Datetime` HTTP request header. If the header is absent, the server returns 400 Bad Request.
- The same `mutationTime` rule applies to the start timestamp of versions created by POST, PUT, or PATCH:
  - If `mutationTime` is `server`, the server sets the start timestamp from its own clock at the time the transaction is processed. Any value supplied by the client for the start of the primary interval is ignored or replaced.
  - If `mutationTime` is `client`, the start timestamp is taken from the start of the primary interval in the request body. If the primary interval, or its start instant, is missing in the body, the server returns 400 Bad Request.
  - The `OGC-Mutation-Datetime` header is used for DELETE only. Servers ignore it for POST, PUT, and PATCH, or, if strict validation is preferred, return 400 Bad Request when it is supplied alongside a request that carries a body.
- PUT, PATCH, and DELETE are not applied to canonical version URIs containing a `datetime` query parameter. Version URIs identify specific feature versions. Mutations are applied to the original feature URI without a `datetime` parameter. A request that attempts to mutate a version URI returns 405 Method Not Allowed.
- If PUT or DELETE is applied to a feature that exists only in history, a 410 Gone error is returned.
- If the feature has never existed and the collection does not allow PUT to create new features (i.e., `supportsNonAutogeneratedResourceIds: false`), a 404 Not Found error is returned.
- No mutation creates a version whose validity starts at or before the start of the latest existing version of the same feature. No mutation creates overlapping validity intervals for versions of the same feature, except for the shared transition instant between two consecutive versions. Requests that violate these constraints are rejected with 409 Conflict.
- Use of the `If-Unmodified-Since` header is recommended to avoid lost updates.

For transactions (POST requests to `/transactions`) the same behaviour applies to the individual operations in the transaction. If `mutationTime` is `server`, all changes in an atomic transaction occur at the same time, while in a batch transaction the time when the individual operation is executed is used. If `mutationTime` is `client`, the supplied mutation timestamp is used for the affected operation or operations as defined by the transaction encoding.

## An example

The following is a building with two versions (another floor was added in 2012):

```
{
    "type": "FeatureCollection",
    "featureType": "building",
    "conformsTo" : ["http://www.opengis.net/spec/json-fg-1/1.0/conf/core"],
    "features": [
        {
            "type"       : "Feature",
            "id"         : "1",
            "time"       : { "interval": ["2001-07-02T10:43:17Z", "2012-10-14T16:43:17Z"] },
            "geometry"   : { "type": "Point", "coordinates": [7, 50] },
            "properties" : {"use": "residential building", "height_m": 10.8}
        },
        {
            "type"       : "Feature",
            "id"         : "1",
            "time"       : { "interval": ["2012-10-14T16:43:17Z", ".."] },
            "geometry"   : { "type": "Point", "coordinates": [7, 50] },
            "properties" : {"use": "residential building", "height_m": 14.0}
        }
    ]
}
```

NOTE: ISO 8601 time intervals are closed on both ends (`[start, end]`). Where two consecutive versions meet, their endpoints share the same instant - in the example, `2012-10-14T16:43:17Z` is both the end of the first version and the start of the second. A request whose `datetime` falls exactly on the boundary returns the later version. This convention avoids any one-second gap between consecutive versions and keeps the version sequence temporally contiguous.

A request to retrieve the feature returns the current version:

```
GET /api/collections/building/items/1

HTTP/2 200
...
Memento-Datetime: Sun, 14 Oct 2012 16:43:17 GMT
Link: <https://example.com/api/collections/building/items/1>; rel="self"
Link: <https://example.com/api/collections/building/items/1?datetime=2012-10-14T16:43:17Z>; rel="canonical"
Link: <https://example.com/api/collections/building/items/1>; rel="original"
Link: <https://example.com/api/collections/building/items/1?datetime=2001-07-02T10:43:17Z>; rel="predecessor-version"
Link: <https://example.com/api/collections/building/items/1/versions>; rel="timemap"
Link: <https://example.com/api/collections/building/items/1/versions>; rel="version-history"

{
    "type"       : "Feature",
    "featureType": "building",
    "conformsTo" : ["http://www.opengis.net/spec/json-fg-1/1.0/conf/core"],
    "id"         : "1",
    "time"       : { "interval": ["2012-10-14T16:43:17Z", ".."] },
    "geometry"   : { "type": "Point", "coordinates": [7, 50] },
    "properties" : {"use": "residential building", "height_m": 14.0}
}
```

A request to a timestamp in 2005 returns the first version. The `canonical` link uses the start timestamp of the selected version, not the timestamp supplied by the client; the `self` link reflects the request URI as supplied:

```
GET /api/collections/building/items/1?datetime=2005-01-01T00:00:00Z

HTTP/2 200
...
Memento-Datetime: Mon, 02 Jul 2001 10:43:17 GMT
Link: <https://example.com/api/collections/building/items/1?datetime=2005-01-01T00:00:00Z>; rel="self"
Link: <https://example.com/api/collections/building/items/1?datetime=2001-07-02T10:43:17Z>; rel="canonical"
Link: <https://example.com/api/collections/building/items/1>; rel="original"
Link: <https://example.com/api/collections/building/items/1?datetime=2012-10-14T16:43:17Z>; rel="successor-version"
Link: <https://example.com/api/collections/building/items/1/versions>; rel="timemap"
Link: <https://example.com/api/collections/building/items/1/versions>; rel="version-history"

{
    "type"       : "Feature",
    "featureType": "building",
    "conformsTo" : ["http://www.opengis.net/spec/json-fg-1/1.0/conf/core"],
    "id"         : "1",
    "time"       : { "interval": ["2001-07-02T10:43:17Z", "2012-10-14T16:43:17Z"] },
    "geometry"   : { "type": "Point", "coordinates": [7, 50] },
    "properties" : {"use": "residential building", "height_m": 10.8}
}
```

A request exactly at the transition instant returns the later version:

```
GET /api/collections/building/items/1?datetime=2012-10-14T16:43:17Z

HTTP/2 200
...
Memento-Datetime: Sun, 14 Oct 2012 16:43:17 GMT
Link: <https://example.com/api/collections/building/items/1?datetime=2012-10-14T16:43:17Z>; rel="self"
Link: <https://example.com/api/collections/building/items/1?datetime=2012-10-14T16:43:17Z>; rel="canonical"
Link: <https://example.com/api/collections/building/items/1>; rel="original"
Link: <https://example.com/api/collections/building/items/1?datetime=2001-07-02T10:43:17Z>; rel="predecessor-version"
Link: <https://example.com/api/collections/building/items/1/versions>; rel="timemap"
Link: <https://example.com/api/collections/building/items/1/versions>; rel="version-history"

...
```

A request to a timestamp in 1990 returns 410 Gone:

```
GET /api/collections/building/items/1?datetime=1990-01-01T00:00:00Z

HTTP/2 410
...
Link: <https://example.com/api/collections/building/items/1?datetime=2012-10-14T16:43:17Z>; rel="latest-version"
Link: <https://example.com/api/collections/building/items/1/versions>; rel="timemap"
Link: <https://example.com/api/collections/building/items/1/versions>; rel="version-history"
```

A request to the version history returns the Time Map, here as JSON:

```
GET /api/collections/building/items/1/versions

HTTP/2 200
...

{
    "links": [
        { "rel": "self", "href": "https://example.com/api/collections/building/items/1/versions" },
        { "rel": "original", "href": "https://example.com/api/collections/building/items/1" },
        { "rel": "first", "href": "https://example.com/api/collections/building/items/1?datetime=2001-07-02T10:43:17Z" },
        { "rel": "memento", "href": "https://example.com/api/collections/building/items/1?datetime=2001-07-02T10:43:17Z", "datetime": "Mon, 02 Jul 2001 10:43:17 GMT" },
        { "rel": "last", "href": "https://example.com/api/collections/building/items/1?datetime=2012-10-14T16:43:17Z" },
        { "rel": "latest-version", "href": "https://example.com/api/collections/building/items/1?datetime=2012-10-14T16:43:17Z" },
        { "rel": "memento", "href": "https://example.com/api/collections/building/items/1?datetime=2012-10-14T16:43:17Z", "datetime": "Sun, 14 Oct 2012 16:43:17 GMT" }
    ]
}
```

A request to retrieve building features returns the current versions (in this case just one, since there is only a single building in the example dataset):

```
GET /api/collections/building/items

HTTP/2 200
...

{
    "type": "FeatureCollection",
    "featureType": "building",
    "conformsTo" : ["http://www.opengis.net/spec/json-fg-1/1.0/conf/core"],
    "numberReturned": 1,
    "features": [
        {
            "type"       : "Feature",
            "id"         : "1",
            "time"       : { "interval": ["2012-10-14T16:43:17Z", ".."] },
            "geometry"   : { "type": "Point", "coordinates": [7, 50] },
            "properties" : {"use": "residential building", "height_m": 14.0}
        }
    ]
}
```

A request for the building on January 1st, 2005, returns the first version of the building:

```
GET /api/collections/building/items?datetime=2005-01-01T00:00:00Z

HTTP/2 200
...

{
    "type": "FeatureCollection",
    "featureType": "building",
    "conformsTo" : ["http://www.opengis.net/spec/json-fg-1/1.0/conf/core"],
    "numberReturned": 1,
    "features": [
        {
            "type"       : "Feature",
            "id"         : "1",
            "time"       : { "interval": ["2001-07-02T10:43:17Z", "2012-10-14T16:43:17Z"] },
            "geometry"   : { "type": "Point", "coordinates": [7, 50] },
            "properties" : {"use": "residential building", "height_m": 10.8}
        }
    ]
}
```

A request for the building on January 1st, 1990, returns no buildings:

```
GET /api/collections/building/items?datetime=1990-01-01T00:00:00Z

HTTP/2 200
...

{
    "type": "FeatureCollection",
    "featureType": "building",
    "conformsTo" : ["http://www.opengis.net/spec/json-fg-1/1.0/conf/core"],
    "numberReturned": 0,
    "features": []
}
```

A request for the buildings since January 1st, 2005, returns both versions. The representation depends on the profile. The server selects the profile based on the requested profile, the server capabilities and the selected feature format. Here is the response for each profile:

```
GET /api/collections/building/items?datetime=2005-01-01T00:00:00Z/..&profile=versions-as-features

HTTP/2 200
...
Link: <http://www.opengis.net/def/profile/OGC/0/versions-as-features>; rel="profile"

{
    "type": "FeatureCollection",
    "featureType": "building",
    "conformsTo" : ["http://www.opengis.net/spec/json-fg-1/1.0/conf/core"],
    "numberReturned": 2,
    "features": [
        {
            "type"       : "Feature",
            "id"         : "1",
            "time"       : { "interval": ["2001-07-02T10:43:17Z", "2012-10-14T16:43:17Z"] },
            "geometry"   : { "type": "Point", "coordinates": [7, 50] },
            "properties" : {"use": "residential building", "height_m": 10.8}
        },
        {
            "type"       : "Feature",
            "id"         : "1",
            "time"       : { "interval": ["2012-10-14T16:43:17Z", ".."] },
            "geometry"   : { "type": "Point", "coordinates": [7, 50] },
            "properties" : {"use": "residential building", "height_m": 14.0}
        }
    ]
}
```

```
GET /api/collections/building/items?datetime=2005-01-01T00:00:00Z/..&profile=versions-as-features-unique-ids

HTTP/2 200
...
Link: <http://www.opengis.net/def/profile/OGC/0/versions-as-features-unique-ids>; rel="profile"

{
    "type": "FeatureCollection",
    "featureType": "building",
    "conformsTo" : ["http://www.opengis.net/spec/json-fg-1/1.0/conf/core"],
    "numberReturned": 2,
    "features": [
        {
            "type"       : "Feature",
            "id"         : "1.20010702T104317Z",
            "time"       : { "interval": ["2001-07-02T10:43:17Z", "2012-10-14T16:43:17Z"] },
            "geometry"   : { "type": "Point", "coordinates": [7, 50] },
            "properties" : {"use": "residential building", "height_m": 10.8}
        },
        {
            "type"       : "Feature",
            "id"         : "1.20121014T164317Z",
            "time"       : { "interval": ["2012-10-14T16:43:17Z", ".."] },
            "geometry"   : { "type": "Point", "coordinates": [7, 50] },
            "properties" : {"use": "residential building", "height_m": 14.0}
        }
    ]
}
```

```
GET /api/collections/building/items?datetime=2005-01-01T00:00:00Z/..&profile=features-with-time-slices

HTTP/2 200
...
Link: <http://www.opengis.net/def/profile/OGC/0/features-with-time-slices>; rel="profile"

{
    "type": "FeatureCollection",
    "featureType": "building",
    "conformsTo" : ["http://www.opengis.net/spec/json-fg-1/1.0/conf/core"],
    "numberReturned": 1,
    "features": [
        {
            "type"       : "Feature",
            "id"         : "1",
            "time"       : { "interval": ["2001-07-02T10:43:17Z", ".."] },
            "geometry"   : { "type": "Point", "coordinates": [7, 50] },
            "properties" : {
                "2001-07-02T10:43:17Z/2012-10-14T16:43:17Z": {"use": "residential building", "height_m": 10.8},
                "2012-10-14T16:43:17Z/.."                  : {"use": "residential building", "height_m": 14.0}
            }
        }
    ]
}
```

Note that this profile can only be applied in this case, because the geometry of the feature did not change over time.

## Backwards compatibility

The proposal is backwards compatible in the sense that for an API user or client that is not aware of the extensions for versioned features, the API still works and provides access to the dataset.

If the `datetime` parameter is not used on the Features resource, the API behaves as if only the current feature versions would be provided by the API.

If the `datetime` parameter is used on the Features resource with a timestamp, the situation at that time will be returned which should also work with current clients.

If the `datetime` parameter is used on the Features resource with an interval, the response may be surprising to existing clients in each of the three profiles discussed above.

In addition, the new API components allow API users/clients to discover and access previous feature versions.

## Requirements classes

The design segments naturally into the following requirements classes. Dependencies are noted; the formal requirements text will be elaborated when this proposal is converted into a candidate standard.

- **Core** - the foundation of the extension. Includes:
  - the `datetime` parameter on `/collections/{collectionId}/items/{featureId}` selecting a version; 200/410/404 status codes; the `self`, `canonical`, `original`, `predecessor-version`, `successor-version`, `latest-version`, `version-history`, and `timemap` link relations as described above; the `Memento-Datetime` response header on version responses; UTC normalisation of RFC 3339 timestamps; caching guidance for immutable Mementoes; and a primary interval on the feature schema (when Part 5: Schemas is supported);
  - the `/collections/{collectionId}/items/{featureId}/versions` Time Map resource and its JSON encoding, including `datetime` values on `memento` links;
  - the time-axis semantics metadata element on the collection resource;
  - the version-resolution rule for shared transition instants.

  Depends on OGC API Features Part 1: Core.

- **Time Map Link Format** - the `application/link-format` (RFC 6690) encoding of the Time Map. Depends on Core. Recommended.
- **Multiple Versions in a Response** - extends behaviour on `/items` to allow `datetime` intervals returning multiple versions per feature. Depends on Core. Includes the `numberMatched`/`numberReturned` rules and the filter-interaction rule. A server implementing this class also implements at least one of the three profile classes below.
  - **Profile: Versions as Features**
  - **Profile: Versions as Features with Unique IDs**
  - **Profile: Features with Time Slices**

- **Mutations** - PUT/PATCH/DELETE behaviour on versioned features, creation by POST and optionally by PUT upsert, the `mutationTime` collection metadata element, the `OGC-Mutation-Datetime` request header for client-supplied mutation timestamps, the prohibition on backdating and overlapping intervals except for a shared transition instant between consecutive versions, the rule that mutation requests target the original feature URI rather than canonical version URIs, and the use of `If-Unmodified-Since`. Depends on Core and on either OGC API Features Part 4 (Create, Replace, Update and Delete) or Part 11 (Atomic and Batch Transactions).

A minimally conformant server implements *Core*. *Multiple Versions in a Response* (with at least one profile) and *Mutations* are added as needed.
