# Alternative Schema

## Metadata

|Tag |Value |
|---- | ---------------- |
|Proposal |[Alternative Schema](https://github.com/opengeospatial/ogcapi-features/tree/master/proposals/Alternative%20Schema)|
|Authors|[Chuck Heazel](https://github.com/cmheazel)|
|Review Manager |TBD |
|Status |**Pilot** |
|Implementations |[Click Here](https://github.com/opengeospatial/ogcapi-features/tree/master/proposals/Alternative%20Schema/implementations.md)
|Issues |[129](https://github.com/opengeospatial/ogcapi-features/issues/129), [56](https://github.com/opengeospatial/ogcapi-features/issues/56)|
|Previous Revisions |none |
 
.Change Log

|Date |Responsible Party |Description |
|---- | ---------------- | ---------- |
|8/21/19 |C. Heazel|Initial Markup Draft |
 
## Introduction

This is a proposal to add a new optional field called ``alternativeSchema`` to OpenAPI documents provided by OGC APIs. This new field will greatly enhance the ability of the OpenAPI document to describe the hosted resources.

## Motivation

OpenAPI allows APIs to describe the syntax of their request and response messaged using a JSON Schema-like syntax. However, not all messages will be in JSON. The ability to refer to one or more external schema will allow an API to describe the syntax of a message regardless of the format used.

For example: Some XML payloads are defined by an XML schema (the syntax) and a suite of Schematron rules (valid values). JSON Schema cannot effectively represent their content. By providing access to the appropriate XML Schema and Schematron files, the payload can be validated the way it was intended to be.

## Proposed solution

This proposal defines an extension to the OpenAPI document used by OGC APIs. It is documented in the form of modifications to the OpenAPI 3.0 specification:

1. Extend the Schema Object by the addition of the x-oas-draft-alternativeSchema field.
1. Addition of the Alternative Schema Object.
1. Addition of Alternative Schema examples.
1. Addition of a preliminary discussion of the Alternative Schema registry.

## Detailed design

###  Extend the Schema Object 

The OpenAPI Schema Object is extended by the addition of the x-oas-draft-alternativeSchema field. The proposed changes to the OpenAPI specification are provided in [schema_object.md](https://github.com/opengeospatial/ogcapi-features/tree/master/proposals/Alternative%20Schema/schema_object.md)

###  Add the Alternative Schema Object 

The new object, the Alternative Schema Object is added to the OpenAPI specification. The proposed changes to the OpenAPI specification are provided in [alternative_schema_object.md](https://github.com/opengeospatial/ogcapi-features/tree/master/proposals/Alternative%20Schema/alternative_schema_object.md)

### Provide Alternative Schema Examples
Examples of the use of the Alternative Schema capability is added to the OpenAPI specification. The proposed changes to the OpenAPI specification are provided in [alternative_schema_examples.md](https://github.com/opengeospatial/ogcapi-features/tree/master/proposals/Alternative%20Schema/alternative_schema_examples.md)

### Alternative Schema Registry

Values used to populate the Alternative Schema Object should be provided by an Alternative Schema Registry. A preliminary Alternative Schema Registry has been developed by the OpenAPI Technical Steering Committee.  It is located [here](https://spec.openapis.org/registry/alternative-schema).

*** Note this is a placeholder registry. Don't take the values seriously. ***  

Inital contents of the registry include:

|Value |Description |Issue | 
|--- | --- | --- |
|jsonSchema |JSON Schema |#1532 | 
|xsdSchema |XML Schema |#1532 |

## Backwards compatibility

This proposal makes use of the extensibility features of OpenAPI. All changes sould appear as extensions and handled accordingly.

## Alternatives considered

Embedding non-JSON content in the OAS document would have imposed an unacceptable burden on tooling. Therefore, an extenal link was prefered. Considerable discussion was held in the OpenAPI Technican Steering Comittee over exactly how the links should be represented in the Schema Object. The selected option should support the greatest number of possible combinations of external schema that can be expressed with the OpenAPI schema language.

