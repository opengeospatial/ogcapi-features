# Feature name


## Metadata

|Tag |Value |
|---- | ---------------- |
|Proposal |[002](https://github.com/opengeospatial/ogcapi-features/blob/Proposals/proposals/002_OpenAPI_Specification_31.md)|
|Authors|[Clemens Portele](https://github.com/cportele)|
|Review Manager |TBD |
|Status |Draft |
|Implementations |[Click Here](https://github.com/opengeospatial/ogcapi-features/blob/Proposals/proposals/002_OAS_31/implementations.md)|
|Issues |n/a |
|Previous Revisions |n/a |

.Change Log

|Date |Responsible Party |Description |
|---- | ---------------- | ---------- |
|2019-10-21 |C. Portele |Initial draft |

## Introduction

Version 3.1 of the OpenAPI Specification (OAS) should be available before the end of 2019. A key feature will be native support for JSON Schema draft 2019-09 for the description of schema components.

## Motivation

This will avoid the need to manage and publish two kinds of JSON schemas, one for the latest version of JSON Schema and one for the OAS variant.

## Proposed solution

Add a new requirements/conformance class "OpenAPI 3.1" in a new part of OGC API - Features.

## Detailed design

The new requirements class is a copy of the "OpenAPI 3.0" class, but with a dependency to OpenAPI version 3.1. Summarize the changes from the "OpenAPI 3.0" class and provide guidance on using 3.0, 3.1 or both.

## Backwards compatibility

Since a new conformance class will be added, the change is backwards compatible, if either APIs continue to support 3.0 or OpenAPI 3.1 is backwards compatible with version 3.0 (which is the current plan, but needs to be evaluated).

## Alternatives considered

Describe alternative approaches to addressing the same problem, and why you chose this approach instead.
