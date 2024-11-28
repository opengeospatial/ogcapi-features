# OpenAPI descriptions of API building blocks

There are two aspects of the use of [OpenAPI](https://openapis.org) in OGC API Features.

1. OpenAPI is used to define the API building blocks that are specified by OGC API Features. That is, OpenAPI components are used to normatively specify characteristics of the API building blocks (content schemas, query or path parameters, etc.). In version 1.0 of Part 1 (Core) OpenAPI 3.0 has been used. Starting with version 1.1, OpenAPI 3.1 will be used to document the API building blocks in OGC API Features standards.

2. OpenAPI descriptions can be used by API instances to document the API. There will be separate requirements classes for OpenAPI 3.0 and OpenAPI 3.1 in OGC API - Features - Part 1: Core 1.1. To support reuse of the API building blocks the OpenAPI components are maintained for both versions of OpenAPI ([ogcapi-features-1-oas30.yaml](ogcapi-features-1-oas30.yaml) and [ogcapi-features-1-oas31.yaml](ogcapi-features-1-oas31.yaml)). The differences are small ("null" is a type in OpenAPI 3.1 vs the use of "nullable" as an attribute of a property in OpenAPI 3.0; in addition, "const" can be used in OpenAPI 3.1 for enumerations with a single value).

For backwards compatibility, [ogcapi-features-1.yaml](ogcapi-features-1.yaml) is the OpenAPI description for version 1.0.1 so that existing references from APIs to this document continue to work.
