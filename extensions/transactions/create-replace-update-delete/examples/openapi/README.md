# OpenAPI definition examples

This folder contains the OpenAPI definitions of the test deployment that is used
by the [executable tests](../../executable-tests) of the Abstract Test Suite
(Annex A). They are examples of how the resources and operations specified by
this Standard can be described in an API definition. Both definitions were
exported from the running deployment (`{landingPageUri}/api?f=yaml`), so the
server URL is the local test deployment.

[ogcapi-features-4-test-api.yaml](ogcapi-features-4-test-api.yaml) is the
definition of the main test API with two feature collections:

* `buildings` — the server assigns the feature identifiers, so new features are
  created with POST on `/collections/buildings/items`;
* `buildings_upsert` — the client assigns the feature identifiers, so there is no
  POST operation and new features are created with PUT on
  `/collections/buildings_upsert/items/{featureId}`.

Both collections support PUT, PATCH and DELETE on the feature and describe the
request bodies (GeoJSON, GML and, for PATCH, JSON Merge Patch) as well as the
`Content-Crs` header, the `Prefer` header with the handling preference and the
`Link` header for the profile of a GeoJSON request body.

[ogcapi-features-4-test-api-no-crs.yaml](ogcapi-features-4-test-api-no-crs.yaml)
is the definition of the second API of the test deployment, which does not
support coordinate reference systems other than WGS 84 longitude/latitude.

The definitions include the responses that this Standard specifies for the
operations, including `201` for a PUT request that creates a feature — declared for
the collection `buildings_upsert`, the only collection where PUT can create one —
and `412` and `428` for the conditional requests of the Optimistic Locking
conformance classes.

NOTE: The definitions describe the implementation that was used to validate the
Abstract Test Suite; they are not normative. They do not describe the OPTIONS
operations at all, so the `Accept-Post` and `Accept-Patch` headers required by
`/req/create-replace-delete/options-accept-post` and
`/req/update/options-accept-patch` do not occur in the definitions, although the
implementation returns them.
