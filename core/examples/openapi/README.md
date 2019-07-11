# OpenAPI definition examples

This folder includes two complete examples of an OpenAPI definition for a Web API implementing OGC API Features (the Core, HTML, GeoJSON and OpenAPI 3.0 conformance classes).

The [first example (ogcapi-features-1-example1.yaml)](ogcapi-features-1-example1.yaml) is a generic example that uses path parameters to describe all feature collections and all features. This OpenAPI definition does not provide any details on the collections or the feature content. This information is only available from the feature collection metadata. The API is also on [SwaggerHub](https://app.swaggerhub.com/apis/cportele/ogcapi-features-1-example1/1.0.0-draft.2).

The [second example (ogcapi-features-1-example2.yaml)](ogcapi-features-1-example2.yaml) does not use a path parameter for the collections and explicitly provides information about the feature collection 'buildings' (paths /collections/buildings etc.), the schema of the building features (schema buildingGeoJSON) and a filter parameter for building features (parameter function). The API is also on [SwaggerHub](https://app.swaggerhub.com/apis/cportele/ogcapi-features-1-example2/1.0.0-draft.2).